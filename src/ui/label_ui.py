from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                              QPushButton, QScrollArea, QRadioButton, QDialog, QColorDialog)
from PySide6.QtGui import QColor
import random
import colorsys


class LabelListWidget(QWidget):
    """图像列表组件"""
    def __init__(self):
        super().__init__()
        self.labels_layout = None
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout()

        # 标签管理按钮区域
        button_layout = QHBoxLayout()

        # 添加标签按钮
        self.add_button = QPushButton("添加标签")
        button_layout.addWidget(self.add_button)

        # 添加默认标签按钮
        self.default_button = QPushButton("添加默认标签")
        button_layout.addWidget(self.default_button)

        layout.addLayout(button_layout)

        # 标签列表区域
        self.labels_layout = QVBoxLayout()
        labels_widget = QWidget()
        labels_widget.setLayout(self.labels_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(labels_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

    def create_label_row(self, label_id, label_name, color):
        """创建标签行"""
        # 创建行容器
        row = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row.setLayout(row_layout)
        
        # 单选按钮
        radio_button = QRadioButton()
        radio_button.setObjectName(f"radio_{label_id}")
        row_layout.addWidget(radio_button)
        
        # 标签名称
        name_label = QLabel(f"{label_id}. {label_name}")
        name_label.setObjectName(f"label_{label_id}")
        row_layout.addWidget(name_label)
        
        # 颜色按钮
        color_button = QPushButton()
        color_button.setObjectName(f"color_{label_id}")
        color_button.setFixedSize(20, 20)
        color_button.setStyleSheet(f"background-color: {color}")
        row_layout.addWidget(color_button)
        
        # 删除按钮
        delete_button = QPushButton("×")
        delete_button.setObjectName(f"delete_{label_id}")
        delete_button.setFixedSize(20, 20)
        row_layout.addWidget(delete_button)
        
        self.labels_layout.addWidget(row)
        return row

    def clear_labels(self):
        """清空所有标签"""
        while self.labels_layout.count():
            item = self.labels_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


class AddLabelDialog(QDialog):
    """添加标签对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加标签")
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        
        # 标签名称输入
        name_label = QLabel("标签名称:")
        self.name_edit = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(self.name_edit)
        
        # 确定取消按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

    def get_label_name(self):
        """获取输入的标签名称"""
        return self.name_edit.text().strip()
