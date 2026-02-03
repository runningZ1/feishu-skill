"""
飞书文档 - 创建块

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/create
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


def create_text_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str,
    text: str
) -> dict:
    """
    创建文本块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 父块 ID（通常是页面的 Page 块 ID）
        text: 文本内容

    Returns:
        dict: 创建的块信息
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 文本块的数据结构
    body = {
        "index": -1,  # -1 表示添加到末尾
        "children": [
            {
                "block_type": 2,  # 2 表示文本块
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
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 创建失败: {result.get('code')} - {result.get('msg')}")
        print(f"详细信息: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return None

    return result.get("data")


def create_heading_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str,
    text: str,
    level: int = 1
) -> dict:
    """
    创建标题块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 父块 ID
        text: 标题内容
        level: 标题级别（1-3）

    Returns:
        dict: 创建的块信息
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 标题块类型映射
    heading_types = {1: 3, 2: 4, 3: 5}
    block_type = heading_types.get(level, 3)

    body = {
        "index": -1,
        "children": [
            {
                "block_type": block_type,
                "heading1" if level == 1 else "heading2" if level == 2 else "heading3": {
                    "elements": [
                        {
                            "text_run": {
                                "content": text
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 创建失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def create_bullet_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str,
    text: str
) -> dict:
    """
    创建无序列表块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 父块 ID
        text: 列表内容

    Returns:
        dict: 创建的块信息
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "index": -1,
        "children": [
            {
                "block_type": 8,  # 8 表示无序列表
                "bullet": {
                    "elements": [
                        {
                            "text_run": {
                                "content": text
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 创建失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def create_ordered_list_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str,
    text: str
) -> dict:
    """
    创建有序列表块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 父块 ID
        text: 列表内容

    Returns:
        dict: 创建的块信息
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "index": -1,
        "children": [
            {
                "block_type": 7,  # 7 表示有序列表
                "orderedList": {
                    "elements": [
                        {
                            "text_run": {
                                "content": text
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 创建失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def create_code_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str,
    code: str,
    language: str = "python"
) -> dict:
    """
    创建代码块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 父块 ID
        code: 代码内容
        language: 编程语言（python, java, javascript 等）

    Returns:
        dict: 创建的块信息
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "index": -1,
        "children": [
            {
                "block_type": 10,  # 10 表示代码块
                "code": {
                    "language": language,
                    "elements": [
                        {
                            "text_run": {
                                "content": code
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 创建失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def create_quote_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str,
    text: str
) -> dict:
    """
    创建引用块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 父块 ID
        text: 引用内容

    Returns:
        dict: 创建的块信息
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "index": -1,
        "children": [
            {
                "block_type": 12,  # 12 表示引用块
                "quote": {
                    "elements": [
                        {
                            "text_run": {
                                "content": text
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 创建失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def create_todo_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str,
    text: str,
    checked: bool = False
) -> dict:
    """
    创建待办块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 父块 ID
        text: 待办内容
        checked: 是否已完成

    Returns:
        dict: 创建的块信息
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "index": -1,
        "children": [
            {
                "block_type": 13,  # 13 表示待办块
                "todo": {
                    "elements": [
                        {
                            "text_run": {
                                "content": text
                            }
                        }
                    ],
                    "checked": checked
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 创建失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def main():
    """使用示例"""
    # 配置应用凭据
    app_id = "cli_a98322b338ed5013"
    app_secret = "NWd2p5HIvmp7VsxRLpgvBfODcFt1d6py"

    # 文档信息 - 使用刚创建的测试文档
    document_id = "Yfu7dIDBBohlbIxs6QQcj5wXn1d"  # 测试文档 ID
    block_id = "Yfu7dIDBBohlbIxs6QQcj5wXn1d"  # 使用 document_id 作为初始 block_id

    print("📝 正在创建块...\n")

    # 随机文本内容
    random_texts = [
        "🌟 今日箴言：成功的秘诀在于坚持自己的目标。",
        "💡 创意思维：让每一天都充满新的可能性。",
        "📚 知识分享：学习是一段永无止境的旅程。",
        "🚀 行动号召：把想法变成现实，从现在开始！",
        "🌈 心灵鸡汤：相信自己，你可以做到任何事情！"
    ]

    success_count = 0

    # 创建文本块
    for idx, text in enumerate(random_texts, 1):
        result = create_text_block(
            app_id=app_id,
            app_secret=app_secret,
            document_id=document_id,
            block_id=block_id,
            text=text
        )
        if result:
            success_count += 1
            print(f"✅ [{idx}/{len(random_texts)}] 创建成功: {text[:30]}...")
        else:
            print(f"❌ [{idx}/{len(random_texts)}] 创建失败")

    # 创建标题
    heading_result = create_heading_block(
        app_id=app_id,
        app_secret=app_secret,
        document_id=document_id,
        block_id=block_id,
        text="📝 随机文字测试",
        level=2
    )
    if heading_result:
        success_count += 1
        print(f"✅ 标题创建成功")

    # 创建无序列表
    bullet_texts = ["第一项内容", "第二项内容", "第三项内容"]
    for text in bullet_texts:
        result = create_bullet_block(
            app_id=app_id,
            app_secret=app_secret,
            document_id=document_id,
            block_id=block_id,
            text=text
        )
        if result:
            success_count += 1

    print(f"\n🎉 创建完成！成功创建 {success_count} 个块")
    print(f"📄 文档链接: https://my.feishu.cn/docx/{document_id}")


if __name__ == "__main__":
    main()
