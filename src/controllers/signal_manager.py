from PySide6.QtCore import QObject, Signal

class SignalManager(QObject):
    """信号管理类，集中管理图像、标签和画布之间的信号交互"""
    
    # 图像相关信号
    images_added = Signal(list)  # 添加新图像时触发，参数为图像路径列表
    image_selected = Signal(str)  # 选择图像时触发，参数为图像路径
    image_removed = Signal(str)  # 删除图像时触发，参数为图像路径
    
    # 标签相关信号
    labels_added = Signal(list)  # 添加新标签时触发，参数为标签列表
    label_selected = Signal(str)  # 选择标签时触发，参数为标签名称
    label_removed = Signal(str)  # 删除标签时触发，参数为标签名称
    label_changed = Signal(str)  # 标签修改时触发，参数为标签ID
    label_deleted = Signal(str)  # 标签删除时触发，参数为标签ID
    default_label_changed = Signal(str)  # 默认标签改变时触发，参数为标签ID
    
    # 画布相关信号
    canvas_updated = Signal()  # 画布更新时触发
    canvas_cleared = Signal()  # 画布清空时触发
    canvas_zoomed = Signal(float)  # 画布缩放时触发，参数为缩放因子
    canvas_panned = Signal(float, float)  # 画布平移时触发，参数为x,y偏移量
    shape_changed = Signal(str)  # 形状改变时触发，参数为形状类型
    shape_updated = Signal(str)  # 形状更新时触发，参数为形状类型
    shape_drawn = Signal(dict)  # 形状绘制完成时触发，参数为形状信息字典
    
    # 数据加载信号
    data_loaded = Signal()  # 数据加载完成时触发
    
    def __init__(self):
        super().__init__()
        
    def connect_image_signals(self, image_list_controller):
        """连接图像相关信号"""
        image_list_controller.images_added.connect(self.images_added)
        image_list_controller.image_selected.connect(self.image_selected)
        image_list_controller.image_removed.connect(self.image_removed)
    
    def connect_label_signals(self, label_list_controller):
        """连接标签相关信号"""
        label_list_controller.labels_added.connect(self.labels_added)
        label_list_controller.label_selected.connect(self.label_selected)
        label_list_controller.label_removed.connect(self.label_removed)
    
    def connect_canvas_signals(self, canvas_controller):
        """连接画布相关信号"""
        canvas_controller.canvas_updated.connect(self.canvas_updated)
        canvas_controller.canvas_cleared.connect(self.canvas_cleared)
        
        # 连接变换信号
        self.canvas_zoomed.connect(canvas_controller.sync_transform)
        self.canvas_panned.connect(canvas_controller.sync_transform)
