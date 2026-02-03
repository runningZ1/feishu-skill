"""
飞书文档 - 创建文档

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/create
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import json
import lark_oapi as lark
from lark_oapi.api.docx.v1 import *


def create_document(
    app_id: str,
    app_secret: str,
    title: str,
    folder_token: str = None
):
    """
    创建飞书文档

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        title: 文档标题
        folder_token: 文件夹 token（可选，指定创建位置）

    Returns:
        dict: 包含 document_id 和 index_type 的创建结果
    """
    # 创建 client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 构造请求体
    body_builder = CreateDocumentRequestBody.builder().title(title)

    # 如果指定了文件夹，设置创建位置
    if folder_token:
        # 创建文档时，可以指定父文件夹
        body_builder.folder_token(folder_token)

    # 构造请求对象
    request = CreateDocumentRequest.builder().request_body(body_builder.build()).build()

    # 发起请求
    response: CreateDocumentResponse = client.docx.v1.document.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document.create failed, code: {response.code}, msg: {response.msg}, "
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

    # 示例 1: 创建普通文档
    # result = create_document(
    #     app_id=app_id,
    #     app_secret=app_secret,
    #     title="测试文档"
    # )

    # 示例 2: 在指定文件夹中创建文档
    # result = create_document(
    #     app_id=app_id,
    #     app_secret=app_secret,
    #     title="文件夹中的测试文档",
    #     folder_token="FdElfqxkalxSqBdv7N2cjxFunOc"  # 文件夹 token
    # )

    print("📝 文档创建脚本已准备就绪")
    print("\n使用说明:")
    print("1. 取消上面的示例代码注释")
    print("2. 修改 title 为想要的文档标题")
    print("3. 可选: 添加 folder_token 来指定创建位置")


if __name__ == "__main__":
    main()
