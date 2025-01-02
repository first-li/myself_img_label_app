import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.logger import logger
from config.load_config import config

def main():
    logger.info("启动应用...")
    app = QApplication(sys.argv)
    logger.info("创建主窗口...")
    window = MainWindow(config)
    logger.info("展示主窗口...")
    window.show()
    logger.info("开始事件循环...")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
