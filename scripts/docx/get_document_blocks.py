"""
飞书文档 - 获取文档所有块

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/list
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import json
import requests


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    response = requests.post(
        url,
        json={"app_id": app_id, "app_secret": app_secret}
    )
    return response.json().get("tenant_access_token")


def get_document_blocks(
    app_id: str,
    app_secret: str,
    document_id: str,
    page_size: int = 500,
    document_revision_id: int = -1
):
    """
    获取文档所有块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        page_size: 分页大小，默认 500，最大 500
        document_revision_id: 文档版本 ID，-1 表示最新版本

    Returns:
        dict: 包含文档块列表的字典
    """
    # 获取 access_token
    access_token = get_tenant_access_token(app_id, app_secret)

    # 构造请求 - 使用正确的 API 端点
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "page_size": page_size,
        "document_revision_id": document_revision_id
    }

    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 获取失败: {result.get('code')} - {result.get('msg')}")
        print(f"详细信息: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return None

    return result.get("data")


def main():
    """使用示例"""
    # 配置应用凭据
    app_id = "cli_a98322b338ed5013"
    app_secret = "NWd2p5HIvmp7VsxRLpgvBfODcFt1d6py"

    # 示例：获取文档所有块
    result = get_document_blocks(
        app_id=app_id,
        app_secret=app_secret,
        document_id="YO0zd1KKYoIEQnxSOgMcKpMwnhg"  # 文档 ID
    )

    if result and result.get("items"):
        print("✅ 文档块列表获取成功！")
        items = result.get("items", [])
        print(f"找到 {len(items)} 个块")
        for item in items[:5]:  # 只显示前5个
            block_id = item.get("block_id", "")
            block_type = item.get("block_type", "")
            print(f"  - Block ID: {block_id}, Type: {block_type}")
    else:
        print("❌ 文档块列表获取失败")


if __name__ == "__main__":
    main()
