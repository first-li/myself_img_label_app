from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush
from PySide6.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QVBoxLayout, QGraphicsPixmapItem, \
    QGraphicsRectItem


class ImageCanvas(QWidget):
    """整合图像显示和标注功能的画布"""
    def __init__(self, ):
        super().__init__()
        self._set_ui()

    def _set_ui(self):
        # 创建场景和视图
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self)
        self.view.setScene(self.scene)
        # 设置拖动模式
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        # 设置resizeAnchor
        self.view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        # 设置布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        # 设置场景大小
        self.scene.setSceneRect(0, 0, 800, 600)

        # 初始化图像项和标注项
        self.image_item = None
        self.annotation_item = None

    def create_image_item(self, pixmap):
        """创建新的图像项"""
        # 清除旧图像和标注
        self.scene.clear()
        
        # 创建新的图像项
        self.image_item = QGraphicsPixmapItem()
        self.image_item.setPixmap(pixmap)
        self.scene.addItem(self.image_item)
        
        # 创建新的标注层
        self.annotation_item = QGraphicsRectItem(self.image_item)
        # 设置画笔为红色半透明边框
        pen = QPen(QColor(255, 0, 0, 128))  # 半透明红色
        pen.setWidth(2)
        self.annotation_item.setPen(pen)

        # 设置画刷为半透明红色填充
        brush = QBrush(QColor(255, 0, 0, 64))  # 半透明红色
        self.annotation_item.setBrush(brush)

        # 设置标注项初始位置和大小
        self.annotation_item.setRect(0, 0, 0, 0)
