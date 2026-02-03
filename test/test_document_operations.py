"""
飞书文档 - 完整测试脚本

功能：
1. 获取 Wiki 文档的所有块
2. 测试更新块功能
3. 测试删除块功能

使用飞书官方 SDK (lark_oapi)
"""

import json
import lark_oapi as lark
from lark_oapi.api.docx.v1 import (
    ListDocumentBlockRequest,
    GetDocumentBlockRequest,
    PatchDocumentBlockRequest,
    BatchDeleteDocumentBlockRequest
)


# 配置
APP_ID = "cli_a98322b338ed5013"
APP_SECRET = "NWd2p5HIvmp7VsxRLpgvBfODcFt1d6py"
USER_ACCESS_TOKEN = "u-dChicu.ilcF8Nr06GstRMVk1iwdQ01qVXqwaJMM0054B"

# Wiki 链接: https://my.feishu.cn/wiki/WAkbwB8tZizdm9kRQjdc7yjNnA8
# 从用户之前的示例获取文档 ID: Uy82weEeqininYki5KWcpnuGnIb
DOCUMENT_ID = "Uy82weEeqininYki5KWcpnuGnIb"


def create_client():
    """创建飞书客户端"""
    client = lark.Client.builder() \
        .app_id(APP_ID) \
        .app_secret(APP_SECRET) \
        .enable_set_token(True) \
        .log_level(lark.LogLevel.WARN) \
        .build()

    option = lark.RequestOption.builder().user_access_token(USER_ACCESS_TOKEN).build()
    client.default_request_option = option

    return client


def get_all_blocks(client: lark.Client, document_id: str) -> list:
    """获取文档所有块"""
    print("📋 正在获取文档所有块...\n")

    request = ListDocumentBlockRequest.builder() \
        .document_id(document_id) \
        .page_size(500) \
        .document_revision_id(-1) \
        .build()

    response = client.docx.v1.document_block.list(request)

    if not response.success():
        print(f"❌ 获取失败: {response.code} - {response.msg}")
        return []

    data = json.loads(lark.JSON.marshal(response.data))
    items = data.get("items", [])

    print(f"✅ 成功获取 {len(items)} 个块\n")

    # 显示前 10 个块的摘要
    for idx, item in enumerate(items[:10], 1):
        block_id = item.get("block_id", "")
        block_type = item.get("block_type", 0)

        block_type_name = {
            1: "页面", 2: "文本", 3: "标题1", 4: "标题2", 5: "标题3",
            6: "图片", 7: "有序列表", 8: "无序列表", 10: "代码块",
            11: "引用", 12: "引用块", 13: "待办", 14: "待办块",
            15: "分隔线", 23: "高亮块", 24: "投票", 25: "目录"
        }.get(block_type, f"类型{block_type}")

        # 尝试获取内容预览
        content_preview = ""
        if "text" in item:
            elements = item["text"].get("elements", [])
            if elements and "text_run" in elements[0]:
                content = elements[0]["text_run"].get("content", "")
                content_preview = content[:40] + "..." if len(content) > 40 else content
        elif "heading1" in item:
            elements = item["heading1"].get("elements", [])
            if elements and "text_run" in elements[0]:
                content = elements[0]["text_run"].get("content", "")
                content_preview = "📌 " + content

        print(f"  [{idx}] {block_type_name} (ID: {block_id[:15]}...) {content_preview}")

    if len(items) > 10:
        print(f"  ... 还有 {len(items) - 10} 个块")

    return items


def get_single_block(client: lark.Client, document_id: str, block_id: str) -> dict:
    """获取单个块的详细信息"""
    request = GetDocumentBlockRequest.builder() \
        .document_id(document_id) \
        .block_id(block_id) \
        .build()

    response = client.docx.v1.document_block.get(request)

    if not response.success():
        print(f"❌ 获取块失败: {response.code} - {response.msg}")
        return None

    return json.loads(lark.JSON.marshal(response.data))


