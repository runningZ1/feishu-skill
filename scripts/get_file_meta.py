"""
飞书云空间 - 获取文件元数据

API 文档: https://open.feishu.cn/document/server-docs/docs/drive-v1/meta/batch_query
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import json
import lark_oapi as lark
from lark_oapi.api.drive.v1 import *


def get_file_meta(
    app_id: str,
    app_secret: str,
    file_token: str,
    file_type: str
):
    """
    获取文件元数据

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        file_token: 文件 token
        file_type: 文件类型，可选值：docx、sheet、bitable、file、folder、mindnote、doc、slide、wiki

    Returns:
        dict: 文件元数据信息
    """
    # 创建 client，直接配置 app_id 和 app_secret
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 构造请求对象
    request = BatchQueryMetaRequest.builder() \
        .request_body(MetaRequest.builder()
            .request_docs([RequestDoc.builder()
                .doc_token(file_token)
                .doc_type(file_type)
                .build()])
            .build()) \
        .build()

    # 发起请求
    response: BatchQueryMetaResponse = client.drive.v1.meta.batch_query(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.meta.batch_query failed, code: {response.code}, msg: {response.msg}, "
            f"log_id: {response.get_log_id()}, resp: \n"
            f"{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}"
        )
        return None

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    # 返回第一个文件的元数据
    if response.data and hasattr(response.data, 'metas') and response.data.metas:
        return response.data.metas[0] if len(response.data.metas) > 0 else None

    # 检查失败列表
    if response.data and hasattr(response.data, 'failed_list') and response.data.failed_list:
        failed = response.data.failed_list[0]
        print(f"⚠️ 获取失败: token={failed.token}, code={failed.code}")

    return None


def batch_get_file_meta(
    app_id: str,
    app_secret: str,
    file_list: list
):
    """
    批量获取文件元数据

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        file_list: 文件列表，格式：[{"token": "xxx", "type": "docx"}, ...]

    Returns:
        list: 文件元数据列表
    """
    # 创建 client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 构造请求对象
    request_docs = [
        RequestDoc.builder()
            .doc_token(item["token"])
            .doc_type(item["type"])
            .build()
        for item in file_list
    ]

    request = BatchQueryMetaRequest.builder() \
        .request_body(MetaRequest.builder()
            .request_docs(request_docs)
            .build()) \
        .build()

    # 发起请求
    response: BatchQueryMetaResponse = client.drive.v1.meta.batch_query(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.meta.batch_query failed, code: {response.code}, msg: {response.msg}, "
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

    # 获取单个文件元数据
    # 使用实际存在的文件 token（从 list_files 获取）
    file_token = "K4j3d0kZoo2B9GxkoQvc6MHUnqc"
    file_type = "docx"

    print(f"📄 正在获取文件元数据: {file_token}")
    result = get_file_meta(
        app_id=app_id,
        app_secret=app_secret,
        file_token=file_token,
        file_type=file_type
    )

    if result:
        print("✅ 文件元数据获取成功！")
        print(f"  文件 Token: {result.doc_token if hasattr(result, 'doc_token') else 'N/A'}")
        print(f"  文件标题: {result.title if hasattr(result, 'title') else 'N/A'}")
        print(f"  文件类型: {result.doc_type if hasattr(result, 'doc_type') else 'N/A'}")
        print(f"  所有者 ID: {result.owner_id if hasattr(result, 'owner_id') else 'N/A'}")
        print(f"  创建时间: {result.create_time if hasattr(result, 'create_time') else 'N/A'}")
        print(f"  最后修改时间: {result.latest_modify_time if hasattr(result, 'latest_modify_time') else 'N/A'}")
    else:
        print("❌ 文件元数据获取失败")


if __name__ == "__main__":
    main()
