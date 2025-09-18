# 代码生成时间: 2025-09-19 03:54:58
import os
import re
from celery import Celery
from celery.result import AsyncResult

# 定义Celery配置
app = Celery('log_parser', broker='pyamqp://guest@localhost//')

# 日志文件解析任务
@app.task
def parse_log_file(log_file_path):
    """
    解析日志文件并提取有用信息。
    
    参数:
    log_file_path -- 日志文件的路径
    
    返回:
    日志文件中的信息摘要
    """
    if not os.path.isfile(log_file_path):
        raise FileNotFoundError(f'The file {log_file_path} does not exist.')
    
    try:
        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()
    except IOError as e:
        raise IOError(f'Failed to read file {log_file_path}: {e}')
    
    # 定义日志行的正则表达式模式
    log_pattern = re.compile(r'\b(ERROR|WARNING|INFO)\b.*')
    
    # 解析日志文件
    log_summary = {'ERROR': 0, 'WARNING': 0, 'INFO': 0}
    for log_line in logs:
        if log_pattern.match(log_line):
            level = log_line.split()[0]
            log_summary[level] += 1
    
    return log_summary

# 启动Celery worker
if __name__ == '__main__':
    app.start()
