"""
飞书云空间 - 获取文件夹中的文件清单

API 文档: https://open.feishu.cn/document/server-docs/docs/drive-v1/folder/list
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import json
import lark_oapi as lark
from lark_oapi.api.drive.v1 import *


def list_files(
    app_id: str,
    app_secret: str,
    parent_token: str = None,
    order_by: str = "EditedTime",
    direction: str = "DESC",
    page_size: int = 50
):
    """
    获取文件夹中的文件清单

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        parent_token: 父文件夹 token（可选，不填则获取根目录）
        order_by: 排序字段，可选值：CreatedTime、EditedTime、ModifiedTime、Size
        direction: 排序方向，可选值：ASC（升序）、DESC（降序）
        page_size: 每页数量，范围 1-100

    Returns:
        dict: 文件列表数据，包含 files 和 page_token
    """
    # 创建 client，直接配置 app_id 和 app_secret
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 构造请求对象
    request_builder = ListFileRequest.builder() \
        .order_by(order_by) \
        .direction(direction) \
        .page_size(page_size)

    # 如果指定了父文件夹，添加到请求中
    if parent_token:
        request_builder.parent_token(parent_token)

    request = request_builder.build()

    # 发起请求
    response: ListFileResponse = client.drive.v1.file.list(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.file.list failed, code: {response.code}, msg: {response.msg}, "
            f"log_id: {response.get_log_id()}, resp: \n"
            f"{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}"
        )
        return None

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))
    return response.data


def main():
    """使用示例"""
    # 配置应用凭据
    app_id = "cli_a98322b338ed5013"
    app_secret = "NWd2p5HIvmp7VsxRLpgvBfODcFt1d6py"

    # 获取文件列表
    result = list_files(
        app_id=app_id,
        app_secret=app_secret,
        order_by="EditedTime",
        direction="DESC",
        page_size=10
    )

    if result:
        print("✅ 文件列表获取成功！")
        if result.files:
            print(f"\n📁 找到 {len(result.files)} 个文件/文件夹:")
            for item in result.files[:5]:  # 只显示前5个
                name = item.name if hasattr(item, 'name') else '未命名'
                token = item.token if hasattr(item, 'token') else 'N/A'
                print(f"  - {name} (token: {token[:20]}...)")
        else:
            print("  文件夹为空")
    else:
        print("❌ 文件列表获取失败")


if __name__ == "__main__":
    main()
