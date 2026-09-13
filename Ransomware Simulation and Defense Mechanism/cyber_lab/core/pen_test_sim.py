import random
import time
import logging

class PenTestSimulator:
    """
    Simulates automated penetration testing activities.
    - Reconnaissance / Scanning
    - Vulnerability Assessment
    - Exploit Attempt (Mock)
    """
    def __init__(self, target_sandbox):
        self.sandbox = target_sandbox
        self.logger = logging.getLogger("PenTestSim")
        self.last_results = {}

    def run_scan(self):
        """Simulates a vulnerability scan of the sandbox."""
        self.logger.info("Starting Pen-Test Scan...")
        time.sleep(1)
        
        findings = [
            {"id": "VULN-01", "name": "Weak File Permissions", "severity": "Medium"},
            {"id": "VULN-02", "name": "Simulated Buffer Overflow Path", "severity": "High"},
            {"id": "VULN-03", "name": "Insecure Backup Config", "severity": "Low"}
        ]
        
        # Randomize findings for realism
        results = random.sample(findings, k=random.randint(1, 3))
        self.last_results = {
            "timestamp": time.time(),
            "findings": results,
            "threat_score": sum([5 if f['severity'] == "High" else 2 for f in results])
        }
        return self.last_results

    def simulate_exploit(self, vuln_id):
        """Attempts to 'exploit' a finding."""
        self.logger.info(f"Attempting to exploit {vuln_id}...")
        time.sleep(2)
        
        # 70% success rate for simulation
        success = random.random() > 0.3
        
        if success:
            self.logger.error(f"EXPLOIT SUCCESSFUL: Gained mock access via {vuln_id}")
            return True, "Exploit successful. System simulation compromised."
        else:
            self.logger.info(f"Exploit failed for {vuln_id}")
            return False, "Access attempt blocked by Zero Trust simulation."
