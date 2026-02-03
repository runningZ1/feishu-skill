"""
飞书 CLI - 文档命令模块
"""

import argparse
from typing import Optional

import lark_oapi as lark
from lark_oapi.api.docx.v1 import *

from ..config import get_config


def create_document(
    app_id: str,
    app_secret: str,
    title: str,
    folder_token: Optional[str] = None
) -> Optional[dict]:
    """
    创建飞书文档

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        title: 文档标题
        folder_token: 文件夹 token

    Returns:
        dict: 创建的文档信息
    """
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    body_builder = CreateDocumentRequestBody.builder().title(title)

    if folder_token:
        body_builder.folder_token(folder_token)

    request = CreateDocumentRequest.builder().request_body(body_builder.build()).build()
    response: CreateDocumentResponse = client.docx.v1.document.create(request)

    if not response.success():
        print(f"❌ 创建失败: {response.msg}")
        return None

    return response.data


def cmd_create(args):
    """处理 create 命令"""
    config = get_config()

    if not config.validate_credentials():
        return 1

    result = create_document(
        app_id=config.app_id,
        app_secret=config.app_secret,
        title=args.title,
        folder_token=args.folder_token
    )

    if result:
        doc_id = result.document.document_id
        print(f"✅ 文档创建成功！")
        print(f"  标题: {args.title}")
        print(f"  Document ID: {doc_id}")
        print(f"  链接: https://my.feishu.cn/docx/{doc_id}")
        return 0
    else:
        print("❌ 文档创建失败")
        return 1


def build_parser(subparsers):
    """构建文档命令的子解析器"""
    doc_parser = subparsers.add_parser('doc', help='文档操作')

    # 子命令
    doc_subparsers = doc_parser.add_subparsers(dest='command', help='可用命令')

    # create 命令
    create_parser = doc_subparsers.add_parser('create', help='创建文档')
    create_parser.add_argument('title', help='文档标题')
    create_parser.add_argument('--folder-token', '-f', help='文件夹 token')
    create_parser.set_defaults(func=cmd_create)
