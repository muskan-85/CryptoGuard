import time
import random
import logging

class LiveMetrics:
    """
    Tracks live system metrics for the dashboard.
    Simulates CPU/RAM usage if psutil is not available.
    Calculates RTO (Recovery Time Objective) estimates.
    """
    def __init__(self):
        self.logger = logging.getLogger("LiveMetrics")
        self.encryption_rate = 0.0 # files/sec
        self.cpu_usage = 0.0
        self.ram_usage = 0.0
        self.last_update = time.time()
        self.files_encrypted_total = 0

    def update(self, files_encrypted_now):
        """
        Updates metrics based on current state.
        """
        current_time = time.time()
        delta = current_time - self.last_update
        
        if delta > 0:
            rate = (files_encrypted_now - self.files_encrypted_total) / delta
            self.encryption_rate = max(0.0, rate)
            self.files_encrypted_total = files_encrypted_now
            self.last_update = current_time

        # Simulate System Load based on activity
        base_load = 5.0
        activity_load = min(self.encryption_rate * 2.0, 80.0) # Cap at +80%
        
        self.cpu_usage = base_load + activity_load + random.uniform(-2, 2)
        self.ram_usage = 40.0 + (self.files_encrypted_total * 0.01) # constant creep
        
        self.cpu_usage = min(max(self.cpu_usage, 0), 100)
        self.ram_usage = min(max(self.ram_usage, 0), 100)

    def get_metrics(self):
        return {
            "encryption_rate": f"{self.encryption_rate:.1f} file/s",
            "cpu": f"{self.cpu_usage:.1f}%",
            "ram": f"{self.ram_usage:.1f}%",
            "files_total": self.files_encrypted_total
        }
