
import logging
from pathlib import Path

class SignatureVerifier:
    """
    Simulates digital signature verification for executables.
    In a real scenario, this would check Authenticode signatures.
    Here, it checks against a 'trusted' whitelist of simulated hashes/names.
    """
    def __init__(self):
        self.logger = logging.getLogger("SignatureVerifier")
        self.trusted_signers = [
            "Microsoft Corporation",
            "CyberLab Defense Systems",
            "Trusted Vendor Inc."
        ]
        self.whitelist_hashes = [
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" # Example hash
        ]

    def verify_signature(self, filepath):
        """
        Simulates verifying the signature of a file.
        Returns (is_valid, signer_name).
        """
        path = Path(filepath)
        if not path.exists():
            return False, "File Not Found"

        # Simulation Logic:
        # If file name starts with "safe_", it's signed by trusted vendor.
        # If it starts with "unknown_", it's unsigned.
        # If it starts with "malware_", it's invalid signature.
        
        filename = path.name.lower()
        
        if filename.startswith("safe_") or filename == "app.py":
            return True, "CyberLab Defense Systems"
        
        if filename.startswith("ms_"):
            return True, "Microsoft Corporation"
            
        if filename.startswith("malware_") or filename == "ransomware.py":
            return False, "Invalid Signature"
            
        return False, "Unsigned"

    def is_trusted(self, filepath):
        is_valid, signer = self.verify_signature(filepath)
        if is_valid and signer in self.trusted_signers:
            return True
        return False
