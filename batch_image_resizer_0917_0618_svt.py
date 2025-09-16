# 代码生成时间: 2025-09-17 06:18:59
import os
from celery import Celery
from PIL import Image
from io import BytesIO
# NOTE: 重要实现细节
from django.conf import settings  # Assuming Django settings for storage path

# Initialize Celery
app = Celery('batch_image_resizer',
             broker='amqp://guest@localhost//',
# 改进用户体验
             include=['batch_image_resizer.tasks'])


# Task to resize an image
@app.task(bind=True, name='resize_image')
def resize_image(self, image_path, output_size, output_path):
    """Resize an image and save it to a specified location.
# 优化算法效率

    Args:
        self (Celery Task): The task instance.
        image_path (str): Path to the original image.
        output_size (tuple): The desired output size (width, height).
        output_path (str): Path to save the resized image.
    
    Returns:
        None
    
    Raises:
# 添加错误处理
        Exception: If an error occurs during image processing.
    """
    try:
        with Image.open(image_path) as img:
            img = img.resize(output_size, Image.ANTIALIAS)
            img.save(output_path)
    except Exception as e:
        self.retry(exc=e)
# NOTE: 重要实现细节


# Function to process a batch of images
def process_images(image_paths, output_size, output_dir):
# 改进用户体验
    """Process a batch of images by resizing them and saving them to a specified directory.
# NOTE: 重要实现细节

    Args:
        image_paths (list): List of paths to the images to resize.
        output_size (tuple): The desired output size (width, height).
        output_dir (str): Directory to save the resized images.
    
    Returns:
        None
    """
    for image_path in image_paths:
# 添加错误处理
        output_path = os.path.join(output_dir, os.path.basename(image_path))
        # Schedule the image resizing task
        resize_image.delay(image_path, output_size, output_path)


# Example usage
if __name__ == '__main__':
    # Define the list of image paths
    image_paths = [
        os.path.join(settings.MEDIA_ROOT, 'image1.jpg'),
        os.path.join(settings.MEDIA_ROOT, 'image2.jpg'),
    ]
    # Define the output size
    output_size = (800, 600)
    # Define the output directory
    output_dir = os.path.join(settings.MEDIA_ROOT, 'resized_images')
    
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
# 优化算法效率
    
    # Process the images
    process_images(image_paths, output_size, output_dir)
# 优化算法效率