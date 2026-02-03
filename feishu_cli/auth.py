"""
飞书 CLI - 认证模块
"""

import requests
from typing import Optional


def get_tenant_access_token(app_id: str, app_secret: str) -> Optional[str]:
    """
    获取 tenant_access_token

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥

    Returns:
        str: tenant_access_token，失败返回 None
    """
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

    try:
        response = requests.post(
            url,
            json={"app_id": app_id, "app_secret": app_secret},
            timeout=10
        )
        result = response.json()

        if result.get("code") != 0:
            print(f"❌ 获取 token 失败: {result.get('msg')}")
            return None

        return result.get("tenant_access_token")
    except requests.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return None


def get_access_token(app_id: str, app_secret: str) -> Optional[str]:
    """
    获取 access_token（别名，与 get_tenant_access_token 相同）

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥

    Returns:
        str: tenant_access_token，失败返回 None
    """
    return get_tenant_access_token(app_id, app_secret)
