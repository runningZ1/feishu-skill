"""
飞书 CLI - 云空间命令模块
"""

import argparse
import json
import sys
from typing import Optional

# 这里使用 lark_oapi SDK
import lark_oapi as lark
from lark_oapi.api.drive.v1 import *

from ..config import get_config


def list_files(
    app_id: str,
    app_secret: str,
    parent_token: Optional[str] = None,
    order_by: str = "EditedTime",
    direction: str = "DESC",
    page_size: int = 50
) -> Optional[dict]:
    """
    获取文件夹中的文件清单

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        parent_token: 父文件夹 token
        order_by: 排序字段
        direction: 排序方向
        page_size: 每页数量

    Returns:
        dict: 文件列表数据
    """
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    request_builder = ListFileRequest.builder() \
        .order_by(order_by) \
        .direction(direction) \
        .page_size(page_size)

    if parent_token:
        request_builder.parent_token(parent_token)

    request = request_builder.build()
    response: ListFileResponse = client.drive.v1.file.list(request)

    if not response.success():
        print(f"❌ 获取失败: {response.msg}")
        return None

    return response.data


def create_folder(
    app_id: str,
    app_secret: str,
    folder_name: str,
    parent_token: Optional[str] = None
) -> Optional[dict]:
    """
    创建文件夹

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        folder_name: 文件夹名称
        parent_token: 父文件夹 token

    Returns:
        dict: 创建的文件夹信息
    """
    # 根目录 token（如未指定 parent_token）
    ROOT_FOLDER_TOKEN = "nodcnepxRXKIeBfFFprTKnXa6Rf"
    target_token = parent_token if parent_token else ROOT_FOLDER_TOKEN

    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    request = CreateFolderFileRequest.builder() \
        .request_body(CreateFolderFileRequestBody.builder()
            .name(folder_name)
            .folder_token(target_token)
            .build()) \
        .build()

    response: CreateFolderFileResponse = client.drive.v1.file.create_folder(request)

    if not response.success():
        print(f"❌ 创建失败: {response.msg}")
        return None

    return response.data


def cmd_list(args):
    """处理 list 命令"""
    config = get_config()

    if not config.validate_credentials():
        return 1

    result = list_files(
        app_id=config.app_id,
        app_secret=config.app_secret,
        parent_token=args.parent_token,
        order_by=args.order_by,
        direction=args.direction,
        page_size=args.limit
    )

    if result and result.files:
        print(f"✅ 找到 {len(result.files)} 个文件/文件夹:\n")
        for item in result.files[:args.limit]:
            name = item.name if hasattr(item, 'name') else '未命名'
            token = item.token if hasattr(item, 'token') else 'N/A'
            file_type = "📁 文件夹" if hasattr(item, 'type') and item.type == 'folder' else "📄 文件"
            print(f"  {file_type} {name}")
            print(f"    Token: {token[:30]}...")
        return 0
    else:
        print("❌ 获取失败或文件夹为空")
        return 1


def cmd_create_folder(args):
    """处理 create-folder 命令"""
    config = get_config()

    if not config.validate_credentials():
        return 1

    result = create_folder(
        app_id=config.app_id,
        app_secret=config.app_secret,
        folder_name=args.name,
        parent_token=args.parent_token
    )

    if result:
        print(f"✅ 文件夹创建成功！")
        print(f"  名称: {args.name}")
        print(f"  Token: {result.token}")
        print(f"  链接: {result.url}")
        return 0
    else:
        print("❌ 文件夹创建失败")
        return 1


def build_parser(subparsers):
    """构建云空间命令的子解析器"""
    drive_parser = subparsers.add_parser('drive', help='云空间操作')

    # 子命令
    drive_subparsers = drive_parser.add_subparsers(dest='command', help='可用命令')

    # list 命令
    list_parser = drive_subparsers.add_parser('list', help='获取文件列表')
    list_parser.add_argument('--parent-token', '-p', help='父文件夹 token')
    list_parser.add_argument('--order-by', '-o', default='EditedTime',
                            choices=['CreatedTime', 'EditedTime', 'ModifiedTime', 'Size'],
                            help='排序字段')
    list_parser.add_argument('--direction', '-d', default='DESC',
                            choices=['ASC', 'DESC'],
                            help='排序方向')
    list_parser.add_argument('--limit', '-l', type=int, default=20,
                            help='显示数量')
    list_parser.set_defaults(func=cmd_list)

    # create-folder 命令
    create_folder_parser = drive_subparsers.add_parser('create-folder', help='创建文件夹')
    create_folder_parser.add_argument('name', help='文件夹名称')
    create_folder_parser.add_argument('--parent-token', '-p', help='父文件夹 token')
    create_folder_parser.set_defaults(func=cmd_create_folder)
