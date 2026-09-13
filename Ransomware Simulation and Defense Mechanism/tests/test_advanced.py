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
from cyber_lab.core.entropy_analysis import EntropyAnalyzer
from cyber_lab.core.honeypot import HoneypotManager
from cyber_lab.core.defense_system import DefenseSystem
from cyber_lab.core.report_generator import ReportGenerator

class TestAdvancedFeatures(unittest.TestCase):
    def setUp(self):
        self.sandbox = SandboxManager("test_adv_sandbox")
        self.sandbox.create_mock_files(5)
        self.encryption = EncryptionEngine(self.sandbox)
        self.key = Fernet.generate_key()
        self.entropy = EntropyAnalyzer()
        self.honeypot = HoneypotManager(self.sandbox)
        self.report = ReportGenerator("test_logs")

    def tearDown(self):
        if Path("test_adv_sandbox").exists():
            shutil.rmtree("test_adv_sandbox")
        if Path("test_logs").exists():
            shutil.rmtree("test_logs")

    def test_entropy_analysis(self):
        """Test entropy calculation on encrypted vs plain files."""
        plain_file = Path("test_adv_sandbox/document_0.txt")
        
        # Plain text entropy should be low
        e_plain = self.entropy.calculate_entropy(str(plain_file))
        self.assertLess(e_plain, 6.0)

        # Encrypt the file
        self.encryption.encrypt_file(str(plain_file), self.key)
        
        # Encrypted entropy should be high (> 7.5 usually)
        e_enc = self.entropy.calculate_entropy(str(plain_file))
        self.assertGreater(e_enc, 7.0) 

    def test_honeypot_deployment(self):
        """Test honeypot creation and detection."""
        self.honeypot.deploy_honeypots()
        
        # Check files exist
        honey_file = Path("test_adv_sandbox/passwords.txt")
        self.assertTrue(honey_file.exists())
        
        # Check detection
        self.assertTrue(self.honeypot.is_honeypot(str(honey_file)))
        
        # Check normal file is not honeypot
        normal_file = Path("test_adv_sandbox/document_0.txt")
        self.assertFalse(self.honeypot.is_honeypot(str(normal_file)))

    def test_report_generation(self):
        """Test report generation."""
        events = [
            ("timestamp", "modified", "file.txt"),
            ("timestamp", "CRITICAL", "Ransomware Detected")
        ]
        status = {"active": True}
        
        report_path = self.report.generate_report(events, status)
        self.assertTrue(Path(report_path).exists())

if __name__ == '__main__':
    unittest.main()
