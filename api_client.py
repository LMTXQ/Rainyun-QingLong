import logging
import time
import requests

logger = logging.getLogger(__name__)


class RainyunAPIError(Exception):
    """雨云 API 异常"""
    pass


class RainyunAPI:
    """雨云 API 客户端"""
    
    def __init__(self, api_key: str, config: dict):
        if not api_key:
            raise ValueError("API Key 不能为空")
        
        self.api_key = api_key
        self.config = config
        self.base_url = config.get("api_base_url", "https://api.v2.rainyun.com")
        self.timeout = config.get("api_request_timeout", 10)
        self.max_retries = config.get("api_max_retries", 3)
        self.retry_delay = config.get("api_retry_delay", 2)
        
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "User-Agent": "Rainyun-QingLong-Script/2.0"
        }
        
        logger.info("🔑 API 客户端初始化成功")
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """发送 API 请求（带重试机制）"""
        url = f"{self.base_url}{endpoint}"
        last_error = None
        
        logger.info(f"📡 API 请求: {method} {endpoint}")
        
        for attempt in range(1, self.max_retries + 1):
            try:
                if method.upper() == "GET":
                    response = requests.get(url, headers=self.headers, timeout=self.timeout)
                else:
                    response = requests.post(url, headers=self.headers, json=data, timeout=self.timeout)
                
                # 解析 JSON
                try:
                    result = response.json()
                except ValueError:
                    response.raise_for_status()
                    raise RainyunAPIError(f"响应不是有效 JSON: {response.text[:200]}")
                
                # 检查业务状态码
                api_code = result.get("code")
                api_message = result.get("message", "未知错误")
                
                if api_code != 200:
                    logger.error(f"   API 返回错误 [{api_code}]: {api_message}")
                    raise RainyunAPIError(f"API 错误 [{api_code}]: {api_message}")
                
                logger.info(f"   ✓ API 请求成功")
                return result.get("data", {})
                
            except requests.RequestException as e:
                last_error = e
                if attempt < self.max_retries:
                    logger.warning(f"   请求失败 (第 {attempt} 次): {e}，{self.retry_delay}秒后重试...")
                    time.sleep(self.retry_delay)
                continue
        
        logger.error(f"   网络请求失败 (已重试 {self.max_retries} 次): {last_error}")
        raise RainyunAPIError(f"网络请求失败: {last_error}")
    
    def get_user_points(self) -> int:
        """获取用户积分余额"""
        data = self._request("GET", "/user/")
        points = data.get("Points", 0)
        logger.info(f"   当前积分: {points}")
        return points
    
    def get_server_list(self, product_type: str = "rgs") -> list:
        """获取服务器 ID 列表"""
        data = self._request("GET", f"/product/id_list?product_type={product_type}")
        server_ids = data.get(product_type, [])
        logger.info(f"   找到 {len(server_ids)} 台{product_type}服务器")
        return server_ids
    
    def get_server_detail(self, server_id: int) -> dict:
        """获取服务器详细信息"""
        logger.info(f"   查询服务器 {server_id} 详情...")
        return self._request("GET", f"/product/rgs/{server_id}/")
    
    def renew_server(self, server_id: int, days: int = 7) -> dict:
        """使用积分续费服务器"""
        data = {
            "duration_day": days,
            "product_id": server_id,
            "product_type": "rgs"
        }
        logger.info(f"   正在续费服务器 {server_id}（{days} 天）...")
        return self._request("POST", "/product/point_renew", data)
    
    def test_connection(self) -> bool:
        """测试 API 连接"""
        try:
            self.get_user_points()
            return True
        except RainyunAPIError:
            return False
