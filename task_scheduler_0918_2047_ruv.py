# 代码生成时间: 2025-09-18 20:47:37
import celery
from celery.schedules import crontab
from celery.task import periodic_task
from celery import Celery
from datetime import timedelta

# 配置Celery
app = Celery('task_scheduler',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'task_scheduler.sample_task',    # 任务名称
        'schedule': 30.0,                      # 每30秒执行一次
    },
    'add-every-5-minutes': {
        'task': 'task_scheduler.sample_task',    # 任务名称
        'schedule': timedelta(minutes=5),       # 每5分钟执行一次
    },
}

# 定义一个周期性任务
@periodic_task(run_every=30, name='sample_task')
def sample_task():
    """
    这是一个示例周期性任务。
    这个任务每30秒执行一次。
    在实际应用中，这里可以放置任何需要周期性执行的代码。
    """
    try:
        # 这里放置实际的周期性执行代码
        print('Sample task is running...')
    except Exception as e:
        # 错误处理
        print(f'An error occurred: {e}')

# 启动Celery定时任务调度器
if __name__ == '__main__':
    app.start()
