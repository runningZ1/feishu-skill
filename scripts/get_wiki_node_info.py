"""
飞书 Wiki - 获取节点信息

从 Wiki 链接获取节点的 document_id 和其他信息
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


def get_wiki_node_info(app_id: str, app_secret: str, node_token: str) -> dict:
    """
    获取 Wiki 节点信息

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        node_token: Wiki 节点 token（从 URL 中提取）

    Returns:
        dict: 节点信息，包含 document_id
    """
    access_token = get_tenant_access_token(app_id, app_secret)

    # 获取 Wiki 节点信息
    url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/nodes/get_node"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "token": node_token
    }

    response = requests.get(url, headers=headers, params=params)

    # 打印原始响应用于调试
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text[:500]}")

    # 尝试解析 JSON
    try:
        result = response.json()
    except Exception as e:
        print(f"❌ JSON 解析失败: {e}")
        print(f"原始响应: {response.text}")
        return None

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

    # Wiki 节点 token（从 URL 中提取）
    # URL: https://my.feishu.cn/wiki/WAkbwB8tZizdm9kRQjdc7yjNnA8
    node_token = "WAkbwB8tZizdm9kRQjdc7yjNnA8"

    print(f"🔍 正在获取 Wiki 节点信息...")
    print(f"节点 Token: {node_token}\n")

    result = get_wiki_node_info(app_id, app_secret, node_token)

    if result:
        print("✅ 节点信息获取成功！\n")
        print(f"节点类型: {result.get('obj_type')}")
        print(f"节点标题: {result.get('title')}")

        # 获取 document_id
        obj_token = result.get("obj_token")
        print(f"Document ID: {obj_token}")

        print("\n" + "="*50)
        print("📝 可以使用以下信息创建块:")
        print(f"document_id = \"{obj_token}\"")
        print(f"block_id = \"{obj_token}\"  # 通常使用 document_id 作为初始 block_id")
        print("="*50)

        return obj_token

    return None


if __name__ == "__main__":
    main()
