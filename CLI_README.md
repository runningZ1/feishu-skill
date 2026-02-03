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
python feishu.py config set app_id cli_xxx

# 设置 app_secret
python feishu.py config set app_secret xxx

# 查看所有配置
python feishu.py config list
```

配置文件保存在 `~/.feishu_config.json`

## 使用方法

### 1. 云空间操作

```bash
# 列出根目录文件
python feishu.py drive list

# 列出指定文件夹的文件
python feishu.py drive list --parent-token <token>

# 按修改时间排序，显示 10 个
python feishu.py drive list --order-by EditedTime --limit 10

# 创建文件夹
python feishu.py drive create-folder "新文件夹"

# 在指定位置创建文件夹
python feishu.py drive create-folder "新文件夹" --parent-token <token>
```

### 2. 文档操作

```bash
# 创建文档
python feishu.py doc create "文档标题"

# 在指定文件夹创建文档
python feishu.py doc create "文档标题" --folder-token <token>
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

在 Unix/Linux/macOS 系统上，可以创建别名：

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
alias feishu='python /path/to/feishu-skill/feishu.py'

# 使用
feishu drive list
feishu doc create "测试"
```

在 Windows 上，可以创建批处理文件 `feishu.bat`：

```batch
@echo off
python C:\path\to\feishu-skill\feishu.py %*
```

## 开发

### 添加新命令

1. 在 `feishu_cli/commands/` 下创建新模块
2. 实现 `build_parser()` 函数
3. 在 `feishu_cli/__main__.py` 中注册

### 项目结构

```
feishu-skill/
├── feishu_cli/           # CLI 核心模块
│   ├── __init__.py
│   ├── __main__.py       # 主入口
│   ├── config.py         # 配置管理
│   ├── auth.py           # 认证逻辑
│   └── commands/         # 命令模块
│       ├── __init__.py
│       ├── drive.py      # 云空间命令
│       └── doc.py        # 文档命令
├── scripts/              # 原始脚本（保留）
├── feishu.py             # CLI 启动脚本
└── requirements.txt
```
