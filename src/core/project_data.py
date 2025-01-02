import datetime


class ProjectData:
    """项目数据管理类"""

    def __init__(self):
        """初始化项目数据"""
        self.refresh()

    def refresh(self):
        """刷新项目数据到初始状态"""
        # 获取当前时间的时间戳
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # 将时间戳添加到项目名称中
        self.default_project_name = f"project_{self.timestamp}"
        self.json_file_path = f"{self.default_project_name}.json"
        self.images_dir_path = None
        self.one_image_regions = {   # 该字典要赋值给image_id
                    "filename": "",  # str 图片文件名
                    "size": 0,  # int 类型，图片大小，单位为像素
                    "regions": [  # 一系列字典的元素，self.region_format
                    ],
                    "file_attributes": {}
                }
        self.obj_class = {
                        "type": "dropdown",
                        "description": "",
                        "options": {  # 键值对，序号： 类别描述
                        },
                        "default_options": {}
                    }
        self.region_format = {
                            "shape_attributes": {
                                "name": "",  # str 类型，表示形状类型，例如 "rect"、"circle"、"polygon" 等
                                "x": 0,    # int 类型，表示形状的左上角 x 坐标
                                "y": 0,    # int 类型，表示形状的左上角 y 坐标
                                "width": 0,   # int 类型，表示形状的宽度
                                "height": 0  # int 类型，表示形状的高度
                            },
                            "region_attributes": {
                                "obj": ""  # str 类型，表示该区域对应的对象类别
                            }
                        }
        self.VIA_data = {
            "_via_settings": {
                "ui": {
                    "annotation_editor_height": 25,
                    "annotation_editor_fontsize": 0.8,
                    "leftsidebar_width": 18,
                    "image_grid": {
                        "img_height": 80,
                        "rshape_fill": "none",
                        "rshape_fill_opacity": 0.3,
                        "rshape_stroke": "yellow",
                        "rshape_stroke_width": 2,
                        "show_region_shape": True,
                        "show_image_policy": "all"
                    },
                    "image": {
                        "region_label": "__via_region_id__",
                        "region_color": "__via_default_region_color__",
                        "region_label_font": "10px Sans",
                        "on_image_annotation_editor_placement": "NEAR_REGION"
                    }
                },
                "core": {
                    "buffer_size": 18,
                    "filepath": {},
                    "default_filepath": ""
                },
                "project": {
                    "name": self.default_project_name
                }
            },
            "_via_img_metadata": {},
            "_via_attributes": {
                "region": {
                    "obj": self.obj_class
                },
                "file": {}
            },
            "_via_data_format_version": "2.0.10",
            "_via_image_id_list": []
        }
