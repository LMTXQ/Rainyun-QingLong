import logging
from datetime import datetime
from typing import Dict, List

from api_client import RainyunAPI, RainyunAPIError

logger = logging.getLogger(__name__)


class ServerManager:
    """服务器自动续费管理"""
    
    def __init__(self, api: RainyunAPI, config: dict):
        self.api = api
        self.config = config
        self.renew_days = config.get("renew_days", 7)
        self.threshold_days = config.get("renew_threshold_days", 3)
        self.min_reserve = config.get("min_points_reserve", 5000)
        
        logger.info("🔧 服务器管理器初始化成功")
        logger.info(f"   续费天数: {self.renew_days} 天")
        logger.info(f"   续费阈值: 剩余 {self.threshold_days} 天时触发")
        logger.info(f"   保留积分: {self.min_reserve} 分")
    
    def check_and_renew(self) -> Dict:
        """检查所有服务器并自动续费"""
        result = {
            "total": 0,
            "renewed": 0,
            "skipped": 0,
            "failed": 0,
            "details": []
        }
        
        try:
            # 获取当前积分
            current_points = self.api.get_user_points()
            logger.info(f"💰 当前积分: {current_points}")
            
            # 获取服务器列表
            server_ids = self.api.get_server_list("rgs")
            result["total"] = len(server_ids)
            logger.info(f"🖥️  找到 {len(server_ids)} 台服务器")
            
            if not server_ids:
                logger.info("   暂无服务器需要检查")
                return result
            
            # 逐个处理服务器
            for idx, server_id in enumerate(server_ids, 1):
                logger.info(f"\n   [{idx}/{len(server_ids)}] 检查服务器 {server_id}")
                detail = self._process_server(server_id, current_points)
                result["details"].append(detail)
                
                if detail["action"] == "renewed":
                    result["renewed"] += 1
                    current_points = detail["points_after"]
                elif detail["action"] == "skipped":
                    result["skipped"] += 1
                elif detail["action"] == "failed":
                    result["failed"] += 1
            
            return result
            
        except RainyunAPIError as e:
            logger.error(f"❌ 服务器检查失败: {e}")
            result["failed"] = result["total"]
            return result
    
    def _process_server(self, server_id: int, available_points: int) -> Dict:
        """处理单个服务器"""
        detail = {
            "server_id": server_id,
            "action": "skipped",
            "reason": "",
            "points_cost": 0,
            "points_after": available_points,
            "exp_date": "",
            "days_left": 0
        }
        
        try:
            # 获取服务器详情
            info = self.api.get_server_detail(server_id)
            server_data = info.get("Data", {})
            renew_prices = info.get("RenewPointPrice", {})
            
            # 解析到期时间（支持多种格式）
            exp_date_raw = server_data.get("ExpDate", "")
            if not exp_date_raw:
                detail["action"] = "failed"
                detail["reason"] = "无法获取到期时间"
                logger.error(f"   ❌ {detail['reason']}")
                return detail
            
            # 判断是时间戳还是字符串
            if isinstance(exp_date_raw, int):
                # 时间戳格式（秒或毫秒）
                if exp_date_raw > 10000000000:  # 毫秒级时间戳
                    exp_date = datetime.fromtimestamp(exp_date_raw / 1000)
                else:  # 秒级时间戳
                    exp_date = datetime.fromtimestamp(exp_date_raw)
                exp_date_str = exp_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                # 字符串格式
                exp_date_str = str(exp_date_raw)
                try:
                    exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    # 尝试其他常见格式
                    try:
                        exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d")
                    except ValueError:
                        detail["action"] = "failed"
                        detail["reason"] = f"无法解析到期时间格式: {exp_date_str}"
                        logger.error(f"   ❌ {detail['reason']}")
                        return detail
            
            days_left = (exp_date - datetime.now()).days
            
            detail["exp_date"] = exp_date_str
            detail["days_left"] = days_left
            
            logger.info(f"   到期时间: {exp_date_str}")
            logger.info(f"   剩余天数: {days_left} 天")
            
            # 判断是否需要续费
            if days_left > self.threshold_days:
                detail["reason"] = f"剩余 {days_left} 天，暂不续费"
                logger.info(f"   ⏭️  {detail['reason']}")
                return detail
            
            # 获取续费价格
            renew_cost = renew_prices.get(str(self.renew_days))
            if not renew_cost:
                detail["action"] = "failed"
                detail["reason"] = f"无 {self.renew_days} 天续费价格"
                logger.error(f"   ❌ {detail['reason']}")
                return detail
            
            logger.info(f"   续费价格: {renew_cost} 积分")
            
            # 检查积分是否足够
            if available_points - renew_cost < self.min_reserve:
                detail["reason"] = (
                    f"积分不足（需 {renew_cost}，剩 {available_points}，"
                    f"需保留 {self.min_reserve}）"
                )
                logger.warning(f"   ⚠️  {detail['reason']}")
                return detail
            
            # 执行续费
            logger.info(f"   🔄 开始续费...")
            self.api.renew_server(server_id, self.renew_days)
            
            detail["action"] = "renewed"
            detail["points_cost"] = renew_cost
            detail["points_after"] = available_points - renew_cost
            detail["reason"] = f"成功续费 {self.renew_days} 天"
            
            logger.info(f"   ✅ 续费成功！")
            logger.info(f"   消耗积分: {renew_cost}")
            logger.info(f"   剩余积分: {detail['points_after']}")
            return detail
            
        except RainyunAPIError as e:
            detail["action"] = "failed"
            detail["reason"] = str(e)
            logger.error(f"   ❌ 续费失败: {e}")
            return detail
        except Exception as e:
            detail["action"] = "failed"
            detail["reason"] = f"未知错误: {str(e)}"
            logger.error(f"   ❌ 处理服务器 {server_id} 时发生异常: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return detail
    
    def generate_report(self, result: Dict) -> str:
        """生成续费报告"""
        lines = [
            "━━━━━━ 服务器续费报告 ━━━━━━",
            f"总计: {result['total']} 台",
            f"✅ 已续费: {result['renewed']} 台",
            f"⏭️  跳过: {result['skipped']} 台",
            f"❌ 失败: {result['failed']} 台",
            ""
        ]
        
        if not result["details"]:
            lines.append("暂无服务器")
            return "\n".join(lines)
        
        for detail in result["details"]:
            server_id = detail["server_id"]
            action = detail["action"]
            reason = detail["reason"]
            days_left = detail.get("days_left", 0)
            exp_date = detail.get("exp_date", "")
            
            if action == "renewed":
                lines.append(f"🟢 服务器 {server_id}: {reason}")
                lines.append(f"   到期时间: {exp_date}")
                lines.append(f"   消耗积分: {detail['points_cost']}，剩余: {detail['points_after']}")
            elif action == "failed":
                lines.append(f"🔴 服务器 {server_id}: {reason}")
                if exp_date:
                    lines.append(f"   到期时间: {exp_date}")
                if days_left > 0:
                    lines.append(f"   剩余天数: {days_left} 天")
            else:
                lines.append(f"⚪ 服务器 {server_id}: {reason}")
                if exp_date:
                    lines.append(f"   到期时间: {exp_date}")
        
        return "\n".join(lines)
