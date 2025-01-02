import logging
from datetime import datetime, timedelta
from pathlib import Path

class Logger:
    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        self._setup_logger()
        self._clean_old_logs()

    def _setup_logger(self):
        log_file = self.log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        # print(f"日志文件路径: {log_file}")  # 调试信息
        logging.basicConfig(
            level=logging.DEBUG,  # 设置为 DEBUG 级别
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),  # 确保 UTF-8 编码
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger()

    def _clean_old_logs(self):
        cutoff = datetime.now() - timedelta(days=30)
        for log_file in self.log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff.timestamp():
                log_file.unlink()

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

logger = Logger()