# 飞书 CLI 使用指南

## 简介

飞书 CLI 是一个命令行工具，用于快速操作飞书开放平台的各项功能，无需编辑代码文件。

## 安装

```bash
# 克隆项目
git clone https://github.com/runningZ1/feishu-skill.git
cd feishu-skill

# 安装依赖
pip install -r requirements.txt
```

## 配置

首次使用需要配置应用凭据：

```bash
# 设置 app_id
python scripts/feishu.py config set app_id cli_xxx

# 设置 app_secret
python scripts/feishu.py config set app_secret xxx

# 查看所有配置
python scripts/feishu.py config list
```

配置文件保存在 `~/.feishu_config.json`

## 使用方法

### 1. 云空间操作

```bash
# 列出根目录文件
python scripts/feishu.py drive list

# 列出指定文件夹的文件
python scripts/feishu.py drive list --parent-token <token>

# 按修改时间排序，显示 10 个
python scripts/feishu.py drive list --order-by EditedTime --limit 10

# 创建文件夹
python scripts/feishu.py drive create-folder "新文件夹"

# 在指定位置创建文件夹
python scripts/feishu.py drive create-folder "新文件夹" --parent-token <token>
```

### 2. 文档操作

```bash
# 创建文档
python scripts/feishu.py doc create "文档标题"

# 在指定文件夹创建文档
python scripts/feishu.py doc create "文档标题" --folder-token <token>
```

### 3. 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `config set <key> <value>` | 设置配置 | `config set app_id xxx` |
| `config get <key>` | 获取配置 | `config get app_id` |
| `config list` | 列出配置 | `config list` |
| `drive list` | 列出文件 | `drive list --limit 10` |
| `drive create-folder <name>` | 创建文件夹 | `drive create-folder "测试"` |
| `doc create <title>` | 创建文档 | `doc create "我的文档"` |

## 快捷方式（可选）

### Unix/Linux/macOS

创建别名：

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
alias feishu='python /path/to/feishu-skill/scripts/feishu.py'

# 使用
feishu drive list
feishu doc create "测试"
```

### Windows

创建批处理文件 `feishu.bat` 并放到 PATH 目录：

```batch
@echo off
python C:\path\to\feishu-skill\scripts\feishu.py %*
```

或者创建 PowerShell 函数：

```powershell
# 添加到 $PROFILE
function feishu {
    python C:\path\to\feishu-skill\scripts\feishu.py $args
}
```

## 开发

### 添加新命令

1. 在 `scripts/feishu_cli/commands/` 下创建新模块
2. 实现 `build_parser()` 函数
3. 在 `scripts/feishu_cli/__main__.py` 中注册

### 项目结构

```
feishu-skill/
├── scripts/                    # 所有脚本文件
│   ├── feishu.py              # CLI 启动脚本
│   ├── feishu_cli/            # CLI 核心模块
│   │   ├── __init__.py
│   │   ├── __main__.py        # 主入口
│   │   ├── config.py          # 配置管理
│   │   ├── auth.py            # 认证逻辑
│   │   └── commands/          # 命令模块
│   │       ├── __init__.py
│   │       ├── drive.py       # 云空间命令
│   │       └── doc.py         # 文档命令
│   ├── list_files.py          # 原始脚本（保留）
│   ├── create_folder.py       # 原始脚本（保留）
│   ├── create_document.py     # 原始脚本（保留）
│   └── ...                    # 其他脚本
├── references/                # 参考文档
├── CLI_README.md              # 本文档
├── task_plan.md               # 开发计划
└── requirements.txt           # 依赖清单
```

### 两种使用方式

**方式一：CLI 命令（推荐）**
```bash
python scripts/feishu.py doc create "文档"
```

**方式二：直接运行脚本**
```bash
python scripts/create_document.py
# 需要编辑脚本中的硬编码参数
```
