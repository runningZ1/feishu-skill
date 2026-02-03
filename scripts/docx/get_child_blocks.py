"""
飞书文档 - 获取所有子块

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/get-2
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
    def get_config():
        class SimpleConfig:
            @property
            def app_id(self):
                return os.environ.get("FEISHU_APP_ID") or os.environ.get("app_id")
            @property
            def app_secret(self):
                return os.environ.get("FEISHU_APP_SECRET") or os.environ.get("app_secret")
            def validate_credentials(self):
                if not self.app_id or not self.app_secret:
                    return False
                return True
        return SimpleConfig()


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    response = requests.post(url, json={"app_id": app_id, "app_secret": app_secret})
    return response.json().get("tenant_access_token")


def get_child_blocks(app_id: str, app_secret: str, document_id: str, block_id: str, page_size: int = 100):
    access_token = get_tenant_access_token(app_id, app_secret)
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    params = {"page_size": page_size}
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    if result.get("code") != 0:
        print(f"❌ 获取失败: {result.get('code')} - {result.get('msg')}")
        return None
    return result.get("data")


def main():
    parser = argparse.ArgumentParser(description="获取块的子块")
    parser.add_argument("--document-id", "-d", required=True, help="文档 ID")
    parser.add_argument("--block-id", "-b", required=True, help="父块 ID")
    args = parser.parse_args()

    config = get_config()
    if not config.validate_credentials():
        sys.exit(1)

    result = get_child_blocks(config.app_id, config.app_secret, args.document_id, args.block_id)
    if result and result.get("items"):
        items = result.get("items", [])
        print(f"✅ 找到 {len(items)} 个子块")
        for item in items:
            print(f"  - {item.get('block_id', '')}: {item.get('block_type', '')}")
        sys.exit(0)
    else:
        print("❌ 获取失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
