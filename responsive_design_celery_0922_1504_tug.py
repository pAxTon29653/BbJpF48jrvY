# 代码生成时间: 2025-09-22 15:04:28
import os
import requests
from celery import Celery
from celery.utils.log import get_task_logger
from urllib.parse import urljoin

# 配置Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # 替换为你的项目设置模块
app = Celery('tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 日志记录
logger = get_task_logger(__name__)

# 定义响应式布局任务
@app.task
def responsive_layout(url, width, height):
    """
    根据给定的URL、宽度和高度，返回响应式布局的HTML代码。
    :param url: 网页URL
    :param width: 页面宽度
    :param height: 页面高度
    :return: 响应式布局的HTML代码
    """
    try:
        # 发送HTTP请求，获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析HTML内容
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # 创建响应式布局的HTML代码
        html_code = f"""
        <!DOCTYPE html>
        <html lang="en">\        <head>
            <meta charset="UTF-8">\            <meta name="viewport" content="width={width}, initial-scale={width/height:.2f}">\            <style>
                /* 响应式布局样式 */
                * {
                    box-sizing: border-box;
                }
                .container {
                    width: 100%;
                    max-width: {width}px;
                    margin: auto;
                }
                /* 添加其他响应式布局样式 */
            </style>
        </head>
        <body>
            <div class="container">\
                {soup.prettify()}
            </div>
        </body>
        </html>
        """

        # 返回响应式布局的HTML代码
        return html_code

    except requests.RequestException as e:
        # 处理HTTP请求错误
        logger.error(f'HTTP请求错误: {e}')
        raise
    except Exception as e:
        # 处理其他错误
        logger.error(f'未知错误: {e}')
        raise
