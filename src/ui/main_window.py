from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSizePolicy, QSplitter, QHBoxLayout

from src.controllers.canvas_controller import CanvasController
from src.ui.canvas_ui import ImageCanvas
from src.ui.image_ui import ImageListWidget
from src.ui.label_ui import LabelListWidget
from src.ui.tool_bar import Toolbar

from src.core.handle_file import FileHandler
from src.core.project_data import ProjectData
from src.controllers.signal_manager import SignalManager

from src.controllers.toolbar_controller import ToolbarController
from src.controllers.image_list_controller import ImageListController
from src.controllers.label_list_controller import LabelListController


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self, config=None):
        super().__init__()
        self.signal_manager = SignalManager()
        self.project_data = ProjectData()
        
        self.label_list_Widget = LabelListWidget()  # 标签列表组件
        self.label_list_Widget_controller = LabelListController(
            self.project_data, 
            self.label_list_Widget,
            self.signal_manager
        )

        self.file_handler = FileHandler(self.signal_manager)
        self.toolbar = Toolbar(self.signal_manager)  # 将 signal_manager 传递给 Toolbar

        self.image_list_Widget = ImageListWidget()  # 图片列表组件
        self.image_list_Widget_controller = ImageListController(
            self.project_data, 
            self.image_list_Widget,
            self.signal_manager
        )

        self.canvas_widget = ImageCanvas()  # 画布组件
        self.canvas_widget_controller = CanvasController(
            self.project_data, 
            self.canvas_widget,
            self.signal_manager
        )

        self.toolbar_controller = ToolbarController(
            self.file_handler,
            self.project_data,
            self.toolbar,
            self.image_list_Widget_controller,
            self.label_list_Widget_controller
        )


        self.setWindowTitle("标注工具")
        # 设置窗口图标
        self.setWindowIcon(QIcon('assets/logo.ico'))
        self.window_width = 1200
        self.window_height = 800
        self.resize(self.window_width, self.window_height) if config is None else self.resize(config.window_width, config.window_height)
        # 设置主布局
        self.setup_main_layout()

    def setup_main_layout(self):
        """设置主布局"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 添加工具栏
        main_layout.addWidget(self.toolbar)

        # 创建水平布局用于放置左侧面板和图像列表
        content_layout = QHBoxLayout()
        # 左侧面板
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setMinimumWidth(200)

        # 创建分隔条
        splitter = QSplitter(Qt.Vertical)
        left_layout.addWidget(splitter)

        # 添加图像列表到分隔条并设置大小
        self.image_list_Widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        splitter.addWidget(self.image_list_Widget)

        # 添加标签类别列表到分隔条
        self.label_list_Widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        splitter.addWidget(self.label_list_Widget)

        # 设置分隔条的初始大小比例
        splitter.setStretchFactor(0, 1)  # 图像列表占 1
        splitter.setStretchFactor(1, 1)  # 标签管理器占 1

        content_layout.addWidget(left_panel)

        # 中间的标注区域
        self.canvas_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        content_layout.addWidget(self.canvas_widget)
        # 将内容布局添加到主布局
        main_layout.addLayout(content_layout)
