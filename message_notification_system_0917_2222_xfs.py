# 代码生成时间: 2025-09-17 22:22:41
import os
import json
from celery import Celery
from celery.exceptions import Ignore

# 配置Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
app = Celery("message_notification_system")
app.config_from_object("django.conf:settings", namespace="CELERY")

# 消息通知任务
@app.task(bind=True)
def notify_user(self, message):
    '''
    发送消息通知给用户的任务
    :param self: Celery任务实例
    :param message: 要发送的消息
    :return: None
    '''
    try:
        print(f"Sending message to user: {message}")
        # 这里可以添加实际的消息发送逻辑，例如发送邮件、短信等
        # send_email(message)
        # send_sms(message)
        return f"Message sent successfully: {message}"
    except Exception as e:
        # 任务执行出错时，记录错误日志
        print(f"Error sending message: {e}")
        raise Ignore()

# 使用示例
if __name__ == "__main__":
    result = notify_user.delay("Hello, this is a test message!")
    print(result.get(timeout=5))
