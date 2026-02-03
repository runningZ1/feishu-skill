"""
飞书 - 搜索文档

通过搜索功能查找 Wiki 文档的 document_id
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


def search_documents(app_id: str, app_secret: str, query: str = "") -> dict:
    """
    搜索文档

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        query: 搜索关键词

    Returns:
        dict: 搜索结果
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = "https://open.feishu.cn/open-apis/docx/v1/documents/search"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "query": query,
        "page_size": 10
    }

    response = requests.post(url, headers=headers, json=body)

    try:
        result = response.json()
        print(f"状态码: {response.status_code}")

        if result.get("code") != 0:
            print(f"❌ 搜索失败: {result.get('code')} - {result.get('msg')}")
            print(f"详细信息: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return None

        return result.get("data")
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        print(f"原始响应: {response.text}")
        return None


def main():
    """使用示例"""
    # 配置应用凭据
    app_id = "cli_a98322b338ed5013"
    app_secret = "NWd2p5HIvmp7VsxRLpgvBfODcFt1d6py"

    print("🔍 正在搜索文档...")

    # 搜索最近创建的文档
    result = search_documents(app_id, app_secret, "")

    if result and result.get("items"):
        print(f"\n✅ 找到 {len(result.get('items', []))} 个文档\n")

        for idx, item in enumerate(result.get("items", [])[:5], 1):
            title = item.get("title", "无标题")
            doc_id = item.get("document_id", "")
            print(f"{idx}. {title}")
            print(f"   Document ID: {doc_id}")
            print()

        # 使用第一个文档
        if result.get("items"):
            first_doc = result.get("items")[0]
            doc_id = first_doc.get("document_id")
            print("="*50)
            print("📝 可以使用以下 Document ID 创建块:")
            print(f'document_id = "{doc_id}"')
            print(f'block_id = "{doc_id}"')
            print("="*50)
            return doc_id
    else:
        print("❌ 未找到文档")

    return None


if __name__ == "__main__":
    main()
