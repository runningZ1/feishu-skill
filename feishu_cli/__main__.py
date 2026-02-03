"""
飞书 CLI - 主入口
"""

import argparse
import sys

from .config import Config, get_config
from .commands import drive, doc


def cmd_config(args):
    """处理 config 命令"""
    config = get_config()

    if args.action == 'set':
        config.set(args.key, args.value)
        config.save()
        print(f"✅ 配置已更新: {args.key}")
    elif args.action == 'get':
        value = config.get(args.key)
        if value:
            print(f"{args.key}: {value}")
        else:
            print(f"未配置: {args.key}")
    elif args.action == 'list':
        print("当前配置:")
        for key, value in config._config.items():
            # 隐藏敏感信息
            if 'secret' in key.lower():
                value = value[:10] + '***' if value else 'N/A'
            print(f"  {key}: {value}")
    return 0


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        prog='feishu',
        description='飞书开放平台命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  feishu drive list                    列出根目录文件
  feishu drive list -p <token> -l 10   列出指定文件夹的 10 个文件
  feishu drive create-folder "测试"     创建文件夹
  feishu doc create "我的文档"          创建文档
  feishu config set app_id xxx         设置配置
  feishu config list                   查看配置
        """
    )

    # 添加版本参数
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')

    # 创建子命令解析器
    subparsers = parser.add_subparsers(dest='module', help='功能模块')

    # config 命令
    config_parser = subparsers.add_parser('config', help='配置管理')
    config_subparsers = config_parser.add_subparsers(dest='action', help='配置操作')

    # config set
    set_parser = config_subparsers.add_parser('set', help='设置配置项')
    set_parser.add_argument('key', help='配置键名')
    set_parser.add_argument('value', help='配置值')
    set_parser.set_defaults(func=cmd_config)

    # config get
    get_parser = config_subparsers.add_parser('get', help='获取配置项')
    get_parser.add_argument('key', help='配置键名')
    get_parser.set_defaults(func=cmd_config)

    # config list
    list_parser = config_subparsers.add_parser('list', help='列出所有配置')
    list_parser.set_defaults(func=cmd_config)

    # 注册各模块命令
    drive.build_parser(subparsers)
    doc.build_parser(subparsers)

    # 解析参数
    args = parser.parse_args()

    # 如果没有指定命令，显示帮助
    if not args.module and not hasattr(args, 'func'):
        parser.print_help()
        return 0

    # 执行命令
    if hasattr(args, 'func'):
        return args.func(args)

    # 处理模块级命令
    if args.module:
        parser.parse_args([args.module, '--help'])

    return 0


if __name__ == '__main__':
    sys.exit(main())
