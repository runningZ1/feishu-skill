"""
飞书文档 - 获取块的内容

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/get
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


def get_block_content(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str
) -> dict:
    """
    获取块的内容

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 块 ID

    Returns:
        dict: 块的内容
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
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

    # 文档信息
    document_id = "Yfu7dIDBBohlbIxs6QQcj5wXn1d"

    # 首先获取文档块列表，找到可查询的块
    print("📋 正在获取文档块列表...")
    from get_document_blocks import get_document_blocks

    blocks = get_document_blocks(app_id, app_secret, document_id)
    if not blocks:
        print("❌ 无法获取文档块")
        return

    print(f"\n📝 正在获取块内容...\n")

    success_count = 0

    # 获取前几个块的内容
    for idx, item in enumerate(blocks.get("items", [])[:5], 1):
        block_id = item.get("block_id")
        block_type = item.get("block_type")

        result = get_block_content(
            app_id=app_id,
            app_secret=app_secret,
            document_id=document_id,
            block_id=block_id
        )

        if result:
            success_count += 1
            # 提取块的主要内容
            content = ""
            if "text" in result:
                elements = result["text"].get("elements", [])
                if elements:
                    content = elements[0].get("text_run", {}).get("content", "")
            elif "heading1" in result:
                elements = result["heading1"].get("elements", [])
                if elements:
                    content = elements[0].get("text_run", {}).get("content", "")
            elif "heading2" in result:
                elements = result["heading2"].get("elements", [])
                if elements:
                    content = elements[0].get("text_run", {}).get("content", "")
            elif "heading3" in result:
                elements = result["heading3"].get("elements", [])
                if elements:
                    content = elements[0].get("text_run", {}).get("content", "")

            block_type_name = {2: "文本", 3: "标题1", 4: "标题2", 5: "标题3", 7: "有序列表", 8: "无序列表"}.get(block_type, f"类型{block_type}")
            print(f"✅ [{idx}] {block_type_name}块: {content[:50]}...")
        else:
            print(f"❌ [{idx}] 获取失败 (block_id: {block_id})")

    print(f"\n🎉 获取完成！成功获取 {success_count} 个块的内容")
    print(f"📄 文档链接: https://my.feishu.cn/docx/{document_id}")


if __name__ == "__main__":
    main()
