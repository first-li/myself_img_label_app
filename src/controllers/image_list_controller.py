import os
from src.core.handle_file import FileHandler
from src.controllers.signal_manager import SignalManager

class ImageListController:
    def __init__(self, project_data, view, signal_manager: SignalManager):
        self.project_data = project_data
        self.view = view
        self.signal_manager = signal_manager
        self.image_id_list = project_data.VIA_data["_via_image_id_list"]
        
        # 连接视图信号
        self.view.add_button.clicked.connect(self.add_images)
        self.view.list_widget.itemSelectionChanged.connect(self.handle_image_selection)

    def update_load_image_list(self):
        """更新并加载图像列表"""
        self.image_id_list = self.project_data.VIA_data["_via_image_id_list"]
        self.view.list_widget.clear()
        # Get filenames from metadata instead of using IDs
        filenames = [
            self.project_data.VIA_data["_via_img_metadata"][img_id]["filename"]
            for img_id in self.image_id_list
        ]
        self.view.list_widget.addItems(filenames)

    def handle_image_selection(self):
        """处理图像选择事件"""
        selected_items = self.view.list_widget.selectedItems()
        if selected_items:
            selected_filename = selected_items[0].text()
            print(f"Selected filename: {selected_filename}")  # 调试信息
            # Find the ID corresponding to the selected filename
            image_id = next(
                (img_id for img_id in self.image_id_list 
                 if self.project_data.VIA_data["_via_img_metadata"][img_id]["filename"] == selected_filename),
                None
            )
            print(f"Found image ID: {image_id}")  # 调试信息
            if image_id:
                image_path = os.path.normpath(os.path.join(self.project_data.images_dir_path, selected_filename))  # 规范化路径
                print(f"Image path: {image_path}")  # 调试信息
                self.signal_manager.image_selected.emit(image_path)

    def add_images(self):
        """添加图像文件"""
        from PySide6.QtWidgets import QFileDialog
        
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            new_image_list = []
            
            # 处理已存在图像
            for existing_id in self.project_data.VIA_data["_via_image_id_list"]:
                filename = self.project_data.VIA_data["_via_img_metadata"][existing_id]["filename"]
                if any(os.path.basename(fp) == filename for fp in file_paths):
                    new_image_list.append(existing_id)
            
            # 添加新图像
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                if not any(self.project_data.VIA_data["_via_img_metadata"][id]["filename"] == filename 
                          for id in self.project_data.VIA_data["_via_image_id_list"]):
                    file_size = FileHandler.get_image_pixel_count(file_path)
                    new_id = f"{filename}{file_size}"
                    new_image_list.append(new_id)
                    self.project_data.VIA_data["_via_img_metadata"][new_id] = {
                        "filename": filename,
                        "size": file_size,
                        "regions": []
                    }
            
            # 设置图像目录路径（使用共同的父目录）
            if file_paths:
                common_dir = os.path.commonpath(file_paths)
                self.project_data.images_dir_path = common_dir if os.path.isdir(common_dir) else os.path.dirname(file_paths[0])
            
            # 更新数据并通知
            self.project_data.VIA_data["_via_image_id_list"] = new_image_list
            self.update_load_image_list()
            self.signal_manager.images_added.emit(file_paths)
