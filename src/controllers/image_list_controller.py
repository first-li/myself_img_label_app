import os


class ImageListController:
    def __init__(self, project_data, view):
        self.project_data = project_data
        self.view = view
        self.image_list = project_data.VIA_data["_via_image_id_list"]

    def update_load_image_list(self):
        self.image_list = self.project_data.VIA_data["_via_image_id_list"]
        self.view.list_widget.clear()  # 清空视图中的所有项
        self.view.list_widget.addItems(self.image_list)

    def load_image(self, index):
        """加载并显示指定索引的图像"""
        if 0 <= index < len(self.image_list):
            image_id = self.image_list[index]
            image_path = os.path.join(self.project_data.image_dir, image_id)
            
            # 通知canvas控制器显示图像
            if hasattr(self.view, 'canvas_controller'):
                self.view.canvas_controller.display_image(image_path)

    def add_images(self):
        """添加图像文件"""
        from PySide6.QtWidgets import QFileDialog
        from src.core.handle_file import load_image_files
        
        # 打开文件选择对话框
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        
        if file_dialog.exec():
            # 获取选择的文件路径
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                # 过滤已存在的图像
                existing_images = set(self.project_data.VIA_data["_via_image_id_list"])
                new_images = [path for path in file_paths 
                            if os.path.basename(path) not in existing_images]
                
                if new_images:
                    # 调用文件处理模块加载图像
                    load_image_files(self.project_data, new_images)
                    self.update_load_image_list()
                    
                    # 在canvas中显示第一个新图像
                    if new_images:
                        self.load_image(len(self.image_list) - len(new_images))
