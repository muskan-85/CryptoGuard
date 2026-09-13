import base64
from cryptography.fernet import Fernet
import logging
import time
from .sandbox_manager import SandboxManager

class EncryptionEngine:
    """
    Handles the file encryption process.
    Strictly enforces sandbox boundaries.
    """
    def __init__(self, sandbox_manager: SandboxManager):
        self.sandbox = sandbox_manager
        self.logger = logging.getLogger("EncryptionEngine")

    def encrypt_file(self, filepath, key):
        """
        Encrypts a single file using the provided key.
        """
        if not self.sandbox.is_safe_path(filepath):
            self.logger.critical(f"SECURITY ALERT: Attempted to encrypt file outside sandbox: {filepath}")
            raise PermissionError(f"Access denied: {filepath} is outside the sandbox.")

        try:
            f = Fernet(key)
            with open(filepath, "rb") as file:
                file_data = file.read()
            
            # Fernet returns Base64 encoded bytes. 
            # We decode to raw bytes to simulate realistic ransomware high entropy.
            encrypted_token = f.encrypt(file_data)
            raw_encrypted_data = base64.urlsafe_b64decode(encrypted_token)
            
            with open(filepath, "wb") as file:
                file.write(raw_encrypted_data)
            
            # Simulate processing time for visual effect
            time.sleep(0.05) 
            self.logger.info(f"Encrypted: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to encrypt {filepath}: {e}")
            return False

    def encrypt_sandbox(self, key, progress_callback=None):
        """
        Encrypts all files in the sandbox.
        """
        files = self.sandbox.list_files()
        total_files = len(files)
        encrypted_count = 0

        for i, filepath in enumerate(files):
            if self.encrypt_file(filepath, key):
                encrypted_count += 1
            
            if progress_callback:
                progress_callback(int((i + 1) / total_files * 100))
        
        return encrypted_count
