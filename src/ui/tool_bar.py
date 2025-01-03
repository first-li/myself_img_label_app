from PySide6.QtWidgets import QToolBar, QMenu, QToolButton
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, QAction
from src.controllers.signal_manager import SignalManager


class Toolbar(QToolBar):
    """工具栏类"""
    def __init__(self, signal_manager):
        super().__init__()
        self.signal_manager = signal_manager
        self.zoom_fit_action = None
        self.save_action = None
        self.load_menu_item3 = None
        self.load_menu_item2 = None
        self.load_menu_item1 = None
        self.load_menu_items = None
        self.load_menu = None
        self.tool_button = None
        self.setup_tools()

    def setup_tools(self):
        """设置工具"""

        # 创建菜单并添加菜单项
        # 创建 QToolButton 并设置菜单
        self.tool_button = QToolButton(self)
        self.tool_button.setText("加载项目")  # 设置按钮文本

        self.load_menu = QMenu(self)
        self.load_menu_items = ["加载json", "加载json(VIA)", "加载json(COCO)"]

        self.load_menu_item1 = QAction(self.load_menu_items[0], self)
        self.load_menu.addAction(self.load_menu_item1)

        self.load_menu_item2 = QAction(self.load_menu_items[1], self)
        self.load_menu.addAction(self.load_menu_item2)

        self.load_menu_item3 = QAction(self.load_menu_items[2], self)
        self.load_menu.addAction(self.load_menu_item3)

        self.tool_button.setMenu(self.load_menu)  # 设置菜单
        self.tool_button.setPopupMode(QToolButton.InstantPopup)  # 设置点击按钮时直接弹出菜单

        # 将 QToolButton 添加到工具栏
        self.addWidget(self.tool_button)

        # 工具
        self.save_action  = QAction("保存项目", self)
        self.save_action .setCheckable(True)
        self.addAction(self.save_action )

        self.zoom_fit_action = QAction("适应窗口", self)
        self.addAction(self.zoom_fit_action)

        # 添加形状菜单
        self.shape_button = QToolButton(self)
        self.shape_button.setText("形状")

        self.shape_menu = QMenu(self)
        self.shape_actions = ["矩形框", "点", "多边形"]

        self.rect_action = QAction(self.shape_actions[0], self)
        self.rect_action.setCheckable(True)
        self.rect_action.setChecked(True)
        self.rect_action.triggered.connect(lambda: self.signal_manager.shape_changed.emit("rect"))
        self.shape_menu.addAction(self.rect_action)

        self.point_action = QAction(self.shape_actions[1], self)
        self.shape_menu.addAction(self.point_action)

        self.polygon_action = QAction(self.shape_actions[2], self)
        self.shape_menu.addAction(self.polygon_action)

        self.shape_button.setMenu(self.shape_menu)
        self.shape_button.setPopupMode(QToolButton.InstantPopup)
        self.addWidget(self.shape_button)
