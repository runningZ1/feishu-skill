"""
获取 Wiki 文档的所有块内容

用于测试用户提供的 Wiki 链接
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


def get_wiki_node_info(app_id: str, app_secret: str, token: str) -> dict:
    """
    获取 Wiki 节点信息

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        token: Wiki 节点 token

    Returns:
        dict: 节点信息
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/nodes/get_node"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "token": token
    }

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 获取失败: {result.get('code')} - {result.get('msg')}")
        print(f"详细信息: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return None

    return result.get("data")


def get_document_blocks(app_id: str, app_secret: str, document_id: str) -> dict:
    """
    获取文档所有块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID

    Returns:
        dict: 块列表
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/list"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 获取失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def main():
    """主函数"""
    # 配置应用凭据
    app_id = "cli_a98322b338ed5013"
    app_secret = "NWd2p5HIvmp7VsxRLpgvBfODcFt1d6py"

    # Wiki 节点 token（从 URL 中提取）
    wiki_token = "WAkbwB8tZizdm9kRQjdc7yjNnA8"

    print(f"📖 正在获取 Wiki 节点信息...")
    print(f"   Token: {wiki_token}\n")

    # 获取 Wiki 节点信息
    node_info = get_wiki_node_info(app_id, app_secret, wiki_token)
    if not node_info:
        print("❌ 无法获取 Wiki 节点信息")
        return

    # 获取文档 ID
    node_type = node_info.get("node_type")
    obj_type = node_info.get("obj_type")
    obj_token = node_info.get("obj_token")

    print(f"节点类型: {node_type}")
    print(f"对象类型: {obj_type}")
    print(f"对象 Token: {obj_token}")

    # 确定文档 ID
    document_id = obj_token  # 对于 docx 类型，obj_token 就是 document_id

    print(f"\n📄 正在获取文档的所有块...")
    print(f"   文档 ID: {document_id}\n")

    # 获取文档所有块
    blocks = get_document_blocks(app_id, app_secret, document_id)
    if not blocks:
        print("❌ 无法获取文档块")
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

        print(f"[{idx}] {block_type_name} (ID: {block_id})")

        # 尝试获取块内容
        if "text" in item:
            elements = item["text"].get("elements", [])
            if elements:
                for elem in elements[:3]:  # 只显示前 3 个元素
                    if "text_run" in elem:
                        content = elem["text_run"].get("content", "")
                        if content:
                            print(f"    📝 {content[:80]}...")
        elif "heading1" in item:
            elements = item["heading1"].get("elements", [])
            if elements:
                content = elements[0].get("text_run", {}).get("content", "")
                if content:
                    print(f"    📌 {content}")
        elif "heading2" in item:
            elements = item["heading2"].get("elements", [])
            if elements:
                content = elements[0].get("text_run", {}).get("content", "")
                if content:
                    print(f"    📌 {content}")
        elif "heading3" in item:
            elements = item["heading3"].get("elements", [])
            if elements:
                content = elements[0].get("text_run", {}).get("content", "")
                if content:
                    print(f"    📌 {content}")

        print()

    print(f"🌐 Wiki 链接: https://my.feishu.cn/wiki/{wiki_token}")
    print(f"📄 文档链接: https://my.feishu.cn/docx/{document_id}")


if __name__ == "__main__":
    main()
