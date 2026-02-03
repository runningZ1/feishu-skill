"""
飞书云空间 - 创建文件夹

API 文档: https://open.feishu.cn/document/server-docs/docs/drive-v1/file/create_folder
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import json
import lark_oapi as lark
from lark_oapi.api.drive.v1 import *


# 云空间根目录 token
ROOT_FOLDER_TOKEN = "nodcnepxRXKIeBfFFprTKnXa6Rf"


def create_folder(
    app_id: str,
    app_secret: str,
    folder_name: str,
    parent_token: str = None
):
    """
    创建文件夹

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        folder_name: 文件夹名称
        parent_token: 父文件夹 token（可选，不填则在云空间根目录创建）

    Returns:
        dict: 创建的文件夹信息，包含 token、name 等
    """
    # 创建 client，直接配置 app_id 和 app_secret
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 如果未指定父文件夹，使用根目录
    target_token = parent_token if parent_token else ROOT_FOLDER_TOKEN

    # 构造请求对象
    request = CreateFolderFileRequest.builder() \
        .request_body(CreateFolderFileRequestBody.builder()
            .name(folder_name)
            .folder_token(target_token)
            .build()) \
        .build()

    # 发起请求
    response: CreateFolderFileResponse = client.drive.v1.file.create_folder(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.file.create_folder failed, code: {response.code}, msg: {response.msg}, "
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

    # 创建文件夹
    folder_name = "Test Folder"

    print(f"📁 正在创建文件夹: {folder_name}")
    result = create_folder(
        app_id=app_id,
        app_secret=app_secret,
        folder_name=folder_name,
        parent_token=None  # 不指定则在根目录创建
    )

    if result:
        print("✅ 文件夹创建成功！")
        print(f"  文件夹名称: {folder_name}")
        print(f"  文件夹 Token: {result.token}")
        print(f"  访问链接: {result.url}")
    else:
        print("❌ 文件夹创建失败")


if __name__ == "__main__":
    main()
