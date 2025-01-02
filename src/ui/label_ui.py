from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QScrollArea


class LabelListWidget(QWidget):
    """图像列表组件"""
    def __init__(self, ):
        super().__init__()
        self.labels_layout = None
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout()

        # 标签管理按钮区域
        button_layout = QHBoxLayout()

        # 添加标签按钮
        add_button = QPushButton("添加标签")
        button_layout.addWidget(add_button)

        # 添加默认标签按钮
        default_button = QPushButton("添加默认标签")
        button_layout.addWidget(default_button)

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