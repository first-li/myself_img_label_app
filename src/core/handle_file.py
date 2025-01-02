import json

import chardet
from PySide6.QtWidgets import QMessageBox
from src.utils.logger import logger


class FileHandler:
    def __init__(self):
        pass

    def load_file_with_encoding(self, file_path):
        """根据文件编码加载文件内容"""
        try:
            # 检测文件编码
            with open(file_path, "rb") as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result["encoding"]
                confidence = result["confidence"]
                logger.info(f"检测到文件编码: {encoding} (置信度: {confidence})")

            # 使用检测到的编码读取文件内容
            with open(file_path, "r", encoding=encoding) as f:
                content = f.read()
                data = json.loads(content)  # 将 JSON 字符串解析为字典

            # # 显示成功消息
            # QMessageBox.information(None, "成功", f"文件加载成功！\n编码: {encoding}")
            return data

        except Exception as e:
            # 显示错误消息
            QMessageBox.critical(None, "错误", f"文件加载失败: {str(e)}")
            logger.error(f"文件加载失败: {str(e)}")
            return None