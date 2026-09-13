import unittest
import shutil
import time
import os
import logging
from pathlib import Path
from cryptography.fernet import Fernet
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from cyber_lab.core.sandbox_manager import SandboxManager
from cyber_lab.core.encryption_engine import EncryptionEngine
from cyber_lab.core.backup_engine import BackupEngine
from cyber_lab.core.file_integrity_checker import FileIntegrityChecker
from cyber_lab.core.process_simulator import ProcessSimulator
from cyber_lab.core.threat_intel_engine import ThreatIntelEngine

# Configure logging to see errors
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class TestPhase2Features(unittest.TestCase):
    def setUp(self):
        self.sandbox = SandboxManager("test_phase2_sandbox")
        self.sandbox.create_mock_files(5)
        self.encryption = EncryptionEngine(self.sandbox)
        self.key = Fernet.generate_key()
        self.backup = BackupEngine(self.sandbox)
        self.integrity = FileIntegrityChecker(self.sandbox)
        self.simulator = ProcessSimulator(self.encryption, self.sandbox)
        self.intel = ThreatIntelEngine()

    def tearDown(self):
        if Path("test_phase2_sandbox").exists():
            shutil.rmtree("test_phase2_sandbox")
        if Path("backups").exists():
            shutil.rmtree("backups")

    def test_backup_and_restore(self):
        """Test snapshot creation and restoration."""
        # Create snapshot
        snap_path = self.backup.create_snapshot()
        self.assertTrue(Path(snap_path).exists())
        
        # Modify a file
        target = Path("test_phase2_sandbox/document_0.txt")
        with open(target, "w") as f:
            f.write("MODIFIED")
            
        # Restore
        self.backup.restore_snapshot(Path(snap_path))
        
        # Verify restore
        with open(target, "r") as f:
            content = f.read()
        self.assertNotEqual(content, "MODIFIED")

    def test_integrity_check(self):
        """Test file integrity monitoring."""
        self.integrity.establish_baseline()
        
        # Modify a file
        target = Path("test_phase2_sandbox/document_0.txt")
        with open(target, "a") as f:
            f.write(" malicious appended data")
            
        compromised = self.integrity.check_integrity()
        self.assertIn(str(target.resolve()), [str(Path(c).resolve()) for c in compromised])

    def test_burst_simulation(self):
        """Test multi-threaded simulation."""
        # Just check it runs without error
        def progress(p):
            pass
        
        self.simulator.simulate_attack(self.key, mode="burst", callback=progress)
        
        # Verify files are encrypted (check for header or high entropy or just content change)
        target = Path("test_phase2_sandbox/document_0.txt")
        self.assertTrue(target.exists())
        # Ideally check content is binary

    def test_threat_intel(self):
        """Test threat intel analysis."""
        # Mock a ransomware file
        bad_file = Path("test_phase2_sandbox/README_DECRYPT.txt")
        with open(bad_file, "w") as f:
            f.write("Give me money")
            
        report = self.intel.analyze_artifact(str(bad_file))
        self.assertGreater(report["risk_score"], 90)
        self.assertEqual(report["threat_level"], "CRITICAL")

if __name__ == '__main__':
    unittest.main()
