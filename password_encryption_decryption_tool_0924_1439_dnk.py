# 代码生成时间: 2025-09-24 14:39:52
import hashlib
import base64
from celery import Celery, Task
from cryptography.fernet import Fernet

# Initialize Celery
app = Celery('password_tool', broker='pyamqp://guest@localhost//')


class PasswordTool(Task):
    """
    A Celery task class for password encryption and decryption.
    """

    def __init__(self):
        super().__init__()
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, password):
        """
        Encrypts a plain text password.
        
        Args:
        password (str): The plain text password.
        
        Returns:
        str: The encrypted password.
        
        Raises:
        ValueError: If the password is None or empty.
        """
        if not password:
            raise ValueError('Password cannot be empty')
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        return base64.b64encode(encrypted_password).decode()

    def decrypt(self, encrypted_password):
        """
        Decrypts an encrypted password.
        
        Args:
        encrypted_password (str): The encrypted password.
        
        Returns:
        str: The decrypted password.
        
        Raises:
        ValueError: If the encrypted password is None or empty.
        """
        if not encrypted_password:
            raise ValueError('Encrypted password cannot be empty')
        encrypted_password_bytes = base64.b64decode(encrypted_password)
        decrypted_password = self.cipher_suite.decrypt(encrypted_password_bytes)
        return decrypted_password.decode()

    @staticmethod
    def hash_password(password):
        """
        Creates a hash of a plain text password using SHA-256.
        
        Args:
        password (str): The plain text password.
        
        Returns:
        str: The hashed password.
        """
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        return sha_signature

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verifies a plain text password against its hashed version.
        
        Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.
        
        Returns:
        bool: True if the password matches, False otherwise.
        """
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


# Example usage:
if __name__ == '__main__':
    password_tool = PasswordTool()
    try:
        password = 'my_secret_password'
        encrypted = password_tool.encrypt(password)
        print('Encrypted:', encrypted)
        decrypted = password_tool.decrypt(encrypted)
        print('Decrypted:', decrypted)
        hashed = password_tool.hash_password(password)
        print('Hashed:', hashed)
        is_valid = password_tool.verify_password(password, hashed)
        print('Is valid:', is_valid)
    except ValueError as e:
        print(f'Error: {e}')
