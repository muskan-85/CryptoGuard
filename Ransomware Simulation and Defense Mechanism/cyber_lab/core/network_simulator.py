import logging
import random
import time
from concurrent.futures import ThreadPoolExecutor

class NetworkSimulator:
    """
    Simulates Network Traffic for the Cyber Range.
    - C2 (Command & Control) Heartbeats
    - DNS Tunneling / Beacons
    - Data Exfiltration (Fake upload traffic)
    """
    def __init__(self):
        self.logger = logging.getLogger("NetSim")
        self.active_connections = []
        self.c2_servers = ["192.168.1.55", "10.0.0.99", "evil-corp.xyz"]
        self.is_running = False

    def start_simulation(self):
        self.is_running = True
        self.active_connections = []
        self.logger.info("Network Simulation: STARTED")
        # In a real app we'd use a thread, here we'll just sim via updates
    
    def stop_simulation(self):
        self.is_running = False
        self.active_connections = []
        self.logger.info("Network Simulation: STOPPED")

    def simulate_tick(self):
        """
        Called periodically to generate fake traffic logs.
        """
        if not self.is_running:
            return None

        # 10% chance of C2 beacon
        if random.random() < 0.1:
            server = random.choice(self.c2_servers)
            event = {
                "timestamp": time.time(),
                "src": "192.168.1.105 (Local)",
                "dst": server,
                "protocol": "HTTPS",
                "type": "C2_BEACON",
                "size": f"{random.randint(100, 500)} bytes"
            }
            self.active_connections.append(event)
            return event
        
        # 5% chance of Data Exfiltration
        if random.random() < 0.05:
            event = {
                "timestamp": time.time(),
                "src": "192.168.1.105",
                "dst": "45.33.22.11 (Unknown)",
                "protocol": "FTP",
                "type": "DATA_EXFIL",
                "size": f"{random.randint(1, 10)} MB"
            }
            return event

        return None
