"""
飞书文档 - 批量更新块的内容

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/batch_update
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


def batch_update_blocks(
    app_id: str,
    app_secret: str,
    document_id: str,
    updates: list
) -> dict:
    """
    批量更新块的内容

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        updates: 更新列表，每个元素包含 block_id 和要更新的内容
                 格式: [{"block_id": "xxx", "text": {"elements": [...]}}]

    Returns:
        dict: 更新结果
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/batch_update"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 批量更新请求体
    body = {
        "requests": updates
    }

    response = requests.post(url, headers=headers, json=body)

    # 调试：打印原始响应
    print(f"状态码: {response.status_code}")
    print(f"原始响应: {response.text[:500]}")

    try:
        result = response.json()
    except Exception as e:
        print(f"❌ JSON 解析失败: {e}")
        return None

    if result.get("code") != 0:
        print(f"❌ 批量更新失败: {result.get('code')} - {result.get('msg')}")
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

    # 首先获取文档块列表，找到可更新的块
    print("📋 正在获取文档块列表...")
    from get_document_blocks import get_document_blocks

    blocks = get_document_blocks(app_id, app_secret, document_id)
    if not blocks:
        print("❌ 无法获取文档块")
        return

    # 准备批量更新数据（更新前 3 个文本块）
    updates = []
    block_ids = []

    for item in blocks.get("items", []):
        if item.get("block_type") == 2:  # 文本块
            block_id = item.get("block_id")
            block_ids.append(block_id)
            # 构造更新请求
            updates.append({
                "block_id": block_id,
                "text": {
                    "elements": [
                        {
                            "text_run": {
                                "content": f"🔄 批量更新内容 - {block_id[:8]}"
                            }
                        }
                    ]
                }
            })
            if len(updates) >= 3:
                break

    if not updates:
        print("❌ 没有找到可更新的文本块")
        return

    print(f"\n📝 正在批量更新 {len(updates)} 个块...\n")

    result = batch_update_blocks(
        app_id=app_id,
        app_secret=app_secret,
        document_id=document_id,
        updates=updates
    )

    if result:
        # 检查每个块是否更新成功
        for idx, item in enumerate(result.get("items", updates)):
            block_id = item.get("block_id", block_ids[idx])
            if "msg" in item:
                print(f"❌ 块 {block_id[:8]} 更新失败: {item.get('msg')}")
            else:
                print(f"✅ 块 {block_id[:8]} 更新成功")

        print(f"\n🎉 批量更新完成！")
        print(f"📄 文档链接: https://my.feishu.cn/docx/{document_id}")
    else:
        print(f"\n❌ 批量更新失败")


if __name__ == "__main__":
    main()
