# PDF 合并工具

一个强大的工具，用于将多个 PDF 文件合并为一个，使用 PySide6 构建现代化的 GUI 体验。

## GitHub 仓库

- **GitHub**: [https://github.com/lulorime-ship-it/PDFMerger](https://github.com/lulorime-ship-it/PDFMerger)

## 功能

- **现代化 GUI**：使用 PySide6 构建，界面干净、响应迅速
- **文件管理**：添加多个 PDF 文件或整个文件夹
- **文件排序**：使用上下移动按钮重新排序文件
- **页面范围选择**：从每个 PDF 中选择特定页面
- **PDF 属性设置**：设置标题、作者、主题和关键词
- **实时预览**：查看 PDF 页面并进行导航
- **进度条**：合并过程中的视觉进度指示器
- **键盘快捷键**：快速访问常用功能
- **捐献支持**：多种加密货币选项

## 要求

- Python 3.13+
- PySide6
- pypdf

## 安装

1. **安装 Python 3.13+** 从 [python.org](https://www.python.org/downloads/)

2. **安装依赖**：
   ```bash
   pip install pyside6 pypdf
   ```

3. **下载项目文件**：
   - `pdf_merger.py` - 主应用程序
   - `run_pdf_merger.bat` - 运行脚本
   - `erweima/` - 捐献二维码

## 使用方法

### 方法 1：双击运行
- 双击 `run_pdf_merger.bat`

### 方法 2：命令行
- 在项目目录中打开终端
- 运行：`python pdf_merger.py`

## 键盘快捷键

- `Ctrl+O`：添加 PDF 文件
- `Ctrl+F`：添加文件夹
- `Delete`：删除选中的文件
- `Ctrl+Up`：向上移动文件
- `Ctrl+Down`：向下移动文件
- `Ctrl+A`：选择所有文件
- `Ctrl+Shift+C`：清除所有文件
- `Ctrl+M`：合并 PDFs
- `F1`：显示帮助
- `Ctrl+Q`：退出程序

## 页面范围格式

- 留空表示包含所有页面
- 单个页面：`5`
- 页面范围：`1-3`
- 多个页面：`1,3,5`
- 混合格式：`1-3,5,7-9`

## 捐献

通过捐献给开发提供支持：

- **XMR**：4DSQMNzzq46N1z2pZWAVdeA6JvUL9TCB2bnBiA3ZzoqEdYJnMydt5akCa3vtmapeDsbVKGPFdNkzzqTcJS8M8oyK7WGj5qMvNZRw61w6wMF
- **USDT (TRC20)**：TG6DCBoQszDxc64owRZKkSHqZfcAQrqR8uM
- **USDT (ERC20)**：0x4323d39BA9b6Bd0570920e63a8D3a192b4459330

## 作者

- **姓名**：Lorime
- **邮箱**：lorime@126.com

## 版本

1.0