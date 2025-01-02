from PySide6.QtGui import QPixmap

class CanvasController:
    def __init__(self, project_data, view):
        self.project_data = project_data
        self.view = view

    def display_image(self, image_path):
        """在canvas上显示图像"""
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.view.canvas.setPixmap(pixmap)
                self.view.canvas.setScaledContents(True)
