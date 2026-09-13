import time
import logging
from collections import deque
from .entropy_analysis import EntropyAnalyzer
from .honeypot import HoneypotManager

class DefenseSystem:
    """
    Analyzes events from the BehaviorMonitor and triggers defensive actions.
    Integrates Entropy analysis, Honeypot detection, AI Anomaly Engine, and Profiler.
    """
    def __init__(self, sandbox_manager=None, ai_engine=None, profiler=None, zero_trust=None, timeline=None, metrics=None):
        self.logger = logging.getLogger("DefenseSystem")
        self.event_history = deque(maxlen=100)
        self.threshold_rate = 10
        self.alarm_triggered = False
        self.auto_restore_enabled = False
        
        # Advanced Features
        self.ai = ai_engine
        self.profiler = profiler
        self.zero_trust = zero_trust
        self.timeline = timeline
        self.metrics = metrics
        self.risk_score = 0.0
        self.baseline_status = "Learning"
        self.entropy_analyzer = EntropyAnalyzer()
        self.honeypot_manager = HoneypotManager(sandbox_manager) if sandbox_manager else None
        self.honeypot_enabled = False

    def enable_honeypots(self):
        if self.honeypot_manager and not self.honeypot_enabled:
            self.honeypot_manager.deploy_honeypots()
            self.honeypot_enabled = True
            self.logger.info("Defense: Honeypots deployed.")

    def record_event(self, event_type, filepath):
        """
        Records an event and analyzes patterns.
        """
        current_time = time.time()
        self.event_history.append((current_time, event_type, filepath))
        
        # 0. Timeline & Metrics
        if self.timeline:
            self.timeline.add_event("FileSystem", event_type, str(filepath))
        if self.metrics:
            # We assume 'modified' on .encrypted files counts as encryption progress
            count = len([e for e in self.event_history if e[1] == 'modified'])
            self.metrics.update(count)

        # 1. Check Honeypot Access
        if self.honeypot_enabled and self.honeypot_manager.is_honeypot(filepath):
            self.trigger_alarm(reason=f"Honeypot Accessed: {filepath}")
            return

        # 2. Update Profiler
        if self.profiler:
            self.profiler.record_event(event_type)
            if not self.profiler.learning_mode:
                self.baseline_status = "Active"

        # 3. Check Entropy & AI
        if event_type == "modified":
            is_encrypted, entropy = self.entropy_analyzer.is_encrypted_suspect(filepath)
            
            # AI Inference
            if self.ai:
                features = {
                    "write_freq": len(self.event_history), 
                    "entropy": entropy,
                    "extension_change": filepath.endswith(".encrypted")
                }
                risk = self.ai.predict_risk(features)
                self.risk_score = risk
                
                if self.ai.is_anomaly(risk):
                    confidence = self.ai.get_confidence(risk)
                    self.logger.warning(f"AI ANOMALY: {confidence} confidence")
                    if risk > 0.9:
                        self.trigger_alarm(f"AI Detection ({confidence})")

            if is_encrypted:
                self.logger.warning(f"High Entropy ({entropy:.2f}) detected in {filepath}")

        self.analyze_behavior()

    def analyze_behavior(self):
        """
        Checks for high-frequency modifications.
        """
        if len(self.event_history) < 5:
            return

        current_time = time.time()
        recent_events = [e for e in self.event_history if current_time - e[0] < 1.0]
        
        if len(recent_events) > self.threshold_rate and not self.alarm_triggered:
            self.trigger_alarm(reason=f"Heuristic: {len(recent_events)} mods/sec")

    def trigger_alarm(self, reason="Unknown"):
        """
        Activates the defense mechanism.
        """
        if self.alarm_triggered:
            return

        self.alarm_triggered = True
        self.logger.critical(f"RANSOMWARE DETECTED! Reason: {reason}")

    def reset_alarm(self):
        self.alarm_triggered = False
        self.logger.info("Defense alarm reset.")

    def set_auto_restore(self, enabled):
        self.auto_restore_enabled = enabled
        self.logger.info(f"Auto-restore set to {enabled}")
