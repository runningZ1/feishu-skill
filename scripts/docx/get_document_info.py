"""
飞书文档 - 获取文档基本信息

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/get
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import argparse
import json
import os
import sys
from pathlib import Path

import lark_oapi as lark
from lark_oapi.api.docx.v1 import *

# 添加项目根目录到路径
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
                if not self.app_id:
                    print("❌ 未配置 app_id")
                    return False
                if not self.app_secret:
                    print("❌ 未配置 app_secret")
                    return False
                return True
        return SimpleConfig()


def get_document(
    app_id: str,
    app_secret: str,
    document_id: str
):
    """
    获取文档基本信息

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID

    Returns:
        dict: 包含文档基本信息的字典
    """
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    request = GetDocumentRequest.builder().document_id(document_id).build()
    response: GetDocumentResponse = client.docx.v1.document.get(request)

    if not response.success():
        print(f"❌ 获取失败: {response.code} - {response.msg}")
        return None

    return response.data


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="获取飞书文档基本信息"
    )
    parser.add_argument("--document-id", "-d", required=True, help="文档 ID")

    args = parser.parse_args()

    config = get_config()

    if not config.validate_credentials():
        sys.exit(1)

    result = get_document(
        app_id=config.app_id,
        app_secret=config.app_secret,
        document_id=args.document_id
    )

    if result:
        print("✅ 文档信息获取成功！")
        print(f"文档 ID: {result.document.document_id}")
        print(f"标题: {result.document.title}")
        print(f"版本 ID: {result.document.revision_id}")
        sys.exit(0)
    else:
        print("❌ 文档信息获取失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
