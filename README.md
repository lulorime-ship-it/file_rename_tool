# PDF Merger Tool

A powerful tool to merge multiple PDF files into one, built with PySide6 for a modern GUI experience.

## GitHub Repository

- **GitHub**: [https://github.com/lulorime-ship-it/PDFMerger](https://github.com/lulorime-ship-it/PDFMerger)

## Features

- **Modern GUI**: Built with PySide6 for a clean, responsive interface
- **File Management**: Add multiple PDF files or entire folders
- **File Sorting**: Reorder files using move up/down buttons
- **Page Range Selection**: Select specific pages from each PDF
- **PDF Properties**: Set title, author, subject, and keywords
- **Real-time Preview**: View PDF pages with navigation
- **Progress Bar**: Visual progress indicator during merging
- **Keyboard Shortcuts**: Quick access to common functions
- **Donation Support**: Multiple cryptocurrency options

## Requirements

- Python 3.13+
- PySide6
- pypdf

## Installation

1. **Install Python 3.13+** from [python.org](https://www.python.org/downloads/)

2. **Install dependencies**:
   ```bash
   pip install pyside6 pypdf
   ```

3. **Download the project files**:
   - `pdf_merger.py` - Main application
   - `run_pdf_merger.bat` - Run script
   - `erweima/` - Donation QR codes

## Usage

### Method 1: Double-click to run
- Double-click `run_pdf_merger.bat`

### Method 2: Command line
- Open terminal in project directory
- Run: `python pdf_merger.py`

## Keyboard Shortcuts

- `Ctrl+O`: Add PDF files
- `Ctrl+F`: Add folder
- `Delete`: Remove selected files
- `Ctrl+Up`: Move file up
- `Ctrl+Down`: Move file down
- `Ctrl+A`: Select all files
- `Ctrl+Shift+C`: Clear all files
- `Ctrl+M`: Merge PDFs
- `F1`: Show help
- `Ctrl+Q`: Exit program

## Page Range Format

- Leave empty to include all pages
- Single page: `5`
- Range of pages: `1-3`
- Multiple pages: `1,3,5`
- Mixed format: `1-3,5,7-9`

## Donation

Support the development by donating:

- **XMR**: 4DSQMNzzq46N1z2pZWAVdeA6JvUL9TCB2bnBiA3ZzoqEdYJnMydt5akCa3vtmapeDsbVKGPFdNkzzqTcJS8M8oyK7WGj5qMvNZRw61w6wMF
- **USDT (TRC20)**: TG6DCBoQszDxc64owRZKkSHqZfcAQrqR8uM
- **USDT (ERC20)**: 0x4323d39BA9b6Bd0570920e63a8D3a192b4459330

## Author

- **Name**: Lorime
- **Email**: lorime@126.com

## Version

1.0
