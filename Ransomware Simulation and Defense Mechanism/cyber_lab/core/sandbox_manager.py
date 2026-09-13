import os
import shutil
import logging
from pathlib import Path

class SandboxManager:
    """
    Manages the isolated sandbox environment for the ransomware simulation.
    Ensures that all operations are strictly confined to the sandbox directory.
    """
    def __init__(self, sandbox_path="sandbox"):
        self.sandbox_path = Path(sandbox_path).resolve()
        self.logger = logging.getLogger("SandboxManager")
        
        if not self.sandbox_path.exists():
            self.sandbox_path.mkdir(parents=True)
            self.logger.info(f"Created sandbox directory at {self.sandbox_path}")

    def is_safe_path(self, filepath):
        """
        Verifies if the given filepath is within the sandbox directory.
        """
        try:
            filepath = Path(filepath).resolve()
            return str(filepath).startswith(str(self.sandbox_path))
        except Exception as e:
            self.logger.error(f"Path verification failed: {e}")
            return False

    def reset_sandbox(self):
        """
        Clears the sandbox directory and recreates it.
        Useful for resetting the simulation.
        """
        if self.sandbox_path.exists():
            shutil.rmtree(self.sandbox_path)
            self.logger.info("Sandbox cleared.")
        self.sandbox_path.mkdir(parents=True)
        self.logger.info("Sandbox recreated.")

    def create_mock_files(self, count=10):
        """
        Generates mock files in the sandbox for testing.
        """
        self.reset_sandbox()
        for i in range(count):
            filename = self.sandbox_path / f"document_{i}.txt"
            with open(filename, "w") as f:
                f.write(f"This is a confidential document number {i}.\n" * 10)
        self.logger.info(f"Created {count} mock files in sandbox.")

    def list_files(self):
        """
        Lists all files in the sandbox.
        """
        return [str(f) for f in self.sandbox_path.rglob("*") if f.is_file()]
