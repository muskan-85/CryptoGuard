
import unittest
import shutil
import os
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from cyber_lab.core.sandbox_manager import SandboxManager
from cyber_lab.core.encryption_engine import EncryptionEngine
from cyber_lab.core.decryption_engine import DecryptionEngine
from cyber_lab.core.key_manager import KeyManager
from cyber_lab.core.backup_engine import BackupEngine
from cyber_lab.core.behavior_monitor import BehaviorMonitor
from cyber_lab.core.defense_system import DefenseSystem
from cyber_lab.core.ai_anomaly_engine import AIAnomalyEngine
from cyber_lab.core.baseline_profiler import BaselineProfiler
from cyber_lab.core.zero_trust_engine import ZeroTrustEngine
from cyber_lab.core.report_generator import ReportGenerator
from cyber_lab.core.timeline_builder import TimelineBuilder
from cyber_lab.core.forensics_engine import ForensicsEngine

class TestFullIntegration(unittest.TestCase):
    def setUp(self):
        self.root = Path("tests/integration_full")
        if self.root.exists():
            shutil.rmtree(self.root)
        self.root.mkdir(parents=True)
        
        self.sandbox = SandboxManager(sandbox_path=self.root / "sandbox")
        self.keys = KeyManager(key_dir=self.root / "keys")
        self.backup = BackupEngine(self.sandbox, backup_dir=self.root / "backups")
        
        self.encryptor = EncryptionEngine(self.sandbox)
        self.decryptor = DecryptionEngine(self.sandbox)
        
        # AI/Defense
        self.ai = AIAnomalyEngine()
        self.profiler = BaselineProfiler(learning_period_seconds=1) # Short for test
        self.zero_trust = ZeroTrustEngine()
        
        self.defense = DefenseSystem(self.sandbox, self.ai, self.profiler, self.zero_trust)
        self.monitor = BehaviorMonitor(self.sandbox, self.defense)
        
        # Reporting/Forensics
        self.timeline = TimelineBuilder()
        self.report_gen = ReportGenerator(self.sandbox, self.timeline)
        self.forensics = ForensicsEngine(self.sandbox, self.backup)

    def tearDown(self):
        if self.root.exists():
            shutil.rmtree(self.root)

    def test_full_attack_defend_cycle(self):
        """Runs a complete end-to-end simulation cycle."""
        # 1. Setup Sandbox
        self.sandbox.create_mock_files()
        files = list(self.root.glob("sandbox/*"))
        self.assertGreater(len(files), 0)
        
        # 2. Baseline Profiling (Already started in init)
        time.sleep(1.1) # Wait for learning to finish
        
        # 3. Create Backup
        self.backup.create_snapshot()
        self.assertGreater(len(list((self.root / "backups").glob("snapshot_*"))), 0)
        
        # 4. simulated Attack
        key = self.keys.load_key()
        # Mock some events into defense system
        self.defense.record_event('modified', str(files[0]))
        
        # 5. Encryption
        self.encryptor.encrypt_sandbox(key)
        
        # 6. Verify Encryption
        enc_files = self.sandbox.list_files()
        self.assertGreater(len(enc_files), 0)
        
        # 7. Forensics
        report = self.forensics.analyze_file_compromise(enc_files[0])
        self.assertEqual(report['status'], "COMPROMISED")
        
        # 8. Decryption
        self.decryptor.decrypt_sandbox(key)
        
        # 9. Verify Restoration
        restored_files = list(self.root.glob("sandbox/*.enc"))
        self.assertEqual(len(restored_files), 0)
        
        # 10. Generate Report
        repo_path = self.report_gen.generate_report("INT-TEST-001", {"encrypted_count": len(enc_files)})
        self.assertTrue(Path(repo_path).exists())

if __name__ == '__main__':
    unittest.main()
