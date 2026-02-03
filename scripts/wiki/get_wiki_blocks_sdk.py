"""
飞书文档 - 获取所有块（简化版）

使用您提供的文档 ID 直接获取块内容
"""

import json
import lark_oapi as lark
from lark_oapi.api.docx.v1 import ListDocumentBlockRequest


def get_document_blocks_with_content(
    client: lark.Client,
    document_id: str,
    page_size: int = 500
) -> dict:
    """
    获取文档所有块

    Args:
        client: 飞书客户端
        document_id: 文档 ID
        page_size: 分页大小，最大 500

    Returns:
        dict: 包含文档块列表的字典
    """
    request = ListDocumentBlockRequest.builder() \
        .document_id(document_id) \
        .page_size(page_size) \
        .document_revision_id(-1) \
        .build()

    response = client.docx.v1.document_block.list(request)

    if not response.success():
        print(f"❌ 获取文档块失败: {response.code} - {response.msg}")
        if response.raw:
            print(f"详细信息: {response.raw.content[:500]}")
        return None

    return json.loads(lark.JSON.marshal(response.data))


def main():
    """使用示例"""
    # 配置应用凭据
    app_id = "cli_a98322b338ed5013"
    app_secret = "NWd2p5HIvmp7VsxRLpgvBfODcFt1d6py"

    # 使用您提供的 user_access_token
    user_access_token = "u-dChicu.ilcF8Nr06GstRMVk1iwdQ01qVXqwaJMM0054B"

    # 使用您示例中的文档 ID
    document_id = "Uy82weEeqininYki5KWcpnuGnIb"

    # 创建客户端（配置 app_id 和 app_secret）
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .enable_set_token(True) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    option = lark.RequestOption.builder().user_access_token(user_access_token).build()
    client.default_request_option = option

    print(f"📄 正在获取文档的所有块...")
    print(f"   文档 ID: {document_id}\n")

    # 获取文档所有块
    blocks = get_document_blocks_with_content(client, document_id)
    if not blocks:
        return

    items = blocks.get("items", [])
    print(f"✅ 成功获取 {len(items)} 个块\n")

    # 显示所有块的详细信息
    for idx, item in enumerate(items, 1):
        block_id = item.get("block_id", "")
        block_type = item.get("block_type", 0)

        block_type_name = {
            1: "页面", 2: "文本", 3: "标题1", 4: "标题2", 5: "标题3",
            6: "图片", 7: "有序列表", 8: "无序列表", 9: "代码",
            10: "代码块", 11: "引用", 12: "引用块", 13: "待办",
            14: "待办块", 15: "分隔线", 16: "视图", 17: "文件",
            18: "视频", 19: "音频", 20: "表格", 21: "卡片",
            22: "分栏", 23: "高亮块", 24: "投票", 25: "目录",
            26: "文件", 27: "未识别", 28: "公式", 29: "代码语言"
        }.get(block_type, f"未知类型({block_type})")

        print(f"[{idx}] {block_type_name} (ID: {block_id[:20]}...)")

        # 尝试获取块内容
        for key in ["text", "heading1", "heading2", "heading3"]:
            if key in item:
                elements = item[key].get("elements", [])
                for elem in elements[:3]:
                    if "text_run" in elem:
                        content = elem["text_run"].get("content", "")
                        if content:
                            prefix = "📌" if "heading" in key else "📝"
                            print(f"    {prefix} {content[:100]}")
                break

        print()

    print(f"📄 文档链接: https://my.feishu.cn/docx/{document_id}")


if __name__ == "__main__":
    main()

