from PySide6.QtWidgets import QFileDialog, QMessageBox
from src.utils.logger import logger


class ToolbarController:
    def __init__(self, file_handler, project_data, view, image_list_controller):
        self.file_handler = file_handler
        self.project_data = project_data
        self.view = view
        self.image_list_controller = image_list_controller

        self.view.save_action.triggered.connect(self.on_save_project_triggered)
        self.view.zoom_fit_action.triggered.connect(self.on_zoom_fit_triggered)
        self.view.load_menu_item1.triggered.connect(self.on_load_submenu_item1_triggered)
        self.view.load_menu_item2.triggered.connect(self.on_load_submenu_item2_triggered)
        self.view.load_menu_item3.triggered.connect(self.on_load_submenu_item3_triggered)


    def on_save_project_triggered(self):
        logger.info("保存项目被触发")

    def on_zoom_fit_triggered(self):
        logger.info("适应窗口被触发")

    def on_load_submenu_item1_triggered(self):
        logger.info("加载json triggered")
        self.project_data.refresh()
        self.open_file_dialog("JSON 文件 (*.json)")
        self.image_list_controller.update_load_image_list()

    def on_load_submenu_item2_triggered(self):
        logger.info("加载json(VIA) triggered")
        self.project_data.refresh()
        self.open_file_dialog("JSON 文件 (*.json)")
        self.image_list_controller.update_load_image_list()

    def on_load_submenu_item3_triggered(self):
        logger.info("加载json(COCO) triggered")
        self.open_file_dialog("JSON 文件 (*.json)")

    def open_file_dialog(self, file_filter):
        """打开文件选择对话框"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None,  # 父窗口
            "选择文件",  # 对话框标题
            "",  # 初始目录
            file_filter  # 文件过滤器
        )
        if file_path:
            logger.info(f"选择的文件路径: {file_path}")
            self.project_data.VIA_data = self.file_handler.load_file_with_encoding(file_path)
            self.project_data.json_file_path = file_path




