"""
飞书文档 - 获取文档纯文本内容

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/raw_content
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


def get_document_raw_content(
    app_id: str,
    app_secret: str,
    document_id: str,
    lang: int = 0
):
    """
    获取文档纯文本内容

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        lang: 提及用户(@用户)的文本语言，可选值：
            - 0: 默认名称，示例：@张敏
            - 1: 英文名称，示例：@Min Zhang
            - 2: 日文名称（暂未支持）

    Returns:
        dict: 包含文档纯文本内容的字典
    """
    # 获取 access_token
    access_token = get_tenant_access_token(app_id, app_secret)

    # 构造请求
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/raw_content"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {"lang": lang}

    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 获取失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def main():
    """使用示例"""
    # 配置应用凭据
    app_id = "cli_a98322b338ed5013"
    app_secret = "NWd2p5HIvmp7VsxRLpgvBfODcFt1d6py"

    # 示例：获取文档纯文本内容
    result = get_document_raw_content(
        app_id=app_id,
        app_secret=app_secret,
        document_id="YO0zd1KKYoIEQnxSOgMcKpMwnhg"  # 文档 ID
    )

    if result:
        print("✅ 文档纯文本内容获取成功！")
        content = result.get("content", "")
        print(f"内容长度: {len(content)} 字符")
        print(f"内容预览: {content[:100] if len(content) > 100 else content}...")
    else:
        print("❌ 文档纯文本内容获取失败")


if __name__ == "__main__":
    main()
