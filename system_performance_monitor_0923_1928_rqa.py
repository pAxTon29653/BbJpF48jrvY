# 代码生成时间: 2025-09-23 19:28:46
import os
import psutil
from celery import Celery
from celery.schedules import crontab
from celery.exceptions import SoftTimeLimitExceeded

# 设置Celery配置
app = Celery('system_performance_monitor',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')
app.conf.update(
    timezone='UTC',
    CELERYBEAT_SCHEDULE={
        'monitor-system-performance': {
            'task': 'system_performance_monitor.monitor_performance',
            'schedule': crontab(minute='*/5')  # 每5分钟执行一次
        },
    })

# 系统性能监控任务
@app.task(soft_time_limit=60)  # 设置任务软时限为60秒
def monitor_performance():
    try:
        # 获取CPU和内存使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        
        # 获取磁盘使用情况
        disk_usage = psutil.disk_usage('/').percent
        
        # 获取网络流量
        net_io = psutil.net_io_counters()
        
        # 打印系统性能数据
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_usage}%")
        print(f"Disk Usage: {disk_usage}%")
        print(f"Network IO: {net_io.bytes_sent} bytes sent, {net_io.bytes_recv} bytes received")
        
        # 可以根据需要将数据存储到数据库或日志文件
        
    except (psutil.NoSuchProcess, psutil.AccessDenied,
            SoftTimeLimitExceeded) as e:
        # 处理可能的异常
        print(f"Failed to monitor system performance: {e}")

# Celery worker入口
if __name__ == '__main__':
    app.start()