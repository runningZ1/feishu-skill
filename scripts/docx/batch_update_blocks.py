"""
飞书文档 - 批量更新块

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/batch_update
"""

import argparse
import json
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


def batch_update_blocks(app_id: str, app_secret: str, document_id: str, updates: list):
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/batch_update"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    body = {"requests": updates}

    response = requests.post(url, headers=headers, json=body)

    try:
        result = response.json()
    except:
        print(f"❌ 请求失败: HTTP {response.status_code}")
        return None

    if result.get("code") != 0:
        print(f"❌ 批量更新失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def main():
    parser = argparse.ArgumentParser(
        description="批量更新文档块",
        epilog="注意：此功能需要构造复杂的更新请求体，建议先获取块列表"
    )
    parser.add_argument("--document-id", "-d", required=True, help="文档 ID")
    parser.add_argument("--text", "-t", help="统一更新的文本内容（简化模式）")
    args = parser.parse_args()

    config = get_config()
    if not config.validate_credentials():
        sys.exit(1)

    print("ℹ️  批量更新需要先获取块列表，然后构造更新请求")
    print("ℹ️  简化模式：请先使用 get_document_blocks.py 获取块，然后用 update_block.py 逐个更新")
    print(f"当前文档 ID: {args.document_id}")
    sys.exit(0)


if __name__ == "__main__":
    main()
