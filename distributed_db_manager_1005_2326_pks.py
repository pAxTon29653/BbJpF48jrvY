# 代码生成时间: 2025-10-05 23:26:45
import os
import celery
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from datetime import timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

# Configuration for Celery
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'

# Database configuration
DB_URI = 'postgresql://user:password@localhost/dbname'

# Create Celery app instance
app = Celery('distributed_db_manager',
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             broker_use_ssl=False)

# Configure soft time limit for tasks
app.conf.task_soft_time_limit = 60  # 60 seconds
app.conf.task_time_limit = 120  # 120 seconds

# SQLAlchemy session setup
Session = scoped_session(sessionmaker(bind=create_engine(DB_URI)))


def db_task(target_func):
    """Decorator to handle database connections and session management."""
    def wrapper(*args, **kwargs):
        try:
            # Open a new session
            session = Session()
            result = target_func(session, *args, **kwargs)
            # Commit changes and close the session
            session.commit()
            return result
        except Exception as e:
            # Rollback changes and close the session in case of error
            session.rollback()
            raise e
        finally:
            # Close the session
            session.close()
    return wrapper

# Task to perform database operations
@app.task(soft_time_limit=30, time_limit=60)
def db_operation(session, sql, params=None):
    """Celery task to execute a database operation."""
    # Execute SQL query or command
    with session.begin():
        if params:
            result = session.execute(text(sql), params)
        else:
            result = session.execute(text(sql))

        # Fetch results if it's a SELECT query
        if sql.strip().lower().startswith('select'):
            return result.fetchall()
        else:
            return result.rowcount

# Example usage of the db_operation task
# db_operation.delay('SELECT * FROM my_table')

# Error handling example
@app.task(bind=True)
@db_task
def db_error_handling(self, session):
    """Task that demonstrates error handling."""
    try:
        # Simulate a database error
        raise SoftTimeLimitExceeded("Task exceeded the soft time limit.")
    except SoftTimeLimitExceeded as e:
        # Handle the timeout error
        self.retry(exc=e, countdown=30, max_retries=3)

# Main execution
if __name__ == '__main__':
    app.start()