import logging

class RBACEngine:
    """
    Role-Based Access Control Engine.
    Manages roles and permissions for the CyberLab system.
    """
    ROLES = {
        "ADMIN": {
            "permissions": ["attack", "restore", "view_audit", "rotate_keys", "configure"],
            "description": "Full system access."
        },
        "OPERATOR": {
            "permissions": ["restore", "view_audit"],
            "description": "Restricted to defense operations."
        },
        "AUDITOR": {
            "permissions": ["view_audit"],
            "description": "Read-only access to logs and metrics."
        }
    }

    def __init__(self):
        self.logger = logging.getLogger("RBAC")
        self.current_user = "AdminUser"
        self.current_role = "ADMIN"

    def set_user(self, username, role):
        if role in self.ROLES:
            self.current_user = username
            self.current_role = role
            self.logger.info(f"User switched: {username} ({role})")
            return True
        return False

    def can(self, permission):
        """Checks if the current role has a specific permission."""
        perms = self.ROLES.get(self.current_role, {}).get("permissions", [])
        allowed = permission in perms
        if not allowed:
            self.logger.warning(f"PERMISSION DENIED: {self.current_user} attempted '{permission}'")
        return allowed

    def get_role_details(self):
        return self.ROLES.get(self.current_role, {})
