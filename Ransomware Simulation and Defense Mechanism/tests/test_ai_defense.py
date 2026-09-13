
import unittest
import time
import shutil
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from cyber_lab.core.ai_anomaly_engine import AIAnomalyEngine
from cyber_lab.core.baseline_profiler import BaselineProfiler
from cyber_lab.core.defense_system import DefenseSystem
from cyber_lab.core.sandbox_manager import SandboxManager

class TestAIDefense(unittest.TestCase):
    def setUp(self):
        self.ai = AIAnomalyEngine()
        self.profiler = BaselineProfiler(learning_period_seconds=1)
        self.sandbox = SandboxManager("test_ai_sandbox")
        self.sandbox.create_mock_files(1)
        self.defense = DefenseSystem(self.sandbox, self.ai, self.profiler)

    def tearDown(self):
        if Path("test_ai_sandbox").exists():
            shutil.rmtree("test_ai_sandbox")

    def test_ai_scoring(self):
        """Test that high frequency + entropy triggers high risk."""
        features = {
            "write_freq": 100,
            "entropy": 8.0,
            "extension_change": True
        }
        score = self.ai.predict_risk(features)
        self.assertGreater(score, 0.8)
        self.assertTrue(self.ai.is_anomaly(score))

    def test_baseline_learning(self):
        """Test that profiler learns and switches mode."""
        self.assertTrue(self.profiler.learning_mode)
        self.profiler.record_event("write", 1)
        time.sleep(1.1) 
        self.profiler.record_event("write", 1) # Should trigger finalize
        self.assertFalse(self.profiler.learning_mode)

    def test_defense_integration(self):
        """Test that defense system updates risk score."""
        self.defense.record_event("modified", "test_ai_sandbox/document_0.txt")
        # Should have called AI
        # Since we didn't mock AI, it ran real logic. 
        # With 1 event, freq is low, entropy 0 (file doesn't exist/empty). Risk should be low.
        self.assertLess(self.defense.risk_score, 0.5)

if __name__ == '__main__':
    unittest.main()
