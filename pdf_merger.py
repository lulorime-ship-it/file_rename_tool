import sys
import os
import json
import threading
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QListWidget, QListWidgetItem, QLineEdit, QLabel, 
    QFileDialog, QMessageBox, QProgressBar, QStatusBar, QTreeWidget, 
    QTreeWidgetItem, QSplitter, QInputDialog, QDialog, QFormLayout,
    QScrollArea, QGroupBox, QRadioButton, QButtonGroup, QTextEdit,
    QGridLayout, QComboBox
)
from PySide6.QtGui import QIcon, QPixmap, QFont, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QThread, Signal
from pypdf import PdfReader, PdfWriter

def get_resource_path(relative_path):
    """获取资源文件的绝对路径，支持PyInstaller打包"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASSED中
        base_path = sys._MEIPASS
    except AttributeError:
        # 不是打包状态，使用脚本所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class PDFMerger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 1000, 700)
        
        # 初始化变量
        self.pdf_files = []
        self.output_path = ""
        self.config_file = os.path.join(os.path.expanduser("~"), ".pdf_merger_config.json")
        
        # PDF属性设置
        self.pdf_properties = {
            'title': '',
            'author': '',
            'subject': '',
            'keywords': ''
        }
        
        # 页面范围设置
        self.page_ranges = {}
        
        # 对话框状态
        self.about_window = None
        self.help_window = None
        self.page_range_window = None
        self.properties_window = None
        
        # 初始化UI
        self.init_ui()
        
        # 加载配置
        self.load_config()
    
    def init_ui(self):
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部按钮区域
        top_layout = QHBoxLayout()
        
        self.add_files_button = QPushButton("Add PDF Files")
        self.add_files_button.clicked.connect(self.add_pdf_files)
        top_layout.addWidget(self.add_files_button)
        
        self.add_folder_button = QPushButton("Add Folder")
        self.add_folder_button.clicked.connect(self.add_folder)
        top_layout.addWidget(self.add_folder_button)
        
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected)
        top_layout.addWidget(self.remove_button)
        
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all)
        top_layout.addWidget(self.clear_button)
        
        self.move_up_button = QPushButton("Move Up")
        self.move_up_button.clicked.connect(self.move_up)
        top_layout.addWidget(self.move_up_button)
        
        self.move_down_button = QPushButton("Move Down")
        self.move_down_button.clicked.connect(self.move_down)
        top_layout.addWidget(self.move_down_button)
        
        main_layout.addLayout(top_layout)
        
        # 分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：文件列表
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # 文件列表
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels(["Name", "Size", "Pages"])
        self.file_tree.setColumnWidth(0, 300)
        self.file_tree.setColumnWidth(1, 100)
        self.file_tree.setColumnWidth(2, 80)
        self.file_tree.itemSelectionChanged.connect(self.update_preview)
        left_layout.addWidget(self.file_tree)
        
        # 统计信息
        self.stats_label = QLabel("Files: 0, Pages: 0")
        left_layout.addWidget(self.stats_label)
        
        splitter.addWidget(left_widget)
        
        # 右侧：预览和控制
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 预览区域
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_label = QLabel("Select a PDF file to preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(300)
        preview_layout.addWidget(self.preview_label)
        
        # 预览导航
        nav_layout = QHBoxLayout()
        self.prev_page_button = QPushButton("Previous")
        self.prev_page_button.setEnabled(False)
        self.prev_page_button.clicked.connect(self.prev_preview_page)
        nav_layout.addWidget(self.prev_page_button)
        
        self.page_label = QLabel("Page: 0/0")
        self.page_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(self.page_label)
        
        self.next_page_button = QPushButton("Next")
        self.next_page_button.setEnabled(False)
        self.next_page_button.clicked.connect(self.next_preview_page)
        nav_layout.addWidget(self.next_page_button)
        
        preview_layout.addLayout(nav_layout)
        right_layout.addWidget(preview_group)
        
        # 输出设置
        output_group = QGroupBox("Output Settings")
        output_layout = QHBoxLayout(output_group)
        
        self.output_line = QLineEdit()
        self.output_line.setPlaceholderText("Output PDF file path")
        output_layout.addWidget(self.output_line)
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_output)
        output_layout.addWidget(self.browse_button)
        
        right_layout.addWidget(output_group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        right_layout.addWidget(self.progress_bar)
        
        # 控制按钮
        control_layout = QHBoxLayout()
        
        self.merge_button = QPushButton("Merge PDFs")
        self.merge_button.clicked.connect(self.start_merge)
        control_layout.addWidget(self.merge_button)
        
        self.properties_button = QPushButton("Properties")
        self.properties_button.clicked.connect(self.show_properties)
        control_layout.addWidget(self.properties_button)
        
        self.page_range_button = QPushButton("Page Range")
        self.page_range_button.clicked.connect(self.show_page_range)
        control_layout.addWidget(self.page_range_button)
        
        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.show_help)
        control_layout.addWidget(self.help_button)
        
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.show_about)
        control_layout.addWidget(self.about_button)
        
        right_layout.addLayout(control_layout)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 600])
        
        main_layout.addWidget(splitter)
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("Ready")
        
        # 预览变量
        self.current_preview_file = None
        self.current_preview_page = 0
        self.preview_pages = []
    
    def add_pdf_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files", "", "PDF Files (*.pdf)"
        )
        if files:
            for file in files:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)
            self.update_file_list()
            self.update_status(f"Added {len(files)} PDF files")
    
    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Folder"
        )
        if folder:
            added = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_path = os.path.join(root, file)
                        if pdf_path not in self.pdf_files:
                            self.pdf_files.append(pdf_path)
                            added += 1
            if added > 0:
                self.update_file_list()
                self.update_status(f"Added {added} PDF files from folder")
            else:
                QMessageBox.information(self, "Info", "No PDF files found in the selected folder")
    
    def remove_selected(self):
        selected_items = self.file_tree.selectedItems()
        if selected_items:
            for item in selected_items:
                file_path = item.data(0, Qt.UserRole)
                if file_path in self.pdf_files:
                    self.pdf_files.remove(file_path)
                    # 移除相关的页面范围设置
                    if file_path in self.page_ranges:
                        del self.page_ranges[file_path]
            self.update_file_list()
            self.update_status(f"Removed {len(selected_items)} files")
            # 清除预览
            self.clear_preview()
    
    def clear_all(self):
        if self.pdf_files:
            self.pdf_files = []
            self.page_ranges = {}
            self.update_file_list()
            self.update_status("Cleared all files")
            # 清除预览
            self.clear_preview()
    
    def move_up(self):
        selected_items = self.file_tree.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.file_tree.indexOfTopLevelItem(item)
            if index > 0:
                file_path = item.data(0, Qt.UserRole)
                # 调整文件列表顺序
                self.pdf_files.insert(index - 1, self.pdf_files.pop(index))
                self.update_file_list()
                # 重新选择移动后的项目
                new_item = self.file_tree.topLevelItem(index - 1)
                self.file_tree.setCurrentItem(new_item)
                self.update_status("Moved file up")
    
    def move_down(self):
        selected_items = self.file_tree.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.file_tree.indexOfTopLevelItem(item)
            if index < len(self.pdf_files) - 1:
                file_path = item.data(0, Qt.UserRole)
                # 调整文件列表顺序
                self.pdf_files.insert(index + 1, self.pdf_files.pop(index))
                self.update_file_list()
                # 重新选择移动后的项目
                new_item = self.file_tree.topLevelItem(index + 1)
                self.file_tree.setCurrentItem(new_item)
                self.update_status("Moved file down")
    
    def update_file_list(self):
        # 清空文件树
        self.file_tree.clear()
        
        total_pages = 0
        
        for file_path in self.pdf_files:
            try:
                # 获取文件信息
                size, pages = self.get_file_info(file_path)
                total_pages += pages
                
                # 创建树项
                item = QTreeWidgetItem()
                item.setText(0, os.path.basename(file_path))
                item.setText(1, size)
                item.setText(2, str(pages))
                item.setData(0, Qt.UserRole, file_path)
                self.file_tree.addTopLevelItem(item)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # 更新统计信息
        self.stats_label.setText(f"Files: {len(self.pdf_files)}, Pages: {total_pages}")
    
    def get_file_info(self, file_path):
        """获取文件信息"""
        # 获取文件大小
        size = os.path.getsize(file_path)
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.2f} KB"
        else:
            size_str = f"{size / (1024 * 1024):.2f} MB"
        
        # 获取页数
        try:
            reader = PdfReader(file_path)
            pages = len(reader.pages)
        except:
            pages = 0
        
        return size_str, pages
    
    def update_preview(self):
        selected_items = self.file_tree.selectedItems()
        if selected_items:
            file_path = selected_items[0].data(0, Qt.UserRole)
            self.current_preview_file = file_path
            self.current_preview_page = 0
            self.load_preview()
        else:
            self.clear_preview()
    
    def load_preview(self):
        if not self.current_preview_file:
            return
        
        try:
            reader = PdfReader(self.current_preview_file)
            total_pages = len(reader.pages)
            
            if total_pages > 0:
                # 渲染第一页
                self.current_preview_page = 0
                pixmap = self.render_pdf_page(None)
                if pixmap:
                    self.preview_label.setPixmap(pixmap)
                    self.page_label.setText(f"Page: 1/{total_pages}")
                    self.prev_page_button.setEnabled(False)
                    self.next_page_button.setEnabled(total_pages > 1)
                    # 预渲染所有页面
                    self.preview_pages = []
                    for i in range(total_pages):
                        self.current_preview_page = i
                        page_pixmap = self.render_pdf_page(None)
                        self.preview_pages.append(page_pixmap)
                    # 重置为第一页
                    self.current_preview_page = 0
                    self.update_preview_page()
                else:
                    self.preview_label.setText("Preview not available")
                    self.page_label.setText("Page: 0/0")
                    self.prev_page_button.setEnabled(False)
                    self.next_page_button.setEnabled(False)
            else:
                self.preview_label.setText("PDF has no pages")
                self.page_label.setText("Page: 0/0")
                self.prev_page_button.setEnabled(False)
                self.next_page_button.setEnabled(False)
        except Exception as e:
            self.preview_label.setText(f"Error loading PDF: {str(e)}")
            self.page_label.setText("Page: 0/0")
            self.prev_page_button.setEnabled(False)
            self.next_page_button.setEnabled(False)
    
    def render_pdf_page(self, page):
        """渲染PDF页面为QPixmap"""
        try:
            # 这里使用pypdf提取文本内容并显示
            from PySide6.QtGui import QPainter
            from PySide6.QtCore import QSize
            
            # 创建一个占位符
            pixmap = QPixmap(400, 600)
            pixmap.fill(Qt.white)
            
            painter = QPainter(pixmap)
            
            # 显示PDF信息
            painter.drawText(100, 50, "PDF Page Preview")
            painter.drawText(100, 100, f"File: {os.path.basename(self.current_preview_file)}")
            
            # 获取PDF信息
            reader = PdfReader(self.current_preview_file)
            total_pages = len(reader.pages)
            painter.drawText(100, 150, f"Page: {self.current_preview_page + 1}/{total_pages}")
            
            # 提取页面文本内容
            page = reader.pages[self.current_preview_page]
            text = page.extract_text()
            
            # 显示文本内容（限制显示行数）
            if text:
                lines = text.split('\n')
                max_lines = 15  # 最多显示15行
                display_lines = lines[:max_lines]
                display_text = '\n'.join(display_lines)
                
                # 绘制文本内容
                y_pos = 200
                for line in display_lines:
                    if y_pos > 550:  # 防止超出边界
                        painter.drawText(100, y_pos, "... (more content)")
                        break
                    painter.drawText(100, y_pos, line)
                    y_pos += 20
            else:
                painter.drawText(100, 200, "No text content available")
            
            painter.end()
            
            return pixmap
        except Exception as e:
            print(f"Error rendering PDF page: {e}")
            # 如果渲染失败，使用简单占位符
            from PySide6.QtGui import QPainter
            from PySide6.QtCore import QSize
            
            pixmap = QPixmap(400, 600)
            pixmap.fill(Qt.white)
            
            painter = QPainter(pixmap)
            painter.drawText(100, 300, "PDF Page Preview")
            painter.end()
            
            return pixmap
    
    def prev_preview_page(self):
        if self.current_preview_page > 0:
            self.current_preview_page -= 1
            self.update_preview_page()
    
    def next_preview_page(self):
        if self.current_preview_page < len(self.preview_pages) - 1:
            self.current_preview_page += 1
            self.update_preview_page()
    
    def update_preview_page(self):
        if 0 <= self.current_preview_page < len(self.preview_pages):
            pixmap = self.preview_pages[self.current_preview_page]
            if pixmap:
                self.preview_label.setPixmap(pixmap)
                self.page_label.setText(f"Page: {self.current_preview_page + 1}/{len(self.preview_pages)}")
                self.prev_page_button.setEnabled(self.current_preview_page > 0)
                self.next_page_button.setEnabled(self.current_preview_page < len(self.preview_pages) - 1)
    
    def clear_preview(self):
        self.current_preview_file = None
        self.current_preview_page = 0
        self.preview_pages = []
        self.preview_label.setText("Select a PDF file to preview")
        self.page_label.setText("Page: 0/0")
        self.prev_page_button.setEnabled(False)
        self.next_page_button.setEnabled(False)
    
    def browse_output(self):
        file, _ = QFileDialog.getSaveFileName(
            self, "Save Output PDF", "", "PDF Files (*.pdf)"
        )
        if file:
            self.output_path = file
            self.output_line.setText(file)
    
    def start_merge(self):
        if not self.pdf_files:
            QMessageBox.warning(self, "Warning", "Please add PDF files first.")
            return
        
        if not self.output_path:
            QMessageBox.warning(self, "Warning", "Please select output file path.")
            return
        
        # 禁用合并按钮
        self.merge_button.setEnabled(False)
        self.update_status("Merging PDFs...")
        self.progress_bar.setValue(0)
        
        # 启动后台线程进行合并
        merge_thread = threading.Thread(target=self.merge_pdfs)
        merge_thread.daemon = True
        merge_thread.start()
    
    def merge_pdfs(self):
        try:
            writer = PdfWriter()
            total_files = len(self.pdf_files)
            
            for i, pdf_file in enumerate(self.pdf_files):
                # 获取页面范围
                page_range = self.page_ranges.get(pdf_file, "")
                if page_range:
                    # 解析页面范围并添加指定页面
                    try:
                        reader = PdfReader(pdf_file)
                        pages = self.parse_page_range(page_range, len(reader.pages))
                        for page_num in pages:
                            writer.add_page(reader.pages[page_num - 1])  # 页面索引从0开始
                    except Exception as e:
                        self.update_status(f"Error processing {os.path.basename(pdf_file)}: {str(e)}")
                else:
                    # 添加整个文件
                    writer.append(pdf_file)
                
                progress = (i + 1) / total_files * 100
                QApplication.processEvents()
                self.progress_bar.setValue(int(progress))
            
            with open(self.output_path, 'wb') as output_file:
                # 设置PDF属性
                if self.pdf_properties['title']:
                    writer.add_metadata({'/Title': self.pdf_properties['title']})
                if self.pdf_properties['author']:
                    writer.add_metadata({'/Author': self.pdf_properties['author']})
                if self.pdf_properties['subject']:
                    writer.add_metadata({'/Subject': self.pdf_properties['subject']})
                if self.pdf_properties['keywords']:
                    writer.add_metadata({'/Keywords': self.pdf_properties['keywords']})
                
                writer.write(output_file)
            
            self.progress_bar.setValue(100)
            self.update_status(f"Successfully merged {len(self.pdf_files)} PDFs to {self.output_path}")
            QMessageBox.information(self, "Success", f"PDFs merged successfully!\nOutput: {self.output_path}")
        
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to merge PDFs: {str(e)}")
        finally:
            # 重新启用按钮
            self.merge_button.setEnabled(True)
            # 保存配置
            self.save_config()
    
    def parse_page_range(self, page_range_str, total_pages):
        """解析页面范围字符串"""
        pages = set()
        ranges = page_range_str.split(',')
        
        for r in ranges:
            r = r.strip()
            if not r:
                continue
            
            if '-' in r:
                # 处理范围，如 1-3
                try:
                    start, end = r.split('-')
                    start = int(start.strip())
                    end = int(end.strip())
                    # 确保范围有效
                    start = max(1, start)
                    end = min(total_pages, end)
                    if start <= end:
                        pages.update(range(start, end + 1))
                except ValueError:
                    pass
            else:
                # 处理单个页面，如 5
                try:
                    page = int(r.strip())
                    if 1 <= page <= total_pages:
                        pages.add(page)
                except ValueError:
                    pass
        
        return sorted(pages)
    
    def show_properties(self):
        # 检查窗口是否已经存在
        if self.properties_window and self.properties_window.isVisible():
            self.properties_window.raise_()
            return
        
        self.properties_window = QDialog(self)
        self.properties_window.setWindowTitle("PDF Properties")
        self.properties_window.setGeometry(300, 200, 400, 250)
        
        layout = QVBoxLayout(self.properties_window)
        
        form_layout = QFormLayout()
        
        self.title_edit = QLineEdit(self.pdf_properties['title'])
        form_layout.addRow("Title:", self.title_edit)
        
        self.author_edit = QLineEdit(self.pdf_properties['author'])
        form_layout.addRow("Author:", self.author_edit)
        
        self.subject_edit = QLineEdit(self.pdf_properties['subject'])
        form_layout.addRow("Subject:", self.subject_edit)
        
        self.keywords_edit = QLineEdit(self.pdf_properties['keywords'])
        form_layout.addRow("Keywords:", self.keywords_edit)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.save_properties)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.properties_window.close)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.properties_window.exec()
    
    def save_properties(self):
        self.pdf_properties['title'] = self.title_edit.text()
        self.pdf_properties['author'] = self.author_edit.text()
        self.pdf_properties['subject'] = self.subject_edit.text()
        self.pdf_properties['keywords'] = self.keywords_edit.text()
        self.properties_window.close()
        self.update_status("PDF properties saved")
    
    def show_page_range(self):
        # 检查窗口是否已经存在
        if self.page_range_window and self.page_range_window.isVisible():
            self.page_range_window.raise_()
            return
        
        # 检查是否有文件
        if not self.pdf_files:
            QMessageBox.warning(self, "Warning", "Please add PDF files first.")
            return
        
        self.page_range_window = QDialog(self)
        self.page_range_window.setWindowTitle("Page Range Settings")
        self.page_range_window.setGeometry(300, 200, 500, 400)
        
        layout = QVBoxLayout(self.page_range_window)
        
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        QLabel("Enter page ranges for each PDF file (e.g., 1-3,5,7-9)", scroll_content).show()
        
        self.page_range_edits = {}
        for i, pdf_file in enumerate(self.pdf_files):
            file_frame = QWidget()
            file_layout = QHBoxLayout(file_frame)
            
            # 获取文件名
            filename = os.path.basename(pdf_file)
            
            # 获取页数
            _, pages = self.get_file_info(pdf_file)
            
            # 标签
            label = QLabel(f"{i+1}. {filename} ({pages} pages):")
            label.setFixedWidth(250)
            file_layout.addWidget(label)
            
            # 输入框
            edit = QLineEdit(self.page_ranges.get(pdf_file, ""))
            self.page_range_edits[pdf_file] = edit
            file_layout.addWidget(edit)
            
            scroll_layout.addWidget(file_frame)
        
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_page_ranges)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.page_range_window.close)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.page_range_window.exec()
    
    def save_page_ranges(self):
        # 保存页面范围设置
        for pdf_file, edit in self.page_range_edits.items():
            self.page_ranges[pdf_file] = edit.text().strip()
        self.page_range_window.close()
        self.update_status("Page range settings saved")
    
    def show_help(self):
        # 检查窗口是否已经存在
        if self.help_window and self.help_window.isVisible():
            self.help_window.raise_()
            return
        
        self.help_window = QDialog(self)
        self.help_window.setWindowTitle("Help")
        self.help_window.setGeometry(300, 200, 600, 500)
        
        layout = QVBoxLayout(self.help_window)
        
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # 基本使用说明
        QLabel("<h2>Basic Usage:</h2>", scroll_content).show()
        usage_steps = [
            "1. Click 'Add PDF Files' to select PDF files to merge",
            "2. Click 'Add Folder' to add all PDF files in a folder",
            "3. Use 'Move Up' and 'Move Down' to adjust the merge order",
            "4. Click 'Page Range' to select specific pages from each PDF",
            "5. Specify the output file path",
            "6. Click 'Merge PDFs' to start the process",
            "7. Check the status bar for progress updates"
        ]
        for step in usage_steps:
            QLabel(step, scroll_content).show()
        
        # 页面范围说明
        QLabel("<h2>Page Range Format:</h2>", scroll_content).show()
        page_range_examples = [
            "- Leave empty to include all pages",
            "- Single page: 5",
            "- Range of pages: 1-3",
            "- Multiple pages: 1,3,5",
            "- Mixed format: 1-3,5,7-9"
        ]
        for example in page_range_examples:
            QLabel(example, scroll_content).show()
        
        # 快捷键说明
        QLabel("<h2>Keyboard Shortcuts:</h2>", scroll_content).show()
        shortcuts = [
            "Ctrl+O: Add PDF files",
            "Ctrl+F: Add folder",
            "Delete: Remove selected files",
            "Ctrl+Up: Move file up",
            "Ctrl+Down: Move file down",
            "Ctrl+A: Select all files",
            "Ctrl+Shift+C: Clear all files",
            "Ctrl+M: Merge PDFs",
            "F1: Show help",
            "Ctrl+Q: Exit program"
        ]
        for shortcut in shortcuts:
            QLabel(shortcut, scroll_content).show()
        
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.help_window.close)
        layout.addWidget(ok_button)
        
        self.help_window.exec()
    
    def show_about(self):
        # 检查窗口是否已经存在
        if self.about_window and self.about_window.isVisible():
            self.about_window.raise_()
            return
        
        self.about_window = QDialog(self)
        self.about_window.setWindowTitle("About PDF Merger")
        self.about_window.setGeometry(300, 200, 700, 650)
        
        layout = QVBoxLayout(self.about_window)
        
        # 标题
        title_label = QLabel("<h1>PDF Merger</h1>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 版本
        version_label = QLabel("Version 1.0")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # 描述
        desc_label = QLabel("A powerful tool to merge multiple PDF files into one.")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)
        
        # 作者和邮箱
        author_label = QLabel("<h3>Author: Lorime</h3>")
        author_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(author_label)
        
        email_label = QLabel("<h4>Email: lorime@126.com</h4>")
        email_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(email_label)
        
        # 捐献信息
        donate_label = QLabel("<h3>Donate:</h3>")
        donate_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(donate_label)
        
        # 捐献框架
        donate_frame = QWidget()
        donate_layout = QVBoxLayout(donate_frame)
        
        # XMR
        xmr_frame = QWidget()
        xmr_layout = QHBoxLayout(xmr_frame)
        xmr_label = QLabel("<b>XMR:</b>")
        xmr_layout.addWidget(xmr_label)
        xmr_address = QLabel("4DSQMNzzq46N1z2pZWAVdeA6JvUL9TCB2bnBiA3ZzoqEdYJnMydt5akCa3vtmapeDsbVKGPFdNkzzqTcJS8M8oyK7WGj5qMvNZRw61w6wMF")
        xmr_address.setWordWrap(True)
        xmr_layout.addWidget(xmr_address)
        donate_layout.addWidget(xmr_frame)

        # 加载XMR二维码
        xmr_qr_path = get_resource_path("erweima/xmr.jpg")
        if os.path.exists(xmr_qr_path):
            xmr_pixmap = QPixmap(xmr_qr_path)
            if not xmr_pixmap.isNull():
                xmr_qr_label = QLabel()
                xmr_qr_label.setPixmap(xmr_pixmap.scaled(120, 120, Qt.KeepAspectRatio))
                xmr_qr_label.setAlignment(Qt.AlignCenter)
                donate_layout.addWidget(xmr_qr_label)

        # USDT TRC20 和 ERC20 并排
        usdt_frame = QWidget()
        usdt_layout = QHBoxLayout(usdt_frame)

        # USDT TRC20
        trc20_frame = QWidget()
        trc20_layout = QVBoxLayout(trc20_frame)
        trc20_label = QLabel("<b>USDT (TRC20):</b>")
        trc20_layout.addWidget(trc20_label)
        trc20_address = QLabel("TG6DCBoQszDxc64owRZKkSHqZfcAQrqR8uM")
        trc20_address.setWordWrap(True)
        trc20_layout.addWidget(trc20_address)
        # 加载TRC20二维码
        trc20_qr_path = get_resource_path("erweima/usdt-tr20.jpg")
        if os.path.exists(trc20_qr_path):
            trc20_pixmap = QPixmap(trc20_qr_path)
            if not trc20_pixmap.isNull():
                trc20_qr_label = QLabel()
                trc20_qr_label.setPixmap(trc20_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                trc20_qr_label.setAlignment(Qt.AlignCenter)
                trc20_layout.addWidget(trc20_qr_label)
        usdt_layout.addWidget(trc20_frame)

        # USDT ERC20
        erc20_frame = QWidget()
        erc20_layout = QVBoxLayout(erc20_frame)
        erc20_label = QLabel("<b>USDT (ERC20):</b>")
        erc20_layout.addWidget(erc20_label)
        erc20_address = QLabel("0x4323d39BA9b6Bd0570920e63a8D3a192b4459330")
        erc20_address.setWordWrap(True)
        erc20_layout.addWidget(erc20_address)
        # 加载ERC20二维码
        erc20_qr_path = get_resource_path("erweima/usdt-erc20.jpg")
        if os.path.exists(erc20_qr_path):
            erc20_pixmap = QPixmap(erc20_qr_path)
            if not erc20_pixmap.isNull():
                erc20_qr_label = QLabel()
                erc20_qr_label.setPixmap(erc20_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                erc20_qr_label.setAlignment(Qt.AlignCenter)
                erc20_layout.addWidget(erc20_qr_label)
        usdt_layout.addWidget(erc20_frame)
        
        donate_layout.addWidget(usdt_frame)
        layout.addWidget(donate_frame)
        
        # 按钮
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.about_window.close)
        layout.addWidget(ok_button)
        
        self.about_window.exec()
    
    def update_status(self, message):
        self.status_bar.showMessage(message)
    
    def load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'output_path' in config:
                        self.output_path = config['output_path']
                        self.output_line.setText(self.output_path)
                    if 'pdf_properties' in config:
                        self.pdf_properties.update(config['pdf_properties'])
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """保存配置"""
        try:
            config = {
                'output_path': self.output_path,
                'pdf_properties': self.pdf_properties
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_O:
                self.add_pdf_files()
            elif event.key() == Qt.Key_F:
                self.add_folder()
            elif event.key() == Qt.Key_Up:
                self.move_up()
            elif event.key() == Qt.Key_Down:
                self.move_down()
            elif event.key() == Qt.Key_A:
                # 全选
                self.file_tree.selectAll()
            elif event.key() == Qt.Key_M:
                self.start_merge()
            elif event.key() == Qt.Key_Q:
                self.close()
        elif event.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier):
            if event.key() == Qt.Key_C:
                self.clear_all()
        elif event.key() == Qt.Key_Delete:
            self.remove_selected()
        elif event.key() == Qt.Key_F1:
            self.show_help()

def main():
    app = QApplication(sys.argv)
    window = PDFMerger()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()