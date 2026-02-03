"""
飞书文档 - 删除块

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/batch_delete
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


def delete_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str
) -> dict:
    """
    删除单个块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 要删除的块 ID

    Returns:
        dict: 删除结果
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.delete(url, headers=headers)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 删除失败: {result.get('code')} - {result.get('msg')}")
        print(f"详细信息: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return None

    return result.get("data")


def batch_delete_blocks(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_ids: list
) -> dict:
    """
    批量删除块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_ids: 要删除的块 ID 列表

    Returns:
        dict: 删除结果
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/batch_delete"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "block_ids": block_ids
    }

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 批量删除失败: {result.get('code')} - {result.get('msg')}")
        print(f"详细信息: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return None

    return result.get("data")


def main():
    """使用示例"""
    # 配置应用凭据
    app_id = "cli_a98322b338ed5013"
    app_secret = "NWd2p5HIvmp7VsxRLpgvBfODcFt1d6py"

    # 文档信息 - 使用测试文档
    document_id = "Uy82weEeqininYki5KWcpnuGnIb"

    # 获取文档中的块列表，选择最后几个块进行删除测试
    print("📋 正在获取文档块列表...")
    from get_document_blocks import get_document_blocks

    blocks = get_document_blocks(app_id, app_secret, document_id)
    if not blocks:
        print("❌ 无法获取文档块")
        return

    items = blocks.get("items", [])
    if len(items) < 2:
        print("❌ 文档中没有足够的块进行测试")
        return

    # 使用最后两个块进行删除测试
    test_blocks = [items[-1].get("block_id"), items[-2].get("block_id")]
    print(f"\n🗑️ 正在删除 {len(test_blocks)} 个块...\n")
    for block_id in test_blocks:
        print(f"待删除: {block_id[:12]}...")

    # 测试批量删除
    result = batch_delete_blocks(
        app_id=app_id,
        app_secret=app_secret,
        document_id=document_id,
        block_ids=test_blocks
    )

    if result:
        # 检查每个块是否删除成功
        for block_id in test_blocks:
            print(f"✅ 块 {block_id[:12]}... 已删除")

        print(f"\n🎉 删除完成！成功删除 {len(test_blocks)} 个块")
        print(f"📄 文档链接: https://my.feishu.cn/docx/{document_id}")
    else:
        print(f"\n❌ 批量删除失败")


if __name__ == "__main__":
    main()
