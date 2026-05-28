<div align="center">

# 🚀 DocConvert-CLI

**A lightweight, cross-platform document format conversion tool**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Introduction

DocConvert-CLI is a **lightweight, zero-configuration** document format conversion tool designed for developers and content creators. It provides seamless conversion between popular document formats including **Markdown, HTML, PDF, DOCX, and TXT**.

**Why DocConvert-CLI?**
- 🪶 **Ultra-lightweight**: Pure Python implementation, single-file executable
- ⚡ **Zero Configuration**: Works out of the box, no complex setup required
- 🎯 **Focused Core**: Concentrates on document formats without over-engineering
- 🔍 **Smart Detection**: Auto-detects input formats, simplifies commands
- 📦 **Batch Processing**: Supports wildcards and folder batch conversion
- 🎨 **Beautiful Output**: Rich CLI interface with progress bars and tables

### ✨ Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📝 **Multi-format Support** | Markdown ↔ HTML ↔ PDF ↔ DOCX ↔ TXT | ✅ Available |
| 🔍 **Auto Format Detection** | Detects format from content and extension | ✅ Available |
| 📂 **Batch Conversion** | Convert multiple files with wildcards | ✅ Available |
| 🎨 **Rich CLI** | Beautiful progress bars and output tables | ✅ Available |
| 🔧 **Encoding Detection** | Automatic file encoding detection | ✅ Available |
| 📊 **Conversion Stats** | Detailed conversion statistics | ✅ Available |

### 🚀 Quick Start

#### Installation

```bash
# Install from source
git clone https://github.com/gitstq/DocConvert-CLI.git
cd DocConvert-CLI
pip install -r requirements.txt

# Or install with full features
pip install -r requirements.txt
```

#### Basic Usage

```bash
# Convert single file
python docconvert.py convert input.md --to html

# Convert with specific output path
python docconvert.py convert input.md --to html --output output.html

# Batch convert
python docconvert.py batch "*.md" --to html

# Detect file format
python docconvert.py detect input.md

# List supported formats
python docconvert.py formats
```

### 📖 Usage Guide

#### Single File Conversion

```bash
# Markdown to HTML
python docconvert.py convert document.md --to html

# HTML to Markdown
python docconvert.py convert page.html --to markdown

# Markdown to Text
python docconvert.py convert notes.md --to txt

# Specify output directory
python docconvert.py convert report.md --to html --output-dir ./converted
```

#### Batch Conversion

```bash
# Convert all Markdown files in current directory
python docconvert.py batch "*.md" --to html

# Convert with recursive search
python docconvert.py batch "docs/**/*.md" --to html

# Convert to specific output directory
python docconvert.py batch "*.md" --to html --output-dir ./html_output
```

#### Format Detection

```bash
# Auto-detect file format and encoding
python docconvert.py detect mystery-file.txt
```

### 💡 Design Philosophy

DocConvert-CLI was born from the need for a **simple, lightweight** document conversion tool. Unlike heavy solutions like ConvertX or Marker:

- **No Docker required** - Pure Python, runs anywhere
- **No complex dependencies** - Core functionality works with minimal packages
- **No configuration files** - Sensible defaults, command-line driven
- **Fast startup** - No waiting for containers or services

### 📦 Supported Formats

| Format | Extensions | Conversion Support |
|--------|------------|-------------------|
| Markdown | .md, .markdown, .mkd | Full native support |
| HTML | .html, .htm | Full native support |
| Plain Text | .txt, .text | Full native support |
| PDF | .pdf | Via PyMuPDF / Pandoc |
| Word | .docx, .doc | Via python-docx / Pandoc |

### 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

DocConvert-CLI 是一款**轻量级、零配置**的文档格式转换工具，专为开发者和内容创作者设计。它提供 **Markdown、HTML、PDF、DOCX 和 TXT** 等流行文档格式之间的无缝转换。

**为什么选择 DocConvert-CLI？**
- 🪶 **极致轻量**：纯 Python 实现，单文件可执行
- ⚡ **开箱即用**：无需复杂配置，安装即可使用
- 🎯 **专注核心**：聚焦文档格式，不做过度扩展
- 🔍 **智能识别**：自动检测输入格式，简化命令
- 📦 **批量处理**：支持通配符和文件夹批量转换
- 🎨 **美观输出**：丰富的 CLI 界面，带进度条和表格

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 📝 **多格式支持** | Markdown ↔ HTML ↔ PDF ↔ DOCX ↔ TXT | ✅ 可用 |
| 🔍 **自动格式检测** | 从内容和扩展名检测格式 | ✅ 可用 |
| 📂 **批量转换** | 使用通配符转换多个文件 | ✅ 可用 |
| 🎨 **丰富 CLI** | 美观的进度条和输出表格 | ✅ 可用 |
| 🔧 **编码检测** | 自动文件编码检测 | ✅ 可用 |
| 📊 **转换统计** | 详细的转换统计信息 | ✅ 可用 |

### 🚀 快速开始

#### 安装

```bash
# 从源码安装
git clone https://github.com/gitstq/DocConvert-CLI.git
cd DocConvert-CLI
pip install -r requirements.txt

# 或安装完整功能
pip install -r requirements.txt
```

#### 基本用法

```bash
# 转换单个文件
python docconvert.py convert input.md --to html

# 指定输出路径
python docconvert.py convert input.md --to html --output output.html

# 批量转换
python docconvert.py batch "*.md" --to html

# 检测文件格式
python docconvert.py detect input.md

# 列出支持的格式
python docconvert.py formats
```

### 📖 详细使用指南

#### 单文件转换

