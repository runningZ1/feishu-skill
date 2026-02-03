---
name: feishu
description: 飞书平台操作技能 - 提供文档、知识库、云空间的完整操作能力。当用户需要操作飞书文档、管理知识库、处理云空间文件时使用此技能。
---

# 飞书技能

## 概述

提供飞书开放平台 API 的完整操作能力，按飞书官方文档结构划分为四大模块：

| 模块 | 目录 | 功能 |
|------|------|------|
| 云空间 | `scripts/drive/` | 文件夹、文件、上传下载、素材管理 |
| 知识库 | `scripts/wiki/` | 知识空间、节点、Wiki 文档 |
| 文档 | `scripts/docx/` | 文档创建、块操作、内容获取 |
| 多维表格 | - | (待实现) |

## 云空间 (Drive)

| 功能 | 脚本 | 说明 |
|------|------|------|
| 列出文件 | `list_files.py` | 获取文件夹中的文件清单 |
| 创建文件夹 | `create_folder.py` | 新建文件夹 |
| 文件元数据 | `get_file_meta.py` | 获取文件元数据 |
| 文件统计 | `get_file_statistics.py` | 获取文件统计信息 |
| 上传素材 | `upload_media.py` | 上传图片/视频等媒体 |

## 知识库 (Wiki)

| 功能 | 脚本 | 说明 |
|------|------|------|
| 节点信息 | `get_wiki_node_info.py` | 获取Wiki节点元信息 |
| 获取块 | `get_wiki_blocks_sdk.py` | 获取Wiki页面的所有块 |

## 文档 (Docx)

| 功能 | 脚本 | 说明 |
|------|------|------|
| 创建文档 | `create_document.py` | 创建新文档 |
| 获取信息 | `get_document_info.py` | 获取文档元信息 |
| 获取内容 | `get_document_raw_content.py` | 获取文档原始内容 |
| 获取块列表 | `get_document_blocks.py` | 获取文档所有块 |
| 搜索文档 | `search_documents.py` | 全文搜索文档 |

### 文档块操作

| 功能 | 脚本 | 说明 |
|------|------|------|
| 创建块 | `create_block.py` | 创建文本/段落/列表等块 |
| 更新块 | `update_block.py` | 更新块内容 |
| 删除块 | `delete_block.py` | 删除指定块 |
| 批量更新 | `batch_update_blocks.py` | 批量更新多个块 |
| 获取子块 | `get_child_blocks.py` | 获取块的子块列表 |
| 获取内容 | `get_block_content.py` | 获取块详细内容 |

## 配置

### 方式一：.env 文件（推荐）

在项目根目录创建 `.env` 文件：

```bash
FEISHU_APP_ID=cli_a98322b338ed5013
FEISHU_APP_SECRET=your_app_secret_here
```

### 方式二：CLI 命令

```bash
python scripts/feishu.py config set app_id <app_id>
python scripts/feishu.py config set app_secret <app_secret>
python scripts/feishu.py config list              # 查看配置
```

## CLI 工具

### 文档操作

```bash
python scripts/feishu.py doc create "文档标题"     # 创建文档
```

### 云空间操作

```bash
python scripts/feishu.py drive list               # 列出文件
python scripts/feishu.py drive create-folder "名称"  # 创建文件夹
```

## 资源目录

### scripts/
可执行的 Python 脚本，直接调用飞书 API 执行具体操作。

### references/
飞书开放平台技术文档和 API 参考资料。

### test/
测试脚本，验证各项功能。
