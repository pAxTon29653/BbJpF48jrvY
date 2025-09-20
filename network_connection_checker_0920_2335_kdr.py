# 代码生成时间: 2025-09-20 23:35:06
import os
import socket
from celery import Celery, states

# 定义网络连接状态检查器的 Celery 任务
app = Celery('network_connection_checker',
             broker='amqp://guest@localhost//')

# 网络连接状态检查任务
@app.task(name='check_connection')
def check_connection(host, port):
    """检查指定主机和端口的网络连接状态。

    参数:
    host (str): 要检查的主机地址。
    port (int): 要检查的端口号。

    返回:
    dict: 包含网络连接状态的字典。
    """
    try:
        # 尝试建立 TCP 连接
        with socket.create_connection((host, port), timeout=10):
            return {'status': 'connected', 'host': host, 'port': port}
    except OSError as e:
        # 处理连接错误
        return {'status': 'error', 'host': host, 'port': port, 'error': str(e)}
    except TimeoutError:
        # 处理连接超时
        return {'status': 'timeout', 'host': host, 'port': port}
    except Exception as e:
        # 处理其他异常
        return {'status': 'unknown error', 'host': host, 'port': port, 'error': str(e)}

# 如果此脚本作为主程序运行，则执行以下代码
if __name__ == '__main__':
    # 启动 Celery worker 以便任务可以被处理
    app.start()
