import os
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, 
                             QMessageBox, QFrame)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class POCGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DudeSuite-POC生成")
        self.setGeometry(100, 100, 900, 700)
        self.setWindowIcon(QIcon("poc_icon.png"))  # 替换为您自己的图标文件
        
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-weight: bold;
                color: #333;
                margin-top: 5px;
            }
            QLineEdit, QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #4d90fe;
            }
            QPushButton {
                background-color: #4d90fe;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #357ae8;
            }
            QPushButton:pressed {
                background-color: #2d5bbf;
            }
            QPushButton#clear_btn {
                background-color: #f44336;
            }
            QPushButton#clear_btn:hover {
                background-color: #d32f2f;
            }
            QPushButton#clear_btn:pressed {
                background-color: #b71c1c;
            }
            QFrame {
                background-color: white;
                border-radius: 6px;
                border: 1px solid #ddd;
            }
        """)
        
        self.initUI()
    
    def initUI(self):
        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("POC生成工具")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            color: #333;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title_label)
        
        # 创建滚动区域容器
        scroll_content = QWidget()
        scroll_content.setLayout(QVBoxLayout())
        scroll_content.layout().setContentsMargins(0, 0, 0, 0)
        scroll_content.layout().setSpacing(15)
        
        # 基本信息框架
        info_frame = QFrame()
        info_frame.setLayout(QVBoxLayout())
        info_frame.layout().setContentsMargins(15, 15, 15, 15)
        info_frame.layout().setSpacing(10)
        
        # 漏洞名称
        info_frame.layout().addWidget(QLabel("漏洞名称:"))
        self.vuln_name = QLineEdit()
        self.vuln_name.setPlaceholderText("请输入漏洞名称")
        info_frame.layout().addWidget(self.vuln_name)
        
        # 漏洞编号
        info_frame.layout().addWidget(QLabel("漏洞编号:"))
        self.vuln_id = QLineEdit()
        self.vuln_id.setPlaceholderText("例如: CVE-2023-XXXX")
        info_frame.layout().addWidget(self.vuln_id)
        
        # 漏洞说明
        info_frame.layout().addWidget(QLabel("漏洞说明:"))
        self.vuln_desc = QTextEdit()
        self.vuln_desc.setMaximumHeight(80)
        self.vuln_desc.setPlaceholderText("简要描述漏洞的详细信息")
        info_frame.layout().addWidget(self.vuln_desc)
        
        # 漏洞特征
        info_frame.layout().addWidget(QLabel("漏洞特征:"))
        self.vuln_feature = QTextEdit()
        self.vuln_feature.setMaximumHeight(80)
        self.vuln_feature.setPlaceholderText("描述漏洞的特征或识别方法")
        info_frame.layout().addWidget(self.vuln_feature)
        
        scroll_content.layout().addWidget(info_frame)
        
        # 请求响应框架
        req_resp_frame = QFrame()
        req_resp_frame.setLayout(QVBoxLayout())
        req_resp_frame.layout().setContentsMargins(15, 15, 15, 15)
        req_resp_frame.layout().setSpacing(10)
        
        # 请求包内容
        req_resp_frame.layout().addWidget(QLabel("请求包内容:"))
        self.request_content = QTextEdit()
        self.request_content.setPlaceholderText("粘贴HTTP请求包内容")
        req_resp_frame.layout().addWidget(self.request_content)
        
        # 响应代码
        req_resp_frame.layout().addWidget(QLabel("响应代码:"))
        self.response_code = QLineEdit("*")
        self.response_code.setPlaceholderText("默认*表示任意响应码")
        req_resp_frame.layout().addWidget(self.response_code)
        
        # 响应特征
        req_resp_frame.layout().addWidget(QLabel("响应特征:"))
        self.response_feature = QTextEdit()
        self.response_feature.setMaximumHeight(80)
        self.response_feature.setPlaceholderText("描述响应中的特征或指纹")
        req_resp_frame.layout().addWidget(self.response_feature)
        
        # 文件定位
        req_resp_frame.layout().addWidget(QLabel("文件定位:"))
        self.file_location = QLineEdit()
        self.file_location.setPlaceholderText("漏洞相关文件位置")
        req_resp_frame.layout().addWidget(self.file_location)
        
        scroll_content.layout().addWidget(req_resp_frame)
        
        # 按钮布局
        button_frame = QFrame()
        button_frame.setLayout(QHBoxLayout())
        button_frame.layout().setContentsMargins(0, 0, 0, 0)
        button_frame.layout().setSpacing(15)
        
        self.generate_btn = QPushButton("生成POC")
        self.generate_btn.clicked.connect(self.generate_poc)
        button_frame.layout().addWidget(self.generate_btn)
        
        self.clear_btn = QPushButton("清空")
        self.clear_btn.setObjectName("clear_btn")
        self.clear_btn.clicked.connect(self.clear_fields)
        button_frame.layout().addWidget(self.clear_btn)
        
        button_frame.layout().addStretch()
        
        scroll_content.layout().addWidget(button_frame)
        scroll_content.layout().addStretch()
        
        main_layout.addWidget(scroll_content)
        main_widget.setLayout(main_layout)
    
    def generate_poc(self):
        # 获取各个字段的值
        vuln_name = self.vuln_name.text().strip()
        if not vuln_name:
            QMessageBox.warning(self, "警告", "漏洞名称不能为空!")
            return
        
        vuln_id = self.vuln_id.text().strip()
        vuln_desc = self.vuln_desc.toPlainText().strip()
        vuln_feature = self.vuln_feature.toPlainText().strip()
        request_content = self.request_content.toPlainText().strip()
        response_code = self.response_code.text().strip()
        response_feature = self.response_feature.toPlainText().strip()
        file_location = self.file_location.text().strip()
        
        # 清理请求内容中的特定头部
        request_lines = request_content.split('\n')
        cleaned_request = []
        for line in request_lines:
            if not any(line.lower().startswith(header) for header in ['host:', 'user-agent:', 'content-length:']):
                cleaned_request.append(line)
        cleaned_request_content = '\n'.join(cleaned_request)
        
        # 构建POC内容 - 即使字段为空也保留标题结构
        poc_content = f"## {vuln_name}\n\n"
        
        poc_content += f"> 漏洞编号：{vuln_id if vuln_id else ''}\n\n"
        
        poc_content += f"> 漏洞说明：{vuln_desc if vuln_desc else ''}\n\n"
        
        poc_content += f"> 漏洞特征：{vuln_feature if vuln_feature else ''}\n"
        
        poc_content += f"```\n"
        poc_content += cleaned_request_content if cleaned_request_content else "请求包内容为空"
        poc_content += "\n```\n\n"
        
        poc_content += f"> 响应代码：{response_code if response_code else ''}\n\n"
        
        poc_content += f"> 响应特征：{response_feature if response_feature else ''}\n\n"
        
        poc_content += f"> 文件定位：{file_location if file_location else ''}\n\n"
        
        
        # 保存文件
        filename = f"{vuln_name}.poc.md"
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存POC文件", filename, "Markdown Files (*.md);;All Files (*)", options=options)
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(poc_content)
                QMessageBox.information(self, "成功", f"POC文件已成功生成:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件时出错:\n{str(e)}")
    
    def clear_fields(self):
        self.vuln_name.clear()
        self.vuln_id.clear()
        self.vuln_desc.clear()
        self.vuln_feature.clear()
        self.request_content.clear()
        self.response_code.setText("*")
        self.response_feature.clear()
        self.file_location.clear()

if __name__ == "__main__":
    app = QApplication([])
    
    # 设置应用程序字体
    font = QFont()
    font.setFamily("Microsoft YaHei")  # 使用微软雅黑字体
    font.setPointSize(10)
    app.setFont(font)
    
    window = POCGenerator()
    window.show()
    app.exec_()