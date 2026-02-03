"""
飞书脚本通用工具
"""

import os


def get_config():
    """获取配置（从环境变量或 .env 文件）"""
    class SimpleConfig:
        @property
        def app_id(self):
            return os.environ.get("FEISHU_APP_ID") or os.environ.get("app_id")

        @property
        def app_secret(self):
            return os.environ.get("FEISHU_APP_SECRET") or os.environ.get("app_secret")

        def validate_credentials(self):
            if not self.app_id:
                print("❌ 未配置 app_id，请设置环境变量 FEISHU_APP_ID 或在 .env 文件中配置")
                return False
            if not self.app_secret:
                print("❌ 未配置 app_secret，请设置环境变量 FEISHU_APP_SECRET 或在 .env 文件中配置")
                return False
            return True
    return SimpleConfig()


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """获取 tenant_access_token"""
    import requests
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    response = requests.post(url, json={"app_id": app_id, "app_secret": app_secret})
    data = response.json()
    if data.get("code") != 0:
        print(f"❌ 获取 token 失败: {data.get('msg')}")
        return None
    return data.get("tenant_access_token")
