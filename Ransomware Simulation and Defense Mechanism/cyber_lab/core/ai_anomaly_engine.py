import random
import logging
import math

class AIAnomalyEngine:
    """
    Simulates an AI-powered Anomaly Detection System (Isolation Forest Model).
    Calculates a 'Risk Probability Score' based on feature vectors.
    """
    def __init__(self):
        self.logger = logging.getLogger("AIAnomalyEngine")
        self.weights = {
            "write_frequency": 0.4,
            "entropy_variance": 0.3,
            "file_extension_anomaly": 0.2,
            "time_of_day_anomaly": 0.1
        }
        self.risk_threshold = 0.75

    def predict_risk(self, features):
        """
        Calculates risk score (0.0 to 1.0) based on input features.
        Features expected:
        - write_freq (norm 0-1): Writes per second normalized
        - entropy (norm 0-1): Average entropy of touched files
        - extension_change (bool): 1.0 if extensions are changing
        """
        # Feature extraction
        w_freq = min(features.get("write_freq", 0) / 50.0, 1.0) # Cap at 50/sec
        w_entropy = 1.0 if features.get("entropy", 0) > 7.0 else 0.2
        w_ext = 1.0 if features.get("extension_change", False) else 0.0
        w_time = 0.1 # Mock constant

        # Weighted Sum (Linear Regression Simulation)
        score = (
            w_freq * self.weights["write_frequency"] +
            w_entropy * self.weights["entropy_variance"] +
            w_ext * self.weights["file_extension_anomaly"] +
            w_time * self.weights["time_of_day_anomaly"]
        )
        
        # Sigmoid-ish smoothing
        risk_probability = 1 / (1 + math.exp(-10 * (score - 0.5)))
        
        return risk_probability

    def get_confidence(self, risk_score):
        """
        Returns confidence percentage string.
        """
        return f"{int(risk_score * 100)}%"

    def is_anomaly(self, risk_score):
        return risk_score > self.risk_threshold