def update_block(client: lark.Client, document_id: str, block_id: str, new_text: str) -> bool:
    """更新块内容"""
    print(f"\n🔄 正在更新块 {block_id[:15]}...")

    request = PatchDocumentBlockRequest.builder() \
        .document_id(document_id) \
        .block_id(block_id) \
        .body({
            "text": {
                "elements": [{
                    "text_run": {
                        "content": new_text
                    }
                }]
            }
        }) \
        .build()

    response = client.docx.v1.document_block.patch(request)

    if not response.success():
        print(f"❌ 更新失败: {response.code} - {response.msg}")
        return False

    print(f"✅ 更新成功！新内容: {new_text[:50]}...")
    return True


def delete_block(client: lark.Client, document_id: str, block_id: str) -> bool:
    """删除块"""
    print(f"\n🗑️  正在删除块 {block_id[:15]}...")

    request = BatchDeleteDocumentBlockRequest.builder() \
        .document_id(document_id) \
        .body({"block_ids": [block_id]}) \
        .build()

    response = client.docx.v1.document_block.batch_delete(request)

    if not response.success():
        print(f"❌ 删除失败: {response.code} - {response.msg}")
        return False

    print(f"✅ 删除成功！")
    return True


def main():
    """主测试流程"""
    client = create_client()

    print("=" * 60)
    print("飞书文档块操作测试")
    print("=" * 60)
    print(f"文档 ID: {DOCUMENT_ID}")
    print(f"文档链接: https://my.feishu.cn/docx/{DOCUMENT_ID}")
    print("=" * 60)

    # 1. 获取所有块
    blocks = get_all_blocks(client, DOCUMENT_ID)

    if not blocks:
        print("❌ 没有获取到块，测试终止")
        return

    # 2. 测试更新块 - 找第一个文本块进行测试
    print("\n" + "=" * 60)
    print("测试 1: 更新块内容")
    print("=" * 60)

    # 查找第一个文本块 (block_type = 2)
    test_text_block = None
    for block in blocks:
        if block.get("block_type") == 2:  # 文本块
            test_text_block = block
            break

    if test_text_block:
        block_id = test_text_block.get("block_id")

        # 获取原始内容
        block_detail = get_single_block(client, DOCUMENT_ID, block_id)
        if block_detail:
            original_content = ""
            if "text" in block_detail:
                elements = block_detail["text"].get("elements", [])
                if elements and "text_run" in elements[0]:
                    original_content = elements[0]["text_run"].get("content", "")

            print(f"原始内容: {original_content}")

        # 更新块
        update_success = update_block(
            client, DOCUMENT_ID, block_id,
            f"🔄 [测试更新] {original_content[:50]} - 测试时间: 2026-02-03"
        )

        if update_success:
            # 获取更新后的内容验证
            block_detail = get_single_block(client, DOCUMENT_ID, block_id)
            if block_detail:
                new_content = ""
                if "text" in block_detail:
                    elements = block_detail["text"].get("elements", [])
                    if elements and "text_run" in elements[0]:
                        new_content = elements[0]["text_run"].get("content", "")
                print(f"验证更新后内容: {new_content}")
    else:
        print("⚠️  没有找到文本块进行测试")

    # 3. 测试删除块 - 使用最后一个块（假设不是重要内容）
    print("\n" + "=" * 60)
    print("测试 2: 删除块")
    print("=" * 60)
    print("⚠️  注意: 这将删除文档中的最后一个块！")
    print("     如果不想删除，请按 Ctrl+C 中断...")

    # 使用最后一个块进行删除测试
    last_block = blocks[-1]
    last_block_id = last_block.get("block_id")

    print(f"要删除的块 ID: {last_block_id}")
    print(f"块类型: {last_block.get('block_type')}")

    # 显示块内容供用户确认
    block_detail = get_single_block(client, DOCUMENT_ID, last_block_id)
    if block_detail:
        if "text" in block_detail:
            elements = block_detail["text"].get("elements", [])
            if elements and "text_run" in elements[0]:
                content = elements[0]["text_run"].get("content", "")
                print(f"块内容: {content}")

    # 执行删除
    delete_success = delete_block(client, DOCUMENT_ID, last_block_id)

    if delete_success:
        # 重新获取块列表验证删除
        print("\n🔍 验证删除结果...")
        blocks_after = get_all_blocks(client, DOCUMENT_ID)
        print(f"\n删除前: {len(blocks)} 个块")
        print(f"删除后: {len(blocks_after)} 个块")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
