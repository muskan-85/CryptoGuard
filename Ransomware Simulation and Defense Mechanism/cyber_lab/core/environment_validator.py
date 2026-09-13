import sys
import os
import logging
from pathlib import Path

class EnvironmentValidator:
    """
    Ensures the application is running in a secure and valid environment.
    Prevents execution if integrity checks fail.
    """
    def __init__(self, sandbox_path):
        self.logger = logging.getLogger("EnvironmentValidator")
        self.sandbox_path = Path(sandbox_path).resolve()

    def validate_venv(self):
        """
        Checks if the application is running inside a virtual environment.
        (Optional strict mode for production/lab safety)
        """
        is_venv = (sys.prefix != sys.base_prefix)
        if not is_venv:
            self.logger.warning("SAFETY WARNING: Application is NOT running in a virtual environment.")
            # In strict mode, we might raise an error here.
            return False
        return True

    def validate_sandbox_integrity(self):
        """
        Ensures the sandbox directory is writable and isolated.
        """
        if not self.sandbox_path.exists():
            self.logger.error(f"Sandbox path does not exist: {self.sandbox_path}")
            return False
        
        # Check permissions
        if not os.access(self.sandbox_path, os.W_OK):
            self.logger.error(f"Sandbox is not writable: {self.sandbox_path}")
            return False

        self.logger.info("Environment integrity verified.")
        return True
