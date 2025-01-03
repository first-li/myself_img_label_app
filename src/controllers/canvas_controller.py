import os
from PySide6.QtCore import Qt, QObject, QEvent
from PySide6.QtGui import QPixmap, QColor, QPen, QBrush
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsView
from src.controllers.signal_manager import SignalManager
from src.core.handle_file import FileHandler


class CanvasController(QObject):
    def __init__(self, project_data, view, signal_manager: SignalManager):
        super().__init__()
        self.project_data = project_data
        self.view = view
        self.signal_manager = signal_manager
        self._resize_timer = None
        self._is_fitted = False
        
        # 连接形状相关信号
        self.signal_manager.shape_changed.connect(self.set_shape)
        self.signal_manager.shape_drawn.connect(self._handle_shape_drawn)
        
        # 初始化变换参数
        self.scale_factor = 1.0
        self.last_mouse_pos = None
        
        # 初始化绘制状态
        self.drawing = False
        self.start_point = None
        self.current_shape = "rect"  # 默认绘制矩形
        
        # 连接信号
        self.signal_manager.images_added.connect(self.handle_images_added)
        self.signal_manager.image_selected.connect(self.display_image)
        self.signal_manager.canvas_updated.connect(self.sync_transform)
        
        # 连接视图事件
        self.view.view.wheelEvent = self.handle_wheel_event
        self.view.view.mousePressEvent = self.handle_mouse_press
        self.view.view.mouseMoveEvent = self.handle_mouse_move
        self.view.view.mouseReleaseEvent = self.handle_mouse_release
        
        # 连接窗口大小变化信号
        self.view.view.viewport().installEventFilter(self)
        
        # 启用视图交互和滚动条
        self.view.view.setMouseTracking(True)
        self.view.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def handle_images_added(self, paths):
        """处理新添加的图像"""
        if paths:
            self.display_image(paths[0])

    def display_image(self, image_path):
        """在canvas上显示图像"""
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # 调用UI层方法创建图像项
                self.view.create_image_item(pixmap)
                
                # 更新当前图片路径
                self.current_image_path = image_path
                
                # 更新标注层
                self.update_annotations(image_path)
                
                # 设置基本视图属性
                self.view.view.setSceneRect(self.view.image_item.boundingRect())
                
                # Only fit view if not already fitted
                if not self._is_fitted:
                    self._fit_to_view()
                    self._is_fitted = True
                
                # 触发更新
                self.signal_manager.canvas_updated.emit()

    def _fit_to_view(self):
        """自适应窗口大小，保持图片比例"""
        from src.utils.logger import logger
        
        # 检查图像项和视图是否有效
        if not self.view or not self.view.image_item or self.view.image_item.pixmap().isNull():
            logger.warning("Fit to view failed: invalid view or image item")
            return
            
        logger.info(f"Fitting image to view. Image size: {self.view.image_item.pixmap().size()}")
        
        # 获取视图和图像尺寸
        view_rect = self.view.view.viewport().rect()
        img_size = self.view.image_item.pixmap().size()
        
        # 计算保持比例的缩放因子
        width_ratio = view_rect.width() / img_size.width()
        height_ratio = view_rect.height() / img_size.height()
        
        # 根据图像大小选择不同的缩放策略
        if img_size.width() < view_rect.width() and img_size.height() < view_rect.height():
            # 小图：按原尺寸显示
            scale = 1.0
        else:
            # 大图：按比例缩放以适应窗口
            scale = min(width_ratio, height_ratio) * 0.9  # 留出10%的边距
            
        # 重置变换
        self.view.view.resetTransform()
        
        # 应用缩放
        self.view.view.scale(scale, scale)
        
        # 居中显示
        self.view.view.centerOn(self.view.image_item)
        
        logger.info(f"Applied scale: {scale}, Image size after scaling: {img_size * scale}")

    def _draw_annotation(self, x, y, width, height):
        """绘制单个标注矩形"""
        # 获取图像边界
        img_rect = self.view.image_item.boundingRect()
        
        # 限制标注区域在图像范围内
        x = max(0, min(x, img_rect.width() - width))
        y = max(0, min(y, img_rect.height() - height))
        width = min(width, img_rect.width() - x)
        height = min(height, img_rect.height() - y)
        
        # 创建矩形并设置样式，作为图像项的子项
        rect_item = QGraphicsRectItem(x, y, width, height, self.view.image_item)
        rect_item.setPen(QPen(QColor(255, 0, 0, 128)))  # 半透明红色边框
        rect_item.setBrush(QBrush(QColor(255, 0, 0, 64)))  # 半透明红色填充
        
        # 设置Z值确保标注在图像上方
        rect_item.setZValue(1)
        
        # 确保标注可见
        rect_item.setVisible(True)

    def handle_wheel_event(self, event):
        """处理滚轮缩放事件"""
        if event.modifiers() & Qt.ControlModifier:
            # 计算缩放因子
            zoom_factor = 1.25
            if event.angleDelta().y() < 0:
                zoom_factor = 1.0 / zoom_factor
            
            # 检查最大缩放限制（20倍）
            MAX_ZOOM = 20.0
            MIN_ZOOM = 0.05  # 5% minimum zoom
            
            # 计算新缩放比例
            new_scale = self.scale_factor * zoom_factor
            
            # 限制缩放范围
            if new_scale > MAX_ZOOM:
                new_scale = MAX_ZOOM
                zoom_factor = MAX_ZOOM / self.scale_factor
            elif new_scale < MIN_ZOOM:
                new_scale = MIN_ZOOM
                zoom_factor = MIN_ZOOM / self.scale_factor
            
            # 更新缩放比例
            self.scale_factor = new_scale
            
            # 重置变换
            self.view.view.resetTransform()
            
            # 应用缩放
            self.view.view.scale(self.scale_factor, self.scale_factor)
            
            # 更新视图变换
            transform = self.view.view.transform()
            self.view.view.setTransform(transform)
            
            # 强制更新所有元素
            self.view.view.scene().update()
            self.view.view.viewport().update()
            self.view.view.updateSceneRect(self.view.view.sceneRect())
            
            # 更新所有子项
            for item in self.view.view.items():
                item.setTransform(transform)
                item.update()
            
            # 确保立即重绘
            self.view.view.viewport().repaint()
            
            # 记录缩放信息
            from src.utils.logger import logger
            logger.info(f"Applied zoom: {zoom_factor}, Current scale: {self.scale_factor}")
            
            # 触发缩放信号
            self.signal_manager.canvas_zoomed.emit(self.scale_factor)
            
            # 同步变换
            self.sync_transform()
            
            # 确保立即重绘
            self.view.view.viewport().repaint()
            
            # 阻止事件继续传播
            event.accept()
        else:
            # 允许默认滚轮行为
            event.ignore()

    def handle_mouse_press(self, event):
        """处理鼠标按下事件"""
        if (event.button() == Qt.RightButton or self.scale_factor != 1.0):
            self.last_mouse_pos = event.pos()
            self.view.view.setCursor(Qt.ClosedHandCursor)
            event.accept()
        elif event.button() == Qt.LeftButton:
            # 检查点击位置是否在图像范围内
            pos = self.view.view.mapToScene(event.pos())
            if self.view.image_item and self.view.image_item.contains(pos):
                # 开始绘制
                self.drawing = True
                self.start_point = pos
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def handle_mouse_move(self, event):
        """处理鼠标移动事件"""
        if (event.buttons() & Qt.RightButton or self.scale_factor != 1.0) and self.last_mouse_pos is not None:
            # 获取当前鼠标位置
            current_pos = event.pos()
            
            # 计算移动距离（考虑缩放比例）
            delta = current_pos - self.last_mouse_pos
            self.last_mouse_pos = current_pos
            
            # 获取滚动条
            h_bar = self.view.view.horizontalScrollBar()
            v_bar = self.view.view.verticalScrollBar()
            
            # 计算新的滚动位置
            new_h_value = h_bar.value() - delta.x() * (1.0 / self.scale_factor)
            new_v_value = v_bar.value() - delta.y() * (1.0 / self.scale_factor)
            
            # 应用平移
            h_bar.setValue(new_h_value)
            v_bar.setValue(new_v_value)
            
            # 触发平移信号
            self.signal_manager.canvas_panned.emit(delta.x(), delta.y())
            
            # 强制更新视图
            self.view.view.viewport().update()
            self.view.view.update()
            event.accept()
        elif self.drawing and event.buttons() & Qt.LeftButton:
            # 绘制预览矩形
            current_point = self.view.view.mapToScene(event.pos())
            self._draw_preview(self.start_point, current_point)
            event.accept()

    def eventFilter(self, obj, event):
        """处理视图大小变化事件"""
        from shiboken6 import isValid
        from src.utils.logger import logger
        
        # Check if view objects still exist
        if (hasattr(self, 'view') and 
            hasattr(self.view, 'view') and 
            isValid(self.view.view) and 
            obj == self.view.view.viewport() and 
            event.type() == QEvent.Resize):
            
            if hasattr(self.view, 'image_item') and self.view.image_item:
                logger.info("Window resized, fitting view")
                self._fit_to_view()
                self._is_fitted = True
        return super().eventFilter(obj, event)

    def handle_mouse_release(self, event):
        """处理鼠标释放事件"""
        if event.button() == Qt.RightButton:
            self.last_mouse_pos = None
            self.view.view.setCursor(Qt.ArrowCursor)
            event.accept()
        elif event.button() == Qt.LeftButton and self.drawing:
            # 完成绘制
            end_point = self.view.view.mapToScene(event.pos())
            self._finalize_shape(self.start_point, end_point)
            self.drawing = False
            self.start_point = None
            
            # 清除预览框
            for item in self.view.scene.items():
                if hasattr(item, "is_preview") and item.is_preview:
                    self.view.scene.removeItem(item)
            
            event.accept()
        else:
            event.ignore()

    def sync_transform(self, *args):
        """同步图像和标注层的变换"""
        transform = self.view.view.transform()
        self.view.image_item.setTransform(transform)
        self.view.annotation_item.setTransform(transform)

    def _draw_preview(self, start_point, end_point):
        """绘制形状预览"""
        # 获取图像边界
        img_rect = self.view.image_item.boundingRect()
        
        # 计算预览矩形边界
        x = min(start_point.x(), end_point.x())
        y = min(start_point.y(), end_point.y())
        width = abs(end_point.x() - start_point.x())
        height = abs(end_point.y() - start_point.y())
        
        # 限制预览区域在图像范围内
        x = max(0, min(x, img_rect.width() - width))
        y = max(0, min(y, img_rect.height() - height))
        width = min(width, img_rect.width() - x)
        height = min(height, img_rect.height() - y)
        
        # 清除之前的预览
        for item in self.view.scene.items():
            if hasattr(item, "is_preview") and item.is_preview:
                self.view.scene.removeItem(item)
        
        # 根据当前形状类型绘制预览
        if self.current_shape == "rect":
            rect = QGraphicsRectItem()
            rect.setRect(x, y, width, height)
            rect.setPen(QPen(QColor(0, 255, 0, 128)))  # 半透明绿色
            rect.is_preview = True
            self.view.scene.addItem(rect)
            
    def _finalize_shape(self, start_point, end_point):
        """完成形状绘制"""
        if self.current_shape == "rect":
            # 将场景坐标转换为图像项局部坐标
            start_local = self.view.image_item.mapFromScene(start_point)
            end_local = self.view.image_item.mapFromScene(end_point)
            
            # 使用局部坐标计算矩形
            x = min(start_local.x(), end_local.x())
            y = min(start_local.y(), end_local.y())
            width = abs(end_local.x() - start_local.x())
            height = abs(end_local.y() - start_local.y())
            
            # 获取图像边界
            img_rect = self.view.image_item.boundingRect()
            
            # 限制矩形区域在图像范围内
            x = max(0, min(x, img_rect.width() - width))
            y = max(0, min(y, img_rect.height() - height))
            width = min(width, img_rect.width() - x)
            height = min(height, img_rect.height() - y)
            
            # 绘制最终形状
            self._draw_annotation(x, y, width, height)
            
            # 触发更新信号
            self.signal_manager.shape_drawn.emit({
                "type": "rect",
                "x": x,
                "y": y,
                "width": width,
                "height": height
            })

    def _handle_shape_drawn(self, shape_data):
        """处理形状绘制完成信号
        
        Args:
            shape_data (dict): 包含形状信息的字典
        """
        # 将绘制的形状保存到项目数据中
        if hasattr(self, 'current_image_path') and self.current_image_path:
            # 获取文件名和文件大小
            filename = os.path.basename(self.current_image_path)
            file_size = FileHandler.get_image_pixel_count(self.current_image_path)
            
            # 生成图像ID
            image_id = f"{filename}{file_size}"
            
            # 创建区域数据
            region = {
                "shape_attributes": {
                    "name": shape_data["type"],
                    "x": shape_data["x"],
                    "y": shape_data["y"],
                    "width": shape_data["width"],
                    "height": shape_data["height"]
                },
                "region_attributes": {}
            }
            
            # 添加区域到当前图像
            if image_id not in self.project_data.VIA_data["_via_img_metadata"]:
                self.project_data.VIA_data["_via_img_metadata"][image_id] = {
                    "filename": filename,
                    "size": file_size,
                    "regions": []
                }
            self.project_data.VIA_data["_via_img_metadata"][image_id]["regions"].append(region)

    def set_shape(self, shape):
        """设置当前绘制形状
        
        Args:
            shape (str): 要设置的形状类型 ('rect', 'circle', etc.)
        """
        # 更新当前形状
        self.current_shape = shape
        
        # 清除任何现有的预览形状
        for item in self.view.scene.items():
            if hasattr(item, "is_preview") and item.is_preview:
                self.view.scene.removeItem(item)
        
        # 触发UI更新
        self.signal_manager.shape_updated.emit(shape)

    def update_annotations(self, image_path):
        """更新当前图像的标注层"""
        from src.core.handle_file import FileHandler
        from src.utils.logger import logger
        
        # 获取图像ID（文件名+文件大小）
        filename = os.path.basename(image_path)
        file_size = os.path.getsize(image_path)
        image_id = f"{filename}{file_size}"
        
        logger.info(f"Updating annotations for image: {image_path}")
        logger.info(f"Generated image ID: {image_id}")
        
        # 确保图像元数据存在
        if image_id not in self.project_data.VIA_data["_via_img_metadata"]:
            self.project_data.VIA_data["_via_img_metadata"][image_id] = {
                "filename": filename,
                "size": file_size,
                "regions": []
            }
        
        # 获取该图像的标注数据
        regions = self.project_data.VIA_data["_via_img_metadata"][image_id].get("regions", [])
        logger.info(f"Found {len(regions)} regions for image {image_id}")
        
        # 清除旧标注
        for item in self.view.scene.items():
            if isinstance(item, QGraphicsRectItem) and item != self.view.annotation_item:
                self.view.scene.removeItem(item)
        
        # 绘制新标注
        for i, region in enumerate(regions):
            shape_attributes = region["shape_attributes"]
            if shape_attributes["name"] == "rect":
                x = shape_attributes["x"]
                y = shape_attributes["y"]
                width = shape_attributes["width"]
                height = shape_attributes["height"]
                
                logger.info(f"Drawing region {i+1}: x={x}, y={y}, width={width}, height={height}")
                
                # 使用单独函数绘制标注
                self._draw_annotation(x, y, width, height)
