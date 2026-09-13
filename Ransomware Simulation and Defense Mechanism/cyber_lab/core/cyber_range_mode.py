import logging
import time

class CyberRangeMode:
    """
    Gamifies the simulation with 'Red Team' vs 'Blue Team' scoring.
    Tracks points based on successful attacks vs successful defenses.
    """
    def __init__(self):
        self.logger = logging.getLogger("CyberRange")
        self.red_score = 0
        self.blue_score = 0
        self.round_active = False
        self.start_time = 0
        self.duration = 60 # 60 seconds round
        self.objectives = {
            "files_encrypted": 0, # Red Point
            "attacks_blocked": 0, # Blue Point
            "honeypots_triggered": 0, # Blue Point (High Value)
            "system_restored": 0 # Blue Point
        }

    def start_round(self):
        self.round_active = True
        self.start_time = time.time()
        self.red_score = 0
        self.blue_score = 0
        self.objectives = {k: 0 for k in self.objectives}
        self.logger.info("CYBER RANGE: Round Started!")

    def update_score(self, event_type, points=10):
        if not self.round_active:
            return

        if event_type == "encryption_success":
            self.red_score += points
            self.objectives["files_encrypted"] += 1
        elif event_type == "attack_blocked":
            self.blue_score += points
            self.objectives["attacks_blocked"] += 1
        elif event_type == "honeypot_catch":
            self.blue_score += points * 5 # Bonus
            self.objectives["honeypots_triggered"] += 1
        elif event_type == "restore_success":
            self.blue_score += points * 2
            self.objectives["system_restored"] += 1

        self._check_time()

    def _check_time(self):
        if time.time() - self.start_time > self.duration:
            self.end_round()

    def end_round(self):
        self.round_active = False
        winner = "BLUE TEAM" if self.blue_score > self.red_score else "RED TEAM"
        self.logger.info(f"CYBER RANGE: Round Over. Winner: {winner} (B:{self.blue_score} - R:{self.red_score})")

    def get_status(self):
        return {
            "active": self.round_active,
            "time_left": max(0, int(self.duration - (time.time() - self.start_time))) if self.round_active else 0,
            "red_score": self.red_score,
            "blue_score": self.blue_score,
            "objectives": self.objectives
        }
