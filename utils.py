# utils.py
import logging
import os
import tempfile

def setup_logging():
    log_file_path = tempfile.gettempdir() + '/debug.log'
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def add_to_history(title, shared_link, conversation_record):
    # 添加到历史记录的逻辑
    pass

def update_history_sidebar():
    # 更新历史记录侧边栏的逻辑
    pass
