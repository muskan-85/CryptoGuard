import hashlib
import logging
from pathlib import Path

class FileIntegrityChecker:
    """
    Monitors file integrity using SHA-256 hashes.
    Detects silent corruption or unauthorized modification.
    """
    def __init__(self, sandbox_manager):
        self.sandbox = sandbox_manager
        self.baseline = {}
        self.logger = logging.getLogger("FileIntegrity")

    def calculate_hash(self, filepath):
        """
        Calculates SHA-256 hash of a file.
        """
        sha256 = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            self.logger.error(f"Error hashing {filepath}: {e}")
            return None

    def establish_baseline(self):
        """
        Scans all files and records their initial hashes.
        """
        self.baseline = {}
        files = self.sandbox.list_files()
        for f in files:
            h = self.calculate_hash(f)
            if h:
                self.baseline[f] = h
        self.logger.info(f"Baseline established for {len(self.baseline)} files.")

    def check_integrity(self):
        """
        Verifies current files against the baseline.
        Returns list of compromised files.
        """
        compromised = []
        files = self.sandbox.list_files()
        
        for f in files:
            current_hash = self.calculate_hash(f)
            original_hash = self.baseline.get(f)
            
            if original_hash and current_hash != original_hash:
                self.logger.warning(f"Integrity violation detected: {f}")
                compromised.append(f)
        
        return compromised
