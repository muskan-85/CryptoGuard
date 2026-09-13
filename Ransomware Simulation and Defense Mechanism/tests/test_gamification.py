
import unittest
import time
import shutil
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from cyber_lab.core.cyber_range_mode import CyberRangeMode
from cyber_lab.core.network_simulator import NetworkSimulator

class TestGamification(unittest.TestCase):
    def setUp(self):
        self.range_mode = CyberRangeMode()
        self.net_sim = NetworkSimulator()

    def test_cyber_range_scoring(self):
        """Test Red vs Blue scoring logic."""
        self.range_mode.start_round()
        self.assertTrue(self.range_mode.round_active)
        
        # Test Blue Points
        self.range_mode.update_score("attack_blocked", 10)
        status = self.range_mode.get_status()
        self.assertEqual(status['blue_score'], 10)
        
        # Test Red Points
        self.range_mode.update_score("encryption_success", 50)
        status = self.range_mode.get_status()
        self.assertEqual(status['red_score'], 50)
        
        self.range_mode.end_round()
        self.assertFalse(self.range_mode.round_active)

    def test_network_simulation(self):
        """Test traffic generation."""
        self.net_sim.start_simulation()
        self.assertTrue(self.net_sim.is_running)
        
        # Simulate a few ticks
        events = []
        for _ in range(50):
            e = self.net_sim.simulate_tick()
            if e: events.append(e)
            
        self.assertGreater(len(events), 0)
        self.net_sim.stop_simulation()
        self.assertFalse(self.net_sim.is_running)

if __name__ == '__main__':
    unittest.main()
