# File Rename Tool

## Introduction

File Rename Tool is a desktop application developed based on PySide6, specifically designed for batch renaming files in folders. It supports bilingual interface switching, regular expression matching, real-time preview, and more.

### Main Features

| Feature | Description |
|---------|-------------|
| Batch Rename | Batch rename all files in a folder |
| String Replace | Replace specified strings in filenames with new strings |
| String Remove | Remove specified strings from filenames |
| Regular Expression | Support regex for complex matching and replacement |
| Real-time Preview | Preview all changes before execution |
| Bilingual Interface | Support Chinese and English interface |

### Interface Overview

The main interface contains the following areas:
- **Language Switch**: Top-right corner to switch between Chinese and English
- **Folder Selection**: Select the folder to operate on
- **Operation Type**: Replace or Remove (radio buttons)
- **Find/Replace**: Enter the strings to find and replace
- **Regular Expression Options**: Enable regex and display examples
- **File List**: Display all files in the selected folder
- **Preview/Apply**: Preview changes and execute renaming

---

## Features

- Batch Rename: Support batch renaming of all files in a directory
- Multiple Operations: Support Replace and Remove operations
- Regular Expression Support: Use regex for complex filename matching and replacement
- Real-time Preview: Preview all changes before applying them
- Bilingual Interface: Support Chinese and English interface switching

## Installation

```bash
pip install PySide6
```

## Usage

### 1. Run the Program

```bash
python file_rename_tool.py
```

### 2. Select a Folder

- Click the "Select Folder" button
- Browse and select the directory to operate on
- The program will display all files in that directory

### 3. Select Operation Type

- **Replace**: Replace specified string in filename with new string
- **Remove**: Remove specified string from filename

### 4. Enter Find and Replace Strings

- Enter the text to find in "Find Text"
- Enter the replacement text in "Replace Text" (leave empty for Remove operation)

### 5. Use Regular Expression

- Check the "Use Regular Expression" option
- Use regex for complex pattern matching and replacement

### 6. Regex Examples

| Find | Replace | Description |
|------|---------|-------------|
| `\s+` | `_` | Replace spaces with underscores |
| `\d+` | `#` | Replace numbers with # |
| `\[.*?\]` | (empty) | Delete brackets and their content |
| `^(.+)$` | `$1` | Capture filename |

### 7. Preview Results

- Click "Preview" to see all changes
- The preview list will show each file's original name and new name

### 8. Apply Changes

- After confirming the preview results, click "Apply"
- The program will execute all rename operations

### 9. Switch Language

- Select "中文" or "English" from the language dropdown at the top of the interface

## Notes

- Please carefully preview changes before applying
- It is recommended to backup important files before operations
- The program will warn you if there are regex syntax errors
- The program only processes files, not folders

---

## Regular Expression Reference

| Pattern | Description | Example |
|---------|-------------|---------|
| `.` | Match any single character | `a.c` matches "abc" |
| `*` | Match preceding element zero or more times | `ab*c` matches "ac", "abc" |
| `+` | Match preceding element one or more times | `ab+c` matches "abc", "abbc" |
| `\s` | Match whitespace character | `\s+` matches one or more spaces |
| `\d` | Match digit | `\d+` matches one or more digits |
| `^` | Match start of string | `^abc` matches strings starting with "abc" |
| `$` | Match end of string | `abc$` matches strings ending with "abc" |
| `[]` | Match character set | `[a-z]` matches lowercase letters |
| `()` | Capture group | `(abc)` captures "abc" |
| `\` | Escape character | `\[` matches literal "[" |

---

## Tech Stack

- Python 3.x
- PySide6 (Qt for Python)
- Regular Expressions (re module)

---

## License

MIT License

---

## Author Information

- **Author**: Lorime
- **Email**: lorime@126.com

---

## Donations

Support development with donations:

- **XMR**: 4DSQMNzzq46N1z2pZWAVdeA6JvUL9TCB2bnBiA3ZzoqEdYJnMydt5akCa3vtmapeDsbVKGPFdNkzzqTcJS8M8oyK7WGj5qMvNZRw61w6wMF
- **USDT (TRC20)**: TG6DCBoQszDxc64owRZKkSHqZfcAQrqR8uM
- **USDT (ERC20)**: 0x4323d39BA9b6Bd0570920e63a8D3a192b4459330

![QR Codes](erweima/xmr.jpg "XMR") ![QR Codes](erweima/usdt-tr20.jpg "USDT TRC20") ![QR Codes](erweima/usdt-erc20.jpg "USDT ERC20")

---

## About

File Rename Tool is a simple and efficient batch renaming tool designed for users who frequently work with files.

### Design Philosophy

- **Easy to Use**: Intuitive interface design, no complex configuration needed
- **Safe and Reliable**: Real-time preview ensures every operation meets expectations
- **Practical Features**: Supports regular expressions for complex renaming needs

### Use Cases

| Scenario | Description |
|----------|-------------|
| Photo Organization | Batch rename photos with unified naming format |
| Document Management | Organize downloaded documents, remove unwanted characters |
| Code Files | Batch modify code file names, unify naming conventions |
| Media Files | Rename music and video files for easier management |

### Version Information

- Current Version: 1.0.0
- Platform: Windows
- Language: Python 3.x
- GUI Framework: PySide6

---

## Help

### FAQ

**Q1: What should I do if the program doesn't start?**
A1: Make sure PySide6 is installed, run `pip install PySide6`.

**Q2: What if regular expressions don't work?**
A2: Make sure the "Use Regular Expression" option is checked, and verify the regex syntax is correct.

**Q3: How can I undo an operation?**
A3: The current version does not support undo. It is recommended to backup important files before operations.

**Q4: Does the program only process files?**
A4: Yes, the current version only processes files, not folders.

**Q5: How can I contact the author?**
A5: You can reach the author at lorime@126.com.

### Feedback and Suggestions

If you encounter any issues or have suggestions for improvement, feel free to contact:
- Email: lorime@126.com
