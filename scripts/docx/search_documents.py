"""
飞书 - 搜索文档

注意：此功能需要应用有搜索权限，且搜索范围取决于应用配置
"""

import argparse
import os
import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from feishu_cli.config import get_config
except ImportError:
    from _utils import get_config


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    response = requests.post(url, json={"app_id": app_id, "app_secret": app_secret})
    data = response.json()
    if data.get("code") != 0:
        return None
    return data.get("tenant_access_token")


def search_documents(app_id: str, app_secret: str, query: str = ""):
    access_token = get_tenant_access_token(app_id, app_secret)
    if not access_token:
        return None

    # 使用搜索 API
    url = "https://open.feishu.cn/open-apis/search/v2/message"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    body = {"query": query, "search_type": "doc", "page_size": 10}

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        print(f"❌ 搜索失败: HTTP {response.status_code}")
        return None

    result = response.json()
    if result.get("code") != 0:
        print(f"❌ 搜索失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def main():
    parser = argparse.ArgumentParser(
        description="搜索飞书文档",
        epilog="注意：此功能需要应用有搜索权限"
    )
    parser.add_argument("--query", "-q", default="", help="搜索关键词（留空获取最近文档）")
    args = parser.parse_args()

    config = get_config()
    if not config.validate_credentials():
        sys.exit(1)

    print(f"🔍 正在搜索: {args.query or '全部'}...")

    result = search_documents(config.app_id, config.app_secret, args.query)

    if result and result.get("items"):
        items = result.get("items", [])
        print(f"✅ 找到 {len(items)} 个文档")
        for item in items[:5]:
            print(f"  - {item.get('title', '无标题')}: {item.get('document_id', '')}")
        sys.exit(0)
    else:
        print("❌ 未找到文档或搜索失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
