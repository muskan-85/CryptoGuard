
import unittest
import json
import shutil
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from cyber_lab.core.rbac_engine import RBACEngine
from cyber_lab.core.audit_logger import AuditLogger

class TestEnterpriseControls(unittest.TestCase):
    def setUp(self):
        self.rbac = RBACEngine()
        self.test_log = Path("tests/audit_test.json")
        if self.test_log.exists():
            self.test_log.unlink()
        self.audit = AuditLogger(log_file=self.test_log)

    def tearDown(self):
        if self.test_log.exists():
            self.test_log.unlink()

    def test_rbac_permissions(self):
        """Verify role permissions."""
        # Admin
        self.rbac.set_user("Admin", "ADMIN")
        self.assertTrue(self.rbac.can("attack"))
        self.assertTrue(self.rbac.can("restore"))
        
        # Auditor
        self.rbac.set_user("Auditor", "AUDITOR")
        self.assertFalse(self.rbac.can("attack"))
        self.assertFalse(self.rbac.can("restore"))
        self.assertTrue(self.rbac.can("view_audit"))

    def test_audit_hash_chain(self):
        """Verify audit log integrity and chaining."""
        self.audit.log_event("UserA", "LOGIN", "Success")
        self.audit.log_event("UserA", "ATTACK", "Initiated")
        
        # Check integrity
        intact, index = self.audit.verify_integrity()
        self.assertTrue(intact)
        
        # Tamper with file
        with open(self.test_log, "r") as f:
            data = json.load(f)
        
        data[0]["details"] = "TAMPERED" # Change data without updating hash
        
        with open(self.test_log, "w") as f:
            json.dump(data, f)
            
        # Verify integrity failure
        self.audit = AuditLogger(log_file=self.test_log)
        intact, index = self.audit.verify_integrity()
        self.assertFalse(intact)
        self.assertEqual(index, 0)

if __name__ == '__main__':
    unittest.main()