```bash
# Markdown 转 HTML
python docconvert.py convert document.md --to html

# HTML 转 Markdown
python docconvert.py convert page.html --to markdown

# Markdown 转文本
python docconvert.py convert notes.md --to txt

# 指定输出目录
python docconvert.py convert report.md --to html --output-dir ./converted
```

#### 批量转换

```bash
# 转换当前目录所有 Markdown 文件
python docconvert.py batch "*.md" --to html

# 递归搜索转换
python docconvert.py batch "docs/**/*.md" --to html

# 转换到指定输出目录
python docconvert.py batch "*.md" --to html --output-dir ./html_output
```

#### 格式检测

```bash
# 自动检测文件格式和编码
python docconvert.py detect mystery-file.txt
```

### 💡 设计思路

DocConvert-CLI 诞生于对**简单、轻量**文档转换工具的需求。与 ConvertX 或 Marker 等重量级解决方案不同：

- **无需 Docker** - 纯 Python，随处运行
- **无复杂依赖** - 核心功能仅需最少包
- **无配置文件** - 合理的默认值，命令行驱动
- **快速启动** - 无需等待容器或服务

### 📦 支持格式

| 格式 | 扩展名 | 转换支持 |
|------|--------|----------|
| Markdown | .md, .markdown, .mkd | 完整原生支持 |
| HTML | .html, .htm | 完整原生支持 |
| 纯文本 | .txt, .text | 完整原生支持 |
| PDF | .pdf | 通过 PyMuPDF / Pandoc |
| Word | .docx, .doc | 通过 python-docx / Pandoc |

### 🤝 贡献指南

我们欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

### 📄 开源协议

本项目采用 MIT 协议 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🇹🇼 繁體中文

### 🎉 專案介紹

DocConvert-CLI 是一款**輕量級、零配置**的文件格式轉換工具，專為開發者和內容創作者設計。它提供 **Markdown、HTML、PDF、DOCX 和 TXT** 等流行文件格式之間的無縫轉換。

**為什麼選擇 DocConvert-CLI？**
- 🪶 **極致輕量**：純 Python 實現，單文件可執行
- ⚡ **開箱即用**：無需複雜配置，安裝即可使用
- 🎯 **專注核心**：聚焦文件格式，不做過度擴展
- 🔍 **智能識別**：自動檢測輸入格式，簡化命令
- 📦 **批次處理**：支援萬用字元和資料夾批次轉換
- 🎨 **美觀輸出**：豐富的 CLI 介面，帶進度條和表格

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 📝 **多格式支援** | Markdown ↔ HTML ↔ PDF ↔ DOCX ↔ TXT | ✅ 可用 |
| 🔍 **自動格式檢測** | 從內容和副檔名檢測格式 | ✅ 可用 |
| 📂 **批次轉換** | 使用萬用字元轉換多個文件 | ✅ 可用 |
| 🎨 **豐富 CLI** | 美觀的進度條和輸出表格 | ✅ 可用 |
| 🔧 **編碼檢測** | 自動文件編碼檢測 | ✅ 可用 |
| 📊 **轉換統計** | 詳細的轉換統計資訊 | ✅ 可用 |

### 🚀 快速開始

#### 安裝

```bash
# 從原始碼安裝
git clone https://github.com/gitstq/DocConvert-CLI.git
cd DocConvert-CLI
pip install -r requirements.txt

# 或安裝完整功能
pip install -r requirements.txt
```

#### 基本用法

```bash
# 轉換單個文件
python docconvert.py convert input.md --to html

# 指定輸出路徑
python docconvert.py convert input.md --to html --output output.html

# 批次轉換
python docconvert.py batch "*.md" --to html

# 檢測文件格式
python docconvert.py detect input.md

# 列出支援的格式
python docconvert.py formats
```

### 📖 詳細使用指南

#### 單文件轉換

```bash
# Markdown 轉 HTML
python docconvert.py convert document.md --to html

# HTML 轉 Markdown
python docconvert.py convert page.html --to markdown

# Markdown 轉文字
python docconvert.py convert notes.md --to txt

# 指定輸出目錄
python docconvert.py convert report.md --to html --output-dir ./converted
```

#### 批次轉換

```bash
# 轉換目前目錄所有 Markdown 文件
python docconvert.py batch "*.md" --to html

# 遞迴搜尋轉換
python docconvert.py batch "docs/**/*.md" --to html

# 轉換到指定輸出目錄
python docconvert.py batch "*.md" --to html --output-dir ./html_output
```

#### 格式檢測

```bash
# 自動檢測文件格式和編碼
python docconvert.py detect mystery-file.txt
```

### 💡 設計理念

DocConvert-CLI 誕生於對**簡單、輕量**文件轉換工具的需求。與 ConvertX 或 Marker 等重量級解決方案不同：

- **無需 Docker** - 純 Python，隨處執行
- **無複雜依賴** - 核心功能僅需最少套件
- **無設定檔** - 合理的預設值，命令列驅動
- **快速啟動** - 無需等待容器或服務

### 📦 支援格式

| 格式 | 副檔名 | 轉換支援 |
|------|--------|----------|
| Markdown | .md, .markdown, .mkd | 完整原生支援 |
| HTML | .html, .htm | 完整原生支援 |
| 純文字 | .txt, .text | 完整原生支援 |
| PDF | .pdf | 透過 PyMuPDF / Pandoc |
| Word | .docx, .doc | 透過 python-docx / Pandoc |

### 🤝 貢獻指南

我們歡迎貢獻！請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

### 📄 開源授權

本專案採用 MIT 授權 - 詳情請參閱 [LICENSE](LICENSE) 文件。

---

<div align="center">

**Made with ❤️ by the DocConvert Team**

</div>
