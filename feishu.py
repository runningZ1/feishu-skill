#!/usr/bin/env python3
"""
飞书 CLI 启动脚本
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from feishu_cli import main

if __name__ == '__main__':
    sys.exit(main())
