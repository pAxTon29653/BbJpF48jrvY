# 代码生成时间: 2025-09-23 00:35:49
import os
import logging
from celery import Celery
from celery.contrib.django import app as celery_app
from django.conf import settings

# 配置Celery
app = celery_app.Celery('database_migration')
app.conf.update(settings.__dict__)

# 导入数据库迁移相关模块
from django.db import migrations, models
from django.db.migrations.writer import MigrationWriter

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 定义数据库迁移任务
@app.task(bind=True)
def migrate_database(self, app_label, migration_name):
    """
    执行数据库迁移任务。

    参数:
    app_label -- Django应用的标签
    migration_name -- 迁移文件的名称

    返回:
    迁移结果
    """
    try:
        # 获取迁移文件路径
        migration_path = os.path.join(settings.BASE_DIR, 'django_migrations', app_label, migration_name + '.py')
        
        # 检查迁移文件是否存在
        if not os.path.exists(migration_path):
            raise FileNotFoundError(f'Migration file {migration_path} not found.')
        
        # 执行迁移
        migration = migrations.Migration(migration_name, app_label)
        writer = MigrationWriter(migration)
        writer.write_migration_file(migration_path)
        migrations.run_migration(migration)
        logger.info(f'Migration {migration_name} for app {app_label} completed successfully.')
        return f'{migration_name} migration completed successfully.'
    except Exception as e:
        logger.error(f'Error occurred during migration: {e}')
        raise
        

# 使用示例
# migrate_database.delay('myapp', '0001_initial')
