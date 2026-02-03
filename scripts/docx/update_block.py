"""
飞书文档 - 更新块

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/patch
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


def update_text_block(app_id: str, app_secret: str, document_id: str, block_id: str, text: str):
    """更新文本块"""
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    body = {
        "text": {
            "elements": [{"text_run": {"content": text}}]
        }
    }

    response = requests.patch(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 更新失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def main():
    parser = argparse.ArgumentParser(description="更新文档块内容")
    parser.add_argument("--document-id", "-d", required=True, help="文档 ID")
    parser.add_argument("--block-id", "-b", required=True, help="块 ID")
    parser.add_argument("--text", "-t", required=True, help="新文本内容")
    args = parser.parse_args()

    config = get_config()
    if not config.validate_credentials():
        sys.exit(1)

    result = update_text_block(config.app_id, config.app_secret, args.document_id, args.block_id, args.text)
    if result:
        print("✅ 块更新成功")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
