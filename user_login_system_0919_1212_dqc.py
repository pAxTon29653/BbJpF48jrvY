# 代码生成时间: 2025-09-19 12:12:31
import logging
from celery import Celery
from celery.utils.log import get_task_logger
from datetime import datetime

# 配置Celery
app = Celery('user_login_system', broker='pyamqp://guest@localhost//')
app.conf.update(
    task_serializer='json',
    result_backend='rpc://',
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,
)

# 获取任务日志
task_logger = get_task_logger(__name__)

# 模拟数据库存储的用户信息
users_db = {
    'john': {'password': '123456', 'last_login': None},
    'jane': {'password': 'abcdef', 'last_login': None},
}


@app.task(bind=True,
         name='user_login_system.verify_user')
def verify_user(self, username, password):
    """
    任务：验证用户登录信息
    :param self: Celery任务实例
    :param username: 用户名
    :param password: 用户密码
    :return: 登录结果，返回用户名如果成功，否则返回错误信息
    """
    try:
        user = users_db.get(username)
        if not user:
            return 'User does not exist.'
        if user['password'] != password:
            return 'Invalid password.'
        user['last_login'] = datetime.now()
        return username
    except Exception as e:
        task_logger.error(f'Error verifying user: {e}')
        return 'An unexpected error occurred.'


def main():
    """
    主函数：用于测试Celery任务
    """
    # 测试用户登录
    login_result = verify_user.delay('john', '123456')
    print(f'Login result: {login_result.get()}
')
    login_result = verify_user.delay('john', 'wrongpassword')
    print(f'Login result: {login_result.get()}
')

if __name__ == '__main__':
    main()
