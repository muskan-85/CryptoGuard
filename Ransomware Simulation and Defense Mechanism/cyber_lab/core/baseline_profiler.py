import logging
import time
from collections import deque

class BaselineProfiler:
    """
    Learns 'Normal' system behavior over time.
    Tracks metrics to establish a baseline for anomaly detection.
    """
    def __init__(self, learning_period_seconds=30):
        self.logger = logging.getLogger("BaselineProfiler")
        self.history = deque(maxlen=100) # Store last 100 events
        self.learning_mode = True
        self.learning_start = time.time()
        self.learning_period = learning_period_seconds
        self.baseline_stats = {
            "avg_writes_per_sec": 0.0,
            "std_dev_writes": 0.0
        }

    def record_event(self, event_type, count=1):
        """
        Records an event and updates internal logic.
        """
        if self.learning_mode:
            self.history.append((time.time(), count))
            if time.time() - self.learning_start > self.learning_period:
                self._finalize_learning()

    def _finalize_learning(self):
        """
        Calculates baseline statistics from history.
        """
        self.learning_mode = False
        self.logger.info("Baseline Learning Complete.")
        
        # Calculate stats
        total_events = sum(c for t, c in self.history)
        duration = self.history[-1][0] - self.history[0][0] if len(self.history) > 1 else 1
        
        self.baseline_stats["avg_writes_per_sec"] = total_events / max(duration, 1)
        self.logger.info(f"Baseline established: {self.baseline_stats}")

    def get_deviation(self, current_rate):
        """
        Returns deviations from baseline (Z-score simulated).
        """
        if self.learning_mode:
            return 0.0
            
        avg = self.baseline_stats["avg_writes_per_sec"]
        if avg == 0: return 0.0
        
        deviation = (current_rate - avg) / avg
        return deviation
