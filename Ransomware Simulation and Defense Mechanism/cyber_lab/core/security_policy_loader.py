import json
import logging
from pathlib import Path

class SecurityPolicyLoader:
    """
    Loads and enforces security policies from a configuration file.
    Defines thresholds for defense mechanisms.
    """
    def __init__(self, policy_file="security_policy.json"):
        self.policy_file = Path(policy_file).resolve()
        self.logger = logging.getLogger("SecurityPolicy")
        self.policy = self._load_default_policy()

        if self.policy_file.exists():
            self._load_policy()
        else:
            self._save_policy()

    def _load_default_policy(self):
        return {
            "defense": {
                "max_entropy_threshold": 7.5,
                "encryption_rate_limit": 10,  # Files per second
                "honeypot_sensitivity": "high",
                "monitor_interval": 1.0
            },
            "snapshots": {
                "auto_backup": True,
                "backup_retention": 5
            },
            "access_control": {
                "require_mfa_restore": False,
                "lock_on_fail": True
            }
        }

    def _load_policy(self):
        try:
            with open(self.policy_file, "r") as f:
                self.policy = json.load(f)
            self.logger.info("Security policy loaded.")
        except Exception as e:
            self.logger.error(f"Failed to load policy: {e}")

    def _save_policy(self):
        with open(self.policy_file, "w") as f:
            json.dump(self.policy, f, indent=4)

    def get_threshold(self, key, default=None):
        return self.policy.get("defense", {}).get(key, default)
