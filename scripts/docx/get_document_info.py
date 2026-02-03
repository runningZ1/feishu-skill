"""
飞书文档 - 获取文档基本信息

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/get
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import json
import lark_oapi as lark
from lark_oapi.api.docx.v1 import *


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
    # 创建 client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 构造请求对象
    request = GetDocumentRequest.builder().document_id(document_id).build()

    # 发起请求
    response: GetDocumentResponse = client.docx.v1.document.get(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document.get failed, code: {response.code}, msg: {response.msg}, "
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

    # 示例：获取文档信息
    # result = get_document(
    #     app_id=app_id,
    #     app_secret=app_secret,
    #     document_id="YO0zd1KKYoIEQnxSOgMcKpMwnhg"  # 文档 ID
    # )

    # 测试：使用刚才创建的文档
    result = get_document(
        app_id=app_id,
        app_secret=app_secret,
        document_id="YO0zd1KKYoIEQnxSOgMcKpMwnhg"
    )

    if result:
        print("✅ 文档信息获取成功！")
        print(f"文档 ID: {result.document.document_id}")
        print(f"标题: {result.document.title}")
        print(f"版本 ID: {result.document.revision_id}")
    else:
        print("❌ 文档信息获取失败")


if __name__ == "__main__":
    main()
