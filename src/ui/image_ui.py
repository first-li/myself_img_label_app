from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget


class ImageListWidget(QWidget):
    """图像列表组件"""
    def __init__(self):
        super().__init__()
        self.list_widget = None
        self.delete_button = None
        self.add_button = None
        self.project_name = None
        self.setup_ui()

    def setup_ui(self):
        """设置界面"""
        # 主布局
        layout = QVBoxLayout(self)

        # 标题和项目名称布局
        title_layout = QHBoxLayout()

        # # 标题
        # title_label = QLabel("图像列表")
        # title_layout.addWidget(title_label)

        # 项目名称
        project_layout = QHBoxLayout()
        project_label = QLabel("项目名称:")
        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("test")
        project_layout.addWidget(project_label)
        project_layout.addWidget(self.project_name)

        title_layout.addLayout(project_layout)
        layout.addLayout(title_layout)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 添加图像按钮
        self.add_button = QPushButton("添加图像")
        self.add_button.setToolTip("添加图像")
        button_layout.addWidget(self.add_button)

        # 删除图像按钮
        self.delete_button = QPushButton("删除图像")
        self.delete_button.setToolTip("删除选中的图像")
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        # 图像列表
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
