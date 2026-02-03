"""
飞书文档 - 创建文档

API 文档: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/create
SDK 文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
"""

import argparse
import json
import os
import sys
from pathlib import Path

import lark_oapi as lark
from lark_oapi.api.docx.v1 import *

# 添加项目根目录到路径，以便导入配置模块
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from feishu_cli.config import get_config
except ImportError:
    # 如果无法导入配置模块，使用简单的环境变量读取
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
                    print("❌ 未配置 app_id，请设置环境变量 FEISHU_APP_ID")
                    return False
                if not self.app_secret:
                    print("❌ 未配置 app_secret，请设置环境变量 FEISHU_APP_SECRET")
                    return False
                return True
        return SimpleConfig()


def create_document(
    app_id: str,
    app_secret: str,
    title: str,
    folder_token: str = None
):
    """
    创建飞书文档

    Args:
        app_id: 应用 ID
        app_secret: 应用密钥
        title: 文档标题
        folder_token: 文件夹 token（可选，指定创建位置）

    Returns:
        dict: 包含 document_id 和 index_type 的创建结果
    """
    # 创建 client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.INFO) \
        .build()

    # 构造请求体
    body_builder = CreateDocumentRequestBody.builder().title(title)

    # 如果指定了文件夹，设置创建位置
    if folder_token:
        body_builder.folder_token(folder_token)

    # 构造请求对象
    request = CreateDocumentRequest.builder().request_body(body_builder.build()).build()

    # 发起请求
    response: CreateDocumentResponse = client.docx.v1.document.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document.create failed, code: {response.code}, msg: {response.msg}, "
            f"log_id: {response.get_log_id()}, resp: \n"
            f"{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}"
        )
        return None

    # 处理业务结果
    return response.data


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="创建飞书文档",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python create_document.py --title "我的文档"
  python create_document.py --title "测试" --folder_token xxx
        """
    )
    parser.add_argument("--title", "-t", required=True, help="文档标题")
    parser.add_argument("--folder-token", "-f", help="文件夹 token（可选）")

    args = parser.parse_args()

    # 获取配置
    config = get_config()

    if not config.validate_credentials():
        sys.exit(1)

    # 创建文档
    result = create_document(
        app_id=config.app_id,
        app_secret=config.app_secret,
        title=args.title,
        folder_token=args.folder_token
    )

    if result:
        document_id = result.document.document_id
        print(f"\n✅ 文档创建成功！")
        print(f"标题: {args.title}")
        print(f"Document ID: {document_id}")
        print(f"文档链接: https://my.feishu.cn/docx/{document_id}")

        print("\n" + "="*50)
        print("📝 可以使用以下信息继续操作:")
        print(f'--document-id "{document_id}"')
        print("="*50)
        sys.exit(0)
    else:
        print("❌ 文档创建失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
