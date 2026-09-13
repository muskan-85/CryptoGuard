
import unittest
import shutil
import sys
from pathlib import Path
import time

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from cyber_lab.core.key_manager import KeyManager
from cyber_lab.core.mfa_auth import MFAAuthenticator

class TestKeyManagement(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests/test_keys")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.keys = KeyManager(key_dir=self.test_dir)
        self.mfa = MFAAuthenticator()

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_key_rotation(self):
        """Test key generation and rotation archival."""
        # 1. Generate Initial Key
        key1 = self.keys.load_key()
        self.assertTrue((self.test_dir / "secret.key").exists())
        
        # 2. Rotate Key
        time.sleep(1) # Ensure timestamp diff
        key2 = self.keys.generate_key()
        
        self.assertNotEqual(key1, key2)
        
        # 3. Check Archive
        archives = list(self.keys.archive_dir.glob("*.key"))
        self.assertEqual(len(archives), 1)
        self.assertTrue(archives[0].name.startswith("secret_"))

    def test_mfa(self):
        """Test MFA simulation."""
        self.assertFalse(self.mfa.enabled)
        
        # 1. Enable MFA
        secret = self.mfa.enable_mfa()
        self.assertTrue(self.mfa.enabled)
        self.assertIsNotNone(secret)
        
        # 2. Verify Token
        token = self.mfa.generate_current_token()
        self.assertTrue(self.mfa.verify_token(token))
        
        # 3. Verify Bad Token
        self.assertFalse(self.mfa.verify_token("000000"))

if __name__ == '__main__':
    unittest.main()
