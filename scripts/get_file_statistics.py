"""
飞书云空间 - 获取文件统计信息

API 文档: https://open.feishu.cn/document/server-docs/docs/drive-v1/file/get
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import json
import lark_oapi as lark
from lark_oapi.api.drive.v1 import *


def get_file_statistics(
    app_id: str,
    app_secret: str,
    file_token: str,
    file_type: str
):
    """
    获取文件统计信息

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        file_token: 文件 token
        file_type: 文件类型，可选值：docx、sheet、bitable、file、folder、mindnote、doc、slide、wiki

    Returns:
        dict: 文件统计信息，包含访问量、浏览量、编辑者数量等
    """
    # 创建 client，直接配置 app_id 和 app_secret
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 构造请求对象
    request = GetFileStatisticsRequest.builder() \
        .file_token(file_token) \
        .file_type(file_type) \
        .build()

    # 发起请求
    response: GetFileStatisticsResponse = client.drive.v1.file_statistics.get(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.file_statistics.get failed, code: {response.code}, msg: {response.msg}, "
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

    # 获取文件统计信息
    # 使用实际存在的文件 token（从 list_files 获取）
    file_token = "K4j3d0kZoo2B9GxkoQvc6MHUnqc"
    file_type = "docx"

    print(f"📊 正在获取文件统计信息: {file_token}")
    result = get_file_statistics(
        app_id=app_id,
        app_secret=app_secret,
        file_token=file_token,
        file_type=file_type
    )

    if result:
        print("✅ 文件统计信息获取成功！")
        if hasattr(result, 'statistics') and result.statistics:
            stats = result.statistics
            print(f"  独立访客数 (UV): {stats.uv}")
            print(f"  页面浏览量 (PV): {stats.pv}")
            print(f"  点赞数: {stats.like_count}")
            print(f"  今日独立访客数: {stats.uv_today}")
            print(f"  今日页面浏览量: {stats.pv_today}")
            print(f"  今日点赞数: {stats.like_count_today}")
        print(f"  文件 Token: {result.file_token}")
        print(f"  文件类型: {result.file_type}")
    else:
        print("❌ 文件统计信息获取失败")


if __name__ == "__main__":
    main()
