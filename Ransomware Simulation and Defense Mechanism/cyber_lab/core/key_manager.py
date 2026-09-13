from cryptography.fernet import Fernet
import logging
import time
import shutil
from pathlib import Path
from datetime import datetime

class KeyManager:
    """
    Manages encryption keys with Lifecycle Management.
    - Key Rotation (Versioning)
    - Key Expiration (Simulated)
    - Archival
    """
    def __init__(self, key_dir="keys"):
        self.key_dir = Path(key_dir).resolve()
        self.archive_dir = self.key_dir / "archive"
        self.logger = logging.getLogger("KeyManager")
        
        self.key_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_key_id = None
        self.expiration_window = 300 # 5 minutes for simulation

    def generate_key(self):
        """
        Rotates the current key. Archives old one if exists.
        """
        # Archive existing
        current = self.key_dir / "secret.key"
        if current.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.move(str(current), str(self.archive_dir / f"secret_{timestamp}.key"))
            self.logger.info(f"Archived old key to secret_{timestamp}.key")

        # Generate New
        key = Fernet.generate_key()
        with open(current, "wb") as key_file:
            key_file.write(key)
        
        self.current_key_id = datetime.now().isoformat()
        self.logger.info(f"New Key Generated. ID: {self.current_key_id}")
        return key

    def load_key(self):
        """
        Loads the active key.
        Checks for expiration (simulated warning).
        """
        key_path = self.key_dir / "secret.key"
        if not key_path.exists():
            return self.generate_key()
        
        # Check metadata (file modification time)
        mtime = key_path.stat().st_mtime
        age = time.time() - mtime
        
        if age > self.expiration_window:
            self.logger.warning(f"KEY EXPIRED! Age: {int(age)}s (Policy: {self.expiration_window}s). Rotation Recommended.")
        
        with open(key_path, "rb") as key_file:
            return key_file.read()

    def list_archived_keys(self):
        return [f.name for f in self.archive_dir.glob("*.key")]
    
    def get_key_status(self):
        key_path = self.key_dir / "secret.key"
        if not key_path.exists():
            return "No Key Found", "N/A"
            
        mtime = key_path.stat().st_mtime
        age = time.time() - mtime
        status = "Active" if age < self.expiration_window else "Expired"
        return status, f"{int(age)}s"
