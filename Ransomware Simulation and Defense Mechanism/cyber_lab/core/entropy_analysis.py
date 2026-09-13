import math
import logging
from pathlib import Path

class EntropyAnalyzer:
    """
    Analyzes files for high entropy, a strong indicator of encryption.
    """
    def __init__(self):
        self.logger = logging.getLogger("EntropyAnalyzer")

    def calculate_entropy(self, filepath):
        """
        Calculates the Shannon entropy of a file.
        Returns a float between 0 and 8.
        """
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                
            if not data:
                return 0.0

            entropy = 0
            for x in range(256):
                p_x = float(data.count(x)) / len(data)
                if p_x > 0:
                    entropy += - p_x * math.log(p_x, 2)

            return entropy
        except Exception as e:
            self.logger.error(f"Error analyzing {filepath}: {e}")
            return 0.0

    def is_encrypted_suspect(self, filepath, threshold=7.5):
        """
        Determines if a file is likely encrypted based on entropy.
        Encrypted files usually have entropy close to 8.0.
        """
        entropy = self.calculate_entropy(filepath)
        is_suspect = entropy > threshold
        
        if is_suspect:
            self.logger.warning(f"High entropy ({entropy:.2f}) detected in {filepath}")
        
        return is_suspect, entropy
