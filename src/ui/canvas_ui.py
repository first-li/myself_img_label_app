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
        # 设置布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        # 设置场景大小
        self.scene.setSceneRect(0, 0, 800, 600)

        # 加载图像
        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)

        # 创建标注层
        self.annotation_item = QGraphicsRectItem()
        # 设置画笔为无边框
        pen = QPen(Qt.NoPen)
        self.annotation_item.setPen(pen)

        # 设置画刷为透明
        brush = QBrush(QColor(255, 0, 0, 0))  # 完全透明
        self.annotation_item.setBrush(brush)

        self.scene.addItem(self.annotation_item)