"""
飞书文档 - 获取所有子块

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/get-2
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


def get_child_blocks(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str
) -> dict:
    """
    获取某个块的所有子块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 父块 ID

    Returns:
        dict: 子块列表
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"

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

    # 文档信息 - 使用 document_id 作为根块 ID
    document_id = "Yfu7dIDBBohlbIxs6QQcj5wXn1d"

    print(f"📋 正在获取文档根块的子块...\n")

    result = get_child_blocks(
        app_id=app_id,
        app_secret=app_secret,
        document_id=document_id,
        block_id=document_id  # 根块的 ID 与文档 ID 相同
    )

    if result:
        items = result.get("items", [])
        print(f"✅ 成功获取 {len(items)} 个子块\n")

        # 显示前 10 个子块的信息
        for idx, item in enumerate(items[:10], 1):
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

            print(f"{idx}. {block_type_name} (ID: {block_id[:12]}...)")

        if len(items) > 10:
            print(f"\n... 还有 {len(items) - 10} 个块")

        print(f"\n📄 文档链接: https://my.feishu.cn/docx/{document_id}")
    else:
        print("❌ 获取子块失败")


if __name__ == "__main__":
    main()
