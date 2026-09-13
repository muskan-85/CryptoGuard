import json
import logging
from pathlib import Path
from datetime import datetime

class ThreatIntelEngine:
    """
    Simulated Threat Intelligence Engine.
    - Maintains a mock database of IOCs (Indicators of Compromise).
    - Maps events to MITRE ATT&CK framework.
    - Calculates Risk Scores based on file artifacts.
    """
    def __init__(self):
        self.logger = logging.getLogger("ThreatIntel")
        self.known_iocs = self._load_mock_iocs()

    def _load_mock_iocs(self):
        return {
            "file_extensions": [".encrypted", ".locked", ".cry", ".wnry"],
            "hashes": [
                # Mock known bad hashes
                "d41d8cd98f00b204e9800998ecf8427e", # Empty file MD5
                "5d41402abc4b2a76b9719d911017c592"  # 'hello' MD5
            ],
            "ransom_notes": ["README_DECRYPT.txt", "YOUR_FILES_ARE_ENCRYPTED.txt"]
        }

    def analyze_artifact(self, filepath):
        """
        Analyzes a file artifact against known IOCs.
        Returns a Risk Score (0-100) and matched threats.
        """
        path = Path(filepath)
        score = 0
        matches = []

        # Check Extension
        if path.suffix in self.known_iocs["file_extensions"]:
            score += 80
            matches.append(f"Known Ransomware Extension: {path.suffix}")

        # Check Filename (Ransom Note)
        if path.name in self.known_iocs["ransom_notes"]:
            score += 95
            matches.append(f"Known Ransom Note Found: {path.name}")

        threat_level = "LOW"
        if score >= 80:
            threat_level = "CRITICAL"
        elif score >= 50:
            threat_level = "HIGH"
        elif score > 0:
            threat_level = "MEDIUM"

        return {
            "risk_score": score,
            "threat_level": threat_level,
            "matches": matches,
            "mitre_tactic": "Impact",
            "mitre_technique": "Data Encrypted for Impact (T1486)"
        }

    def get_feed_summary(self):
        """
        Returns a summary of the simulated threat feed.
        """
        return {
            "source": "Mock Threat Feed v1.0",
            "total_signatures": len(self.known_iocs["file_extensions"]) + len(self.known_iocs["hashes"]),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
