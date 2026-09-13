import shutil
import hashlib
import logging
import time
import os
from pathlib import Path
from datetime import datetime

class BackupEngine:
    """
    Manages automated snapshots and restoration of the sandbox environment.
    Ensures data safety before simulated attacks.
    """
    def __init__(self, sandbox_manager, backup_count=3, backup_dir="backups"):
        self.sandbox = sandbox_manager
        self.backup_dir = Path(backup_dir).resolve()
        self.backup_count = backup_count
        self.logger = logging.getLogger("BackupEngine")
        
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)

    def create_snapshot(self):
        """
        Creates a timestamped snapshot of the sandbox.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = self.backup_dir / f"snapshot_{timestamp}"
        
        try:
            # Explicitly resolve paths to strings to avoid Pathlib issues on some Py versions
            src = str(self.sandbox.sandbox_path)
            dst = str(snapshot_path)
            shutil.copytree(src, dst)
            self.logger.info(f"Snapshot created: {snapshot_path}")
            self._cleanup_old_snapshots()
            return str(snapshot_path)
        except Exception as e:
            self.logger.error(f"Snapshot failed: {e}")
            return None

    def restore_snapshot(self, snapshot_path=None):
        """
        Restores the sandbox from a snapshot.
        If no path provided, restores the latest.
        """
        if not snapshot_path:
            snapshots = sorted(self.backup_dir.glob("snapshot_*"), key=os.path.getmtime, reverse=True)
            if not snapshots:
                self.logger.warning("No snapshots available to restore.")
                return False
            snapshot_path = snapshots[0]

        try:
            # Verify backup integrity first (mock check)
            if not self._verify_integrity(snapshot_path):
                self.logger.critical("Backup integrity check failed! Aborting restore.")
                return False

            self.sandbox.reset_sandbox()
            # We copy contents back, not the dir itself to keep sandbox root
            for item in snapshot_path.iterdir():
                if item.is_dir():
                    shutil.copytree(item, self.sandbox.sandbox_path / item.name)
                else:
                    shutil.copy2(item, self.sandbox.sandbox_path)
            
            self.logger.info(f"Restored from: {snapshot_path}")
            return True
        except Exception as e:
            self.logger.error(f"Restore failed: {e}")
            return False

    def _cleanup_old_snapshots(self):
        snapshots = sorted(self.backup_dir.glob("snapshot_*"), key=os.path.getmtime)
        while len(snapshots) > self.backup_count:
            oldest = snapshots.pop(0)
            shutil.rmtree(oldest)
            self.logger.info(f"Deleted old snapshot: {oldest}")
    
    def _verify_integrity(self, path):
        # Implementation of hash check would go here
        return True
