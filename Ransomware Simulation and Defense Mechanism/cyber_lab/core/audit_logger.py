import hashlib
import json
import time
import logging
from pathlib import Path
from datetime import datetime

class AuditLogger:
    """
    Tamper-proof Audit Logger using Hash Chaining.
    Each entry includes the hash of the previous entry.
    """
    def __init__(self, log_file="logs/audit_trail.json"):
        self.log_file = Path(log_file).resolve()
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("AuditLogger")
        self.chain = self._load_chain()

    def _load_chain(self):
        if self.log_file.exists():
            try:
                with open(self.log_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load audit chain: {e}")
        return []

    def _calculate_hash(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def log_event(self, user, action, details):
        """
        Logs an event and extends the hash chain.
        """
        prev_hash = self.chain[-1]["current_hash"] if self.chain else "0" * 64
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "action": action,
            "details": details,
            "previous_hash": prev_hash
        }
        
        # Calculate current hash including all fields + previous_hash
        entry["current_hash"] = self._calculate_hash(entry)
        
        self.chain.append(entry)
        self._save_chain()
        self.logger.info(f"Audit log entry added: {action} by {user}")

    def _save_chain(self):
        with open(self.log_file, "w") as f:
            json.dump(self.chain, f, indent=4)

    def verify_integrity(self):
        """
        Verifies the integrity of the audit chain.
        Returns (is_intact, error_index)
        """
        for i in range(len(self.chain)):
            entry = self.chain[i].copy()
            claimed_hash = entry.pop("current_hash")
            
            # Recalculate hash
            actual_content_hash = self._calculate_hash(entry)
            
            if claimed_hash != actual_content_hash:
                return False, i
            
            if i > 0:
                if entry["previous_hash"] != self.chain[i-1]["current_hash"]:
                    return False, i
                    
        return True, -1
