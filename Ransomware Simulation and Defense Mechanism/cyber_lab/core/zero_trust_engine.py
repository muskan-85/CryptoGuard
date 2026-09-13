import logging
import time

class ZeroTrustEngine:
    """
    Simulates a Zero Trust Architecture (ZTA).
    Intercepts operations and mandates explicit visualization of 'Authorization'.
    """
    def __init__(self):
        self.logger = logging.getLogger("ZeroTrust")
        self.active_session = None
        self.blocked_actions = 0
        self.roles = {
            "admin": ["read", "write", "encrypt", "decrypt", "restore"],
            "user": ["read", "write"],
            "guest": ["read"]
        }

    def authenticate_session(self, role):
        self.active_session = role
        self.logger.info(f"Session authenticated as: {role}")

    def authorize_action(self, action):
        """
        Checks if the current session is authorized for the action.
        """
        if not self.active_session:
            self.blocked_actions += 1
            self.logger.warning(f"BLOCKED: Unauthenticated attempt to {action}")
            return False
            
        allowed_actions = self.roles.get(self.active_session, [])
        if action in allowed_actions:
            return True
        else:
            self.blocked_actions += 1
            self.logger.warning(f"BLOCKED: {self.active_session} not authorized for {action}")
            return False
