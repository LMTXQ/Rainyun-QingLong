import json
import logging
import os
import sys
from typing import List

logger = logging.getLogger(__name__)


class Account:
    """账号数据类"""
    
    def __init__(self, username: str, password: str, auto_renew: bool = False, api_key: str = ""):
        self.username = username
        self.password = password
        self.auto_renew = auto_renew
        self.api_key = api_key
    
    def __repr__(self):
        return f"Account(username={self.username}, auto_renew={self.auto_renew}, has_api_key={bool(self.api_key)})"


def parse_accounts() -> List[Account]:
    """
    解析账号配置
    
    支持格式:
    1. [["账号1", "密码1", "true", "api_key1"], ["账号2", "密码2", "false", "api_key2"]]
    2. [["账号1", "密码1", "true"], ["账号2", "密码2"]]  # 不带API Key
    3. [["账号1", "密码1"], ["账号2", "密码2"]]  # 使用全局配置
    
    Returns:
        账号对象列表
    """
    account_str = os.getenv("RAINYUN_ACCOUNT")
    if not account_str:
        logger.error("❌ 未配置 RAINYUN_ACCOUNT 环境变量！")
        logger.error("格式示例:")
        logger.error('  [[\"账号1\",\"密码1\",\"true\",\"api_key1\"],[\"账号2\",\"密码2\",\"false\"]]')
        logger.error("说明:")
        logger.error("  - 第3个参数：是否启用自动续费（true/false）")
        logger.error("  - 第4个参数：API Key（可选，如果不续费可以不填）")
        sys.exit(1)
    
    try:
        # 统一为双引号
        account_str = account_str.replace("'", "\"")
        accounts_raw = json.loads(account_str)
        
        if not isinstance(accounts_raw, list):
            raise ValueError("配置格式错误：必须是列表类型")
        
        accounts = []
        for idx, item in enumerate(accounts_raw, 1):
            if not isinstance(item, list):
                raise ValueError(f"第 {idx} 个账号格式错误：必须是列表")
            
            if len(item) < 2:
                raise ValueError(f"第 {idx} 个账号格式错误：至少需要[账号, 密码]")
            
            username = item[0].strip()
            password = item[1].strip()
            
            if not username or not password:
                raise ValueError(f"第 {idx} 个账号的用户名或密码为空")
            
            # 解析自动续费开关（可选，默认false）
            auto_renew = False
            if len(item) >= 3:
                auto_renew_str = str(item[2]).strip().lower()
                auto_renew = auto_renew_str in ["true", "1", "yes", "on"]
            
            # 解析API Key（可选，默认空字符串）
            api_key = ""
            if len(item) >= 4:
                api_key = item[3].strip()
            
            accounts.append(Account(username, password, auto_renew, api_key))
        
        logger.info("=" * 80)
        logger.info(f"✅ 成功解析 {len(accounts)} 个账号")
        logger.info("-" * 80)
        for idx, acc in enumerate(accounts, 1):
            renew_status = "✅ 开启" if acc.auto_renew else "⏭️  关闭"
            api_status = "✅ 已配置" if acc.api_key else "⚪ 未配置"
            logger.info(f"账号 {idx}: {acc.username}")
            logger.info(f"  自动续费: {renew_status}")
            logger.info(f"  API Key: {api_status}")
            if idx < len(accounts):
                logger.info("-" * 40)
        logger.info("=" * 80)
        
        return accounts
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ RAINYUN_ACCOUNT 格式解析失败: {e}")
        logger.error("请检查格式是否为合法 JSON（注意引号和逗号）")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"❌ 账号配置错误: {e}")
        sys.exit(1)
