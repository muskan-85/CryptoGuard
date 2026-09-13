import base64
from cryptography.fernet import Fernet
import logging
import time
from .sandbox_manager import SandboxManager

class DecryptionEngine:
    """
    Handles the file decryption process.
    """
    def __init__(self, sandbox_manager: SandboxManager):
        self.sandbox = sandbox_manager
        self.logger = logging.getLogger("DecryptionEngine")

    def decrypt_file(self, filepath, key):
        """
        Decrypts a single file using the provided key.
        """
        if not self.sandbox.is_safe_path(filepath):
            self.logger.critical(f"SECURITY ALERT: Attempted to decrypt file outside sandbox: {filepath}")
            raise PermissionError(f"Access denied: {filepath} is outside the sandbox.")

        try:
            f = Fernet(key)
            with open(filepath, "rb") as file:
                raw_encrypted_data = file.read()
            
            # Re-encode raw bytes to Base64 token for Fernet
            encrypted_token = base64.urlsafe_b64encode(raw_encrypted_data)
            decrypted_data = f.decrypt(encrypted_token)
            
            with open(filepath, "wb") as file:
                file.write(decrypted_data)
            
            # Simulate processing time
            time.sleep(0.05)
            self.logger.info(f"Decrypted: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to decrypt {filepath}: {e}")
            return False

    def decrypt_sandbox(self, key, progress_callback=None):
        """
        Decrypts all files in the sandbox.
        """
        files = self.sandbox.list_files()
        total_files = len(files)
        decrypted_count = 0

        for i, filepath in enumerate(files):
            if self.decrypt_file(filepath, key):
                decrypted_count += 1
            
            if progress_callback:
                progress_callback(int((i + 1) / total_files * 100))

        return decrypted_count
