"""
飞书云空间 - 上传素材

API 文档: https://open.feishu.cn/document/server-docs/docs/drive-v1/media/upload_all
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import json
import os
import lark_oapi as lark
from lark_oapi.api.drive.v1 import *


def upload_media(
    app_id: str,
    app_secret: str,
    file_path: str,
    parent_type: str,
    parent_node: str,
    file_name: str = None,
    size: int = None,
    checksum: str = None,
    extra: str = None
):
    """
    上传素材到云文档

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        file_path: 本地文件路径
        parent_type: 上传点类型，可选值：
            - docx_image: 新版文档图片
            - docx_file: 新版文档文件
            - doc_image: 旧版文档图片
            - doc_file: 旧版文档文件
            - sheet_image: 表格图片
            - sheet_file: 表格文件
            - bitable_image: 多维表格图片
            - bitable_file: 多维表格文件
        parent_node: 上传点 token
            - 对于 docx_image/docx_file: 文档块的 block_id
            - 对于 sheet_image/sheet_file: 表格的 spreadsheet_token
            - 对于 bitable_image/bitable_file: 多维表格的 app_token
        file_name: 文件名（可选，默认使用文件原始名称）
        size: 文件大小（字节，可选，默认自动获取）
        checksum: Adler-32 校验和（可选）
        extra: 额外参数（可选，JSON 字符串格式）

    Returns:
        dict: 包含 file_token 的上传结果
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        lark.logger.error(f"文件不存在: {file_path}")
        return None

    # 获取文件信息
    if file_name is None:
        file_name = os.path.basename(file_path)

    if size is None:
        size = os.path.getsize(file_path)

    # 检查文件大小限制 (20MB)
    max_size = 20 * 1024 * 1024  # 20MB
    if size > max_size:
        lark.logger.error(f"文件大小超过限制: {size} > {max_size}，请使用分片上传")
        return None

    # 创建 client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 读取文件内容
    with open(file_path, 'rb') as f:
        file_content = f.read()

    # 更新文件大小为实际读取的大小
    actual_size = len(file_content)
    if actual_size != size:
        lark.logger.warning(f"文件大小修正: {size} -> {actual_size}")
        size = actual_size

    # 构造请求体
    body_builder = UploadAllMediaRequestBody.builder() \
        .file_name(file_name) \
        .parent_type(parent_type) \
        .parent_node(parent_node) \
        .size(size) \
        .file(file_content)

    # 添加可选参数
    if checksum:
        body_builder.checksum(checksum)
    if extra:
        body_builder.extra(extra)

    # 构造请求对象
    request = UploadAllMediaRequest.builder().request_body(body_builder.build()).build()

    # 发起请求
    response: UploadAllMediaResponse = client.drive.v1.media.upload_all(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.media.upload_all failed, code: {response.code}, msg: {response.msg}, "
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

    # 示例 1: 上传图片到新版文档
    # 注意: 需要先创建文档或获取已有的 block_id
    # result = upload_media(
    #     app_id=app_id,
    #     app_secret=app_secret,
    #     file_path="test_image.jpg",
    #     parent_type="docx_image",
    #     parent_node="doxcnXXXXXXXXXXXXXXXXXX"  # 文档块的 block_id
    # )

    # 示例 2: 上传文件到表格
    # result = upload_media(
    #     app_id=app_id,
    #     app_secret=app_secret,
    #     file_path="test_file.pdf",
    #     parent_type="sheet_file",
    #     parent_node="suXXXXXXXXXXXXXXXXXX"  # 表格的 spreadsheet_token
    # )

    # 示例 3: 上传图片到多维表格
    # result = upload_media(
    #     app_id=app_id,
    #     app_secret=app_secret,
    #     file_path="avatar.png",
    #     parent_type="bitable_image",
    #     parent_node="bascnXXXXXXXXXXXXXXXXXX"  # 多维表格的 app_token
    # )

    print("📝 素材上传脚本已准备就绪")
    print("\n使用说明:")
    print("1. 取消上面的示例代码注释")
    print("2. 修改 file_path 为实际文件路径")
    print("3. 修改 parent_type 为目标文档类型")
    print("4. 修改 parent_node 为目标 token:")
    print("   - docx_image/docx_file: 文档块的 block_id")
    print("   - sheet_image/sheet_file: 表格的 spreadsheet_token")
    print("   - bitable_image/bitable_file: 多维表格的 app_token")
    print("\n上传点类型 (parent_type):")
    print("- docx_image: 新版文档图片")
    print("- docx_file: 新版文档文件")
    print("- doc_image: 旧版文档图片")
    print("- doc_file: 旧版文档文件")
    print("- sheet_image: 表格图片")
    print("- sheet_file: 表格文件")
    print("- bitable_image: 多维表格图片")
    print("- bitable_file: 多维表格文件")


if __name__ == "__main__":
    main()
