from datetime import datetime
import logging
from utils.path_tool import get_abs_path
import os

"""
 日志处理
"""

# 日志的保存路径
LOG_ROOT = get_abs_path("logs")
# 确保日志目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志的格式
"""
asctime: 时间
name: 日志名称
levelname: 日志级别
lineno: 行号
message: 日志内容
"""
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)


def get_logger(name: str = "agent", console_level: int = logging.INFO, file_level: int = logging.DEBUG,
               log_file=None) -> logging.Logger:
    # 获取日志对象
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加Handler 避免日志重复输出
    if logger.handlers:
        return logger

    # 控制台处理器 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    # 文件处理器 Handler
    if log_file is None:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger


# 快捷获取日志器
logger = get_logger()

if __name__ == '__main__':
    logger.info("信息日志")
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.debug("调试日志")
