"""
飞书文档 - 创建块

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/create
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import argparse
import json
import os
import requests
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from feishu_cli.config import get_config
except ImportError:
    def get_config():
        class SimpleConfig:
            @property
            def app_id(self):
                return os.environ.get("FEISHU_APP_ID") or os.environ.get("app_id")

            @property
            def app_secret(self):
                return os.environ.get("FEISHU_APP_SECRET") or os.environ.get("app_secret")

            def validate_credentials(self):
                if not self.app_id:
                    print("❌ 未配置 app_id")
                    return False
                if not self.app_secret:
                    print("❌ 未配置 app_secret")
                    return False
                return True
        return SimpleConfig()


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    response = requests.post(url, json={"app_id": app_id, "app_secret": app_secret})
    return response.json().get("tenant_access_token")


def create_block(
    app_id: str,
    app_secret: str,
    document_id: str,
    block_id: str,
    block_type: str,
    content: str,
    level: int = 1
):
    """
    创建块

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        document_id: 文档 ID
        block_id: 父块 ID
        block_type: 块类型 (text, heading, bullet, ordered, code, quote, todo)
        content: 内容
        level: 标题级别 (仅用于 heading 类型)

    Returns:
        dict: 创建的块信息
    """
    access_token = get_tenant_access_token(app_id, app_secret)
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 块类型映射
    block_configs = {
        "text": {
            "block_type": 2,
            "body": {"text": {"elements": [{"text_run": {"content": content}}]}}
        },
        "heading": {
            "block_type": {1: 3, 2: 4, 3: 5}.get(level, 3),
            "body_key": {1: "heading1", 2: "heading2", 3: "heading3"}.get(level, "heading1"),
            "body": {"elements": [{"text_run": {"content": content}}]}
        },
        "bullet": {
            "block_type": 8,
            "body": {"bullet": {"elements": [{"text_run": {"content": content}}]}}
        },
        "ordered": {
            "block_type": 7,
            "body": {"orderedList": {"elements": [{"text_run": {"content": content}}]}}
        },
        "code": {
            "block_type": 10,
            "body": {"code": {"language": "python", "elements": [{"text_run": {"content": content}}]}}
        },
        "quote": {
            "block_type": 12,
            "body": {"quote": {"elements": [{"text_run": {"content": content}}]}}
        },
        "todo": {
            "block_type": 13,
            "body": {"todo": {"elements": [{"text_run": {"content": content}}], "checked": False}}
        }
    }

    if block_type not in block_configs:
        print(f"❌ 不支持的块类型: {block_type}")
        return None

    config = block_configs[block_type]
    body = {"index": -1, "children": []}

    if block_type == "heading":
        body["children"].append({
            "block_type": config["block_type"],
            config["body_key"]: config["body"]
        })
    else:
        body["children"].append({
            "block_type": config["block_type"],
            **config["body"]
        })

    response = requests.post(url, headers=headers, json=body)
    result = response.json()

    if result.get("code") != 0:
        print(f"❌ 创建失败: {result.get('code')} - {result.get('msg')}")
        return None

    return result.get("data")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="创建飞书文档块",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
块类型:
  text     - 文本块
  heading  - 标题块
  bullet   - 无序列表
  ordered  - 有序列表
  code     - 代码块
  quote    - 引用块
  todo     - 待办块

示例:
  python create_block.py --document-id xxx --block-id xxx --type text --content "内容"
  python create_block.py --document-id xxx --block-id xxx --type heading --content "标题" --level 2
        """
    )
    parser.add_argument("--document-id", "-d", required=True, help="文档 ID")
    parser.add_argument("--block-id", "-b", required=True, help="父块 ID（通常使用 document_id）")
    parser.add_argument("--type", "-t", required=True, choices=["text", "heading", "bullet", "ordered", "code", "quote", "todo"], help="块类型")
    parser.add_argument("--content", "-c", required=True, help="块内容")
    parser.add_argument("--level", "-l", type=int, default=1, choices=[1, 2, 3], help="标题级别（仅用于 heading 类型）")

    args = parser.parse_args()

    config = get_config()

    if not config.validate_credentials():
        sys.exit(1)

    result = create_block(
        app_id=config.app_id,
        app_secret=config.app_secret,
        document_id=args.document_id,
        block_id=args.block_id,
        block_type=args.type,
        content=args.content,
        level=args.level
    )

    if result:
        print("✅ 块创建成功！")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
