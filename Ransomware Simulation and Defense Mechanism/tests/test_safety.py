import unittest
import shutil
import os
from pathlib import Path
from cryptography.fernet import Fernet
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from cyber_lab.core.sandbox_manager import SandboxManager
from cyber_lab.core.encryption_engine import EncryptionEngine
from cyber_lab.core.decryption_engine import DecryptionEngine
from cyber_lab.core.key_manager import KeyManager

class TestRansomwareSimulation(unittest.TestCase):
    def setUp(self):
        self.sandbox = SandboxManager("test_sandbox")
        self.sandbox.create_mock_files(5)
        self.key_manager = KeyManager("test_keys")
        self.encryption = EncryptionEngine(self.sandbox)
        self.decryption = DecryptionEngine(self.sandbox)
        self.key = self.key_manager.generate_key()

    def tearDown(self):
        if Path("test_sandbox").exists():
            shutil.rmtree("test_sandbox")
        if Path("test_keys").exists():
            shutil.rmtree("test_keys")

    def test_sandbox_isolation(self):
        """Test that operations outside sandbox are blocked."""
        outside_file = Path("outside.txt")
        with open(outside_file, "w") as f:
            f.write("sensitive data")
        
        try:
            # Attempt to encrypt file outside sandbox
            with self.assertRaises(PermissionError):
                self.encryption.encrypt_file(str(outside_file.resolve()), self.key)
        finally:
            if outside_file.exists():
                os.remove(outside_file)

    def test_encryption_decryption_flow(self):
        """Test the full encryption and decryption cycle."""
        test_file = Path("test_sandbox/document_0.txt")
        original_content = test_file.read_text()

        # Encrypt
        self.encryption.encrypt_file(str(test_file), self.key)
        
        # Encrypted content is now raw binary, so we must read as bytes
        encrypted_content = test_file.read_bytes()
        self.assertNotEqual(original_content.encode(), encrypted_content)

        # Decrypt
        self.decryption.decrypt_file(str(test_file), self.key)
        decrypted_content = test_file.read_text()
        self.assertEqual(original_content, decrypted_content)

    def test_sandbox_bulk_operations(self):
        """Test bulk encryption/decryption of the sandbox."""
        # Encrypt all
        encrypted_count = self.encryption.encrypt_sandbox(self.key)
        self.assertEqual(encrypted_count, 5)

        # check if all files are encrypted (naive check: content changed)
        # In a real test we'd check for header or similar, but here we just assume change
        
        # Decrypt all
        decrypted_count = self.decryption.decrypt_sandbox(self.key)
        self.assertEqual(decrypted_count, 5)

if __name__ == '__main__':
    unittest.main()
