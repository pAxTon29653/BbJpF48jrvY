# 代码生成时间: 2025-09-16 22:16:30
#!/usr/bin/env python

"""
Memory Usage Analyze
=======================

This program analyzes the memory usage of a system using Python and Celery.
It utilizes the `psutil` library to gather system memory information and
schedules memory usage checks at regular intervals.

"""

import os
import psutil
from celery import Celery
from celery.schedules import crontab

# Initialize Celery app
app = Celery('memory_usage_analyze', broker='pyamqp://guest@localhost//')
app.conf.beat_schedule = {
    'check-memory-every-minute': {
        'task': 'memory_usage_analyze.check_memory_usage',
        'schedule': crontab(minute='*')
    }
}


# Define the task for checking memory usage
@app.task
def check_memory_usage():
    """
    Check the current memory usage of the system.
    If the memory usage exceeds a certain threshold, log a warning.
    """
    try:
        # Get the current system memory usage
        memory = psutil.virtual_memory()

        # Calculate the percentage of memory used
        memory_usage_percentage = memory.percent

        # Define the memory usage threshold
        memory_threshold = 80  # 80%

        # Check if the memory usage exceeds the threshold
        if memory_usage_percentage > memory_threshold:
            raise Exception(f"Memory usage is above the threshold: {memory_usage_percentage}%")
        else:
            print(f"Memory usage is within the safe limit: {memory_usage_percentage}%")
    except Exception as e:
        # Log the exception
        print(f"An error occurred while checking memory usage: {e}")


# Define a periodic task to check memory usage
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Set up periodic task to check memory usage every minute
    sender.add_periodic_task(60.0, check_memory_usage.s(), name='check-memory-every-minute')

if __name__ == '__main__':
    # Start the Celery worker
    app.start()