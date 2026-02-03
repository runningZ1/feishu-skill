"""
飞书文档 - 更新块的内容

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/patch
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


def update_text_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str,
    text: str
) -> dict:
    """
    更新文本块的内容

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 块 ID
        text: 新的文本内容

    Returns:
        dict: 更新结果
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 更新文本块的数据结构（不包含 block_type，因为更新时不可变）
    body = {
        "text": {
            "elements": [
                {
                    "text_run": {
                        "content": text
                    }
                }
            ]
        }
    }

    response = requests.patch(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 更新失败: {result.get('code')} - {result.get('msg')}")
        print(f"详细信息: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return None

    return result.get("data")


def update_heading_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str,
    text: str,
    level: int = 1
) -> dict:
    """
    更新标题块的内容

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 块 ID
        text: 新的标题内容
        level: 标题级别（1-3）

    Returns:
        dict: 更新结果
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 标题块类型映射
    heading_types = {1: 3, 2: 4, 3: 5}
    block_type = heading_types.get(level, 3)

    heading_key = "heading1" if level == 1 else "heading2" if level == 2 else "heading3"

    body = {
        heading_key: {
            "elements": [
                {
                    "text_run": {
                        "content": text
                    }
                }
            ]
        }
    }

    response = requests.patch(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 更新失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def main():
    """使用示例"""
    # 配置应用凭据
    app_id = "cli_a98322b338ed5013"
    app_secret = "NWd2p5HIvmp7VsxRLpgvBfODcFt1d6py"

    # 文档信息 - 使用测试文档
    document_id = "Uy82weEeqininYki5KWcpnuGnIb"

    # 首先获取文档块列表，找到可更新的块
    print("📋 正在获取文档块列表...")
    from get_document_blocks import get_document_blocks

    blocks = get_document_blocks(app_id, app_secret, document_id)
    if not blocks:
        print("❌ 无法获取文档块")
        return

    # 找到第一个文本块进行更新测试
    text_block_id = None
    heading_block_id = None

    for item in blocks.get("items", []):
        block_type = item.get("block_type")
        if block_type == 2 and not text_block_id:  # 文本块
            text_block_id = item.get("block_id")
        elif block_type in [3, 4, 5] and not heading_block_id:  # 标题块
            heading_block_id = item.get("block_id")

    print(f"\n📝 正在更新块...\n")

    success_count = 0

    # 更新文本块
    if text_block_id:
        result = update_text_block(
            app_id=app_id,
            app_secret=app_secret,
            document_id=document_id,
            block_id=text_block_id,
            text="🔄 这是更新后的文本内容 - " + json.dumps({"timestamp": "2024-01-01"}, ensure_ascii=False)
        )
        if result:
            success_count += 1
            print(f"✅ 文本块更新成功 (block_id: {text_block_id})")
        else:
            print(f"❌ 文本块更新失败 (block_id: {text_block_id})")

    # 更新标题块
    if heading_block_id:
        result = update_heading_block(
            app_id=app_id,
            app_secret=app_secret,
            document_id=document_id,
            block_id=heading_block_id,
            text="🔄 更新后的标题",
            level=2
        )
        if result:
            success_count += 1
            print(f"✅ 标题块更新成功 (block_id: {heading_block_id})")
        else:
            print(f"❌ 标题块更新失败 (block_id: {heading_block_id})")

    print(f"\n🎉 更新完成！成功更新 {success_count} 个块")
    print(f"📄 文档链接: https://my.feishu.cn/docx/{document_id}")


if __name__ == "__main__":
    main()
