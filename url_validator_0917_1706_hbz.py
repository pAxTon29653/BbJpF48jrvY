# 代码生成时间: 2025-09-17 17:06:14
import requests
from celery import Celery
from urllib.parse import urlparse
from typing import Dict, Any

# 配置Celery
app = Celery('url_validator',
              broker='pyamqp://guest@localhost//')


@app.task
def validate_url(url: str) -> Dict[str, Any]:
    """
    验证URL链接的有效性。
    
    参数:
    - url: 待验证的URL字符串
    
    返回:
    - 一个包含'status'和'message'的字典
    """
    try:
        # 解析URL
        parsed_url = urlparse(url)

        # 检查URL是否有网络位置
        if not parsed_url.netloc:
            return {'status': False, 'message': 'Invalid URL: No network location found.'}

        # 发送HEAD请求以验证URL的可达性
        response = requests.head(url, allow_redirects=True)

        # 检查HTTP响应状态码
        if response.status_code != 200:
            return {'status': False, 'message': f'Invalid URL: HTTP response status code is {response.status_code}.'}

        # 如果响应成功，返回成功状态
        return {'status': True, 'message': 'URL is valid.'}

    except requests.exceptions.RequestException as e:
        # 捕获请求异常，如连接错误
        return {'status': False, 'message': f'Error occurred: {str(e)}'}
    except Exception as e:
        # 捕获其他异常
        return {'status': False, 'message': f'An unexpected error occurred: {str(e)}'}
