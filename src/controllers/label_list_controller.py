from PySide6.QtWidgets import QColorDialog, QRadioButton, QPushButton, QLabel
from PySide6.QtGui import QColor
from src.ui.label_ui import AddLabelDialog
import random
import colorsys


class LabelListController:
    def __init__(self, project_data, view, signal_manager):
        self.project_data = project_data
        self.view = view
        self.signal_manager = signal_manager
        self.default_label_id = None
        self._connect_signals()
        self._setup_connections()

    def _connect_signals(self):
        """连接信号"""
        self.signal_manager.data_loaded.connect(self.update_label_list)

    def _setup_connections(self):
        """设置UI信号连接"""
        self.view.add_button.clicked.connect(self.show_add_label_dialog)
        self.view.default_button.clicked.connect(self.add_default_labels)

    def generate_random_color(self):
        """生成随机颜色"""
        h = random.random()
        s = 0.6 + random.random() * 0.4
        v = 0.6 + random.random() * 0.4
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )

    def update_label_list(self):
        """更新标签列表"""
        if not self.project_data.VIA_data:
            return
            
        self.view.clear_labels()
        
        if not self.project_data.VIA_data or "_via_attributes" not in self.project_data.VIA_data:
            return
            
        obj_class = self.project_data.VIA_data["_via_attributes"]["region"]["obj"]
        if not obj_class or not obj_class.get("options"):
            return
            
        # 添加新标签
        for label_id, label_name in obj_class["options"].items():
            color = self.generate_random_color()
            row = self.view.create_label_row(label_id, label_name, color)
            
            # 连接信号
            radio = row.findChild(QRadioButton)
            color_btn = row.findChild(QPushButton, f"color_{label_id}")
            delete_btn = row.findChild(QPushButton, f"delete_{label_id}")
            
            if radio:
                radio.clicked.connect(lambda _, id=label_id: self.set_default_label(id))
            if color_btn:
                color_btn.clicked.connect(lambda _, id=label_id: self.edit_label_color(id))
            if delete_btn:
                delete_btn.clicked.connect(lambda _, id=label_id: self.delete_label(id))

    def show_add_label_dialog(self):
        """显示添加标签对话框"""
        from PySide6.QtWidgets import QDialog
        
        dialog = AddLabelDialog(self.view)
        # 连接按钮信号
        dialog.ok_button.clicked.connect(dialog.accept)
        dialog.cancel_button.clicked.connect(dialog.reject)
        
        if dialog.exec_() == QDialog.Accepted:
            label_name = dialog.get_label_name()
            if label_name:
                self.add_label(label_name)

    def add_label(self, name, color=None):
        """添加新标签"""
        if not name:
            return
            
        if color is None:
            color = self.generate_random_color()
            
        # 生成新ID
        label_id = str(len(self.project_data.VIA_data["_via_attributes"]["region"]["obj"]["options"]) + 1)
        
        # 更新项目数据
        self.project_data.VIA_data["_via_attributes"]["region"]["obj"]["options"][label_id] = name
        
        # 更新UI
        row = self.view.create_label_row(label_id, name, color)
        
        # 如果是第一个标签，设为默认
        if len(self.project_data.VIA_data["_via_attributes"]["region"]["obj"]["options"]) == 1:
            self.set_default_label(label_id)
            
        # 连接信号
        radio = row.findChild(QRadioButton)
        color_btn = row.findChild(QPushButton, f"color_{label_id}")
        delete_btn = row.findChild(QPushButton, f"delete_{label_id}")
        
        if radio:
            radio.clicked.connect(lambda _, id=label_id: self.set_default_label(id))
        if color_btn:
            color_btn.clicked.connect(lambda _, id=label_id: self.edit_label_color(id))
        if delete_btn:
            delete_btn.clicked.connect(lambda _, id=label_id: self.delete_label(id))
            
        self.signal_manager.labels_added.emit([(label_id, name)])

    def edit_label_color(self, label_id):
        """编辑标签颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            # 更新UI
            color_btn = self.view.findChild(QPushButton, f"color_{label_id}")
            if color_btn:
                color_btn.setStyleSheet(f"background-color: {color.name()}")
            self.signal_manager.label_changed.emit(label_id)

    def delete_label(self, label_id):
        """删除标签"""
        # 从项目数据中删除
        if label_id in self.project_data.VIA_data["_via_attributes"]["region"]["obj"]["options"]:
            del self.project_data.VIA_data["_via_attributes"]["region"]["obj"]["options"][label_id]
            
        # 从UI中删除
        for i in reversed(range(self.view.labels_layout.count())):
            widget = self.view.labels_layout.itemAt(i).widget()
            if widget and widget.findChild(QLabel, f"label_{label_id}"):
                widget.deleteLater()
                break
                
        # 如果删除的是默认标签，重新选择默认
        if label_id == self.default_label_id:
            if self.view.labels_layout.count() > 0:
                first_widget = self.view.labels_layout.itemAt(0).widget()
                if first_widget:
                    first_radio = first_widget.findChild(QRadioButton)
                    if first_radio:
                        first_radio.setChecked(True)
                        self.default_label_id = first_widget.findChild(QLabel).text().split(".")[0]
            else:
                self.default_label_id = None
                
        self.signal_manager.label_deleted.emit(label_id)

    def set_default_label(self, label_id):
        """设置默认标签"""
        self.default_label_id = label_id
        self.signal_manager.default_label_changed.emit(label_id)

    def add_default_labels(self):
        """添加默认标签"""
        default_labels = {
            "1": "类别1",
            "2": "类别2", 
            "3": "类别3"
        }
        
        for label_id, label_name in default_labels.items():
            if label_id not in self.project_data.VIA_data["_via_attributes"]["region"]["obj"]["options"]:
                self.add_label(label_name, color=self.generate_random_color())
                
        if not self.default_label_id:
            self.set_default_label("1")
