
import unittest
import shutil
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from cyber_lab.core.pen_test_sim import PenTestSimulator
from cyber_lab.core.forensics_engine import ForensicsEngine
from cyber_lab.core.sandbox_manager import SandboxManager
from cyber_lab.core.backup_engine import BackupEngine

class TestTestingForensics(unittest.TestCase):
    def setUp(self):
        self.sandbox = SandboxManager(sandbox_path="tests/forensics_sandbox")
        self.backup = BackupEngine(self.sandbox, backup_dir="tests/forensics_backups")
        self.pen_test = PenTestSimulator(self.sandbox)
        self.forensics = ForensicsEngine(self.sandbox, self.backup)

    def tearDown(self):
        if Path("tests/forensics_sandbox").exists():
            shutil.rmtree("tests/forensics_sandbox")
        if Path("tests/forensics_backups").exists():
            shutil.rmtree("tests/forensics_backups")

    def test_pen_test_scan(self):
        """Verify scan results."""
        results = self.pen_test.run_scan()
        self.assertIn('findings', results)
        self.assertGreater(len(results['findings']), 0)
        self.assertTrue(results['threat_score'] > 0)

    def test_forensic_mem_dump(self):
        """Verify memory artifact generation."""
        dump = self.forensics.generate_memory_dump()
        self.assertTrue(dump['dump_id'].startswith("MEM_"))
        self.assertIn("REDEEM_YOUR_FILES", dump['suspicious_strings'])

if __name__ == '__main__':
    unittest.main()
