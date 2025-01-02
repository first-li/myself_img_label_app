from PySide6.QtWidgets import QToolBar, QMenu, QToolButton
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, QAction


class Toolbar(QToolBar):
    """工具栏类"""
    def __init__(self):
        super().__init__()
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
