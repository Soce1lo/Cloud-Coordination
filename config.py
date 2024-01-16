import logging
import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///node_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    LOGGING_LEVEL = logging.INFO
    LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOGGING_FILE = '/app/logs/app.log'


def setup_logging():
    logger = logging.getLogger('my_logger')
    logger.setLevel(Config.LOGGING_LEVEL)

    # 文件处理器
    file_handler = logging.FileHandler(Config.LOGGING_FILE)
    file_handler.setLevel(Config.LOGGING_LEVEL)
    file_handler.setFormatter(logging.Formatter(Config.LOGGING_FORMAT))

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.LOGGING_LEVEL)
    console_handler.setFormatter(logging.Formatter(Config.LOGGING_FORMAT))

    # 添加处理器到记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger