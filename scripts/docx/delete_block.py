"""
飞书文档 - 删除块

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/batch_delete
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


def delete_block(app_id: str, app_secret: str, document_id: str, block_id: str):
    """删除块"""
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return True

    try:
        result = response.json()
        if result.get("code") != 0:
            print(f"❌ 删除失败: {result.get('code')} - {result.get('msg')}")
            return False
    except:
        pass

    return False


def main():
    parser = argparse.ArgumentParser(description="删除文档块")
    parser.add_argument("--document-id", "-d", required=True, help="文档 ID")
    parser.add_argument("--block-id", "-b", required=True, help="要删除的块 ID")
    parser.add_argument("--yes", "-y", action="store_true", help="跳过确认")
    args = parser.parse_args()

    config = get_config()
    if not config.validate_credentials():
        sys.exit(1)

    if not args.yes:
        print(f"⚠️  即将删除块: {args.block_id}")
        confirm = input("确认删除？(yes/no): ")
        if confirm.lower() not in ["yes", "y"]:
            print("❌ 取消删除")
            sys.exit(1)

    result = delete_block(config.app_id, config.app_secret, args.document_id, args.block_id)
    if result:
        print("✅ 块删除成功")
        sys.exit(0)
    else:
        print("❌ 块删除失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
