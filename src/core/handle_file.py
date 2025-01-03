import json
import os
import chardet
from PIL import Image
from PySide6.QtWidgets import QMessageBox
from src.utils.logger import logger


class FileHandler:
    def __init__(self, signal_manager):
        self.signal_manager = signal_manager

    def load_file_with_encoding(self, file_path):
        """加载JSON文件内容"""
        try:
            # 使用UTF-8编码读取文件内容
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)  # 直接解析JSON文件
                logger.info(f"成功加载JSON文件: {file_path}")

            # 触发数据加载完成信号
            self.signal_manager.data_loaded.emit()
            return data

        except Exception as e:
            # 显示错误消息
            QMessageBox.critical(None, "错误", f"文件加载失败: {str(e)}")
            logger.error(f"文件加载失败: {str(e)}")
            return None

    @staticmethod
    def get_image_pixel_count(image_path):
        """
        获取图像文件大小

        :param image_path: 图像文件路径
        :return: 图像文件大小（字节数）
        """
        try:
            return os.path.getsize(image_path)
        except Exception as e:
            logger.error(f"无法获取文件大小: {str(e)}")
            return None
