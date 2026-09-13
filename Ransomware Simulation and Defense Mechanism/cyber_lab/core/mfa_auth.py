import pyotp
import qrcode
import time
import logging
from io import BytesIO

class MFAAuthenticator:
    """
    Simulates Multi-Factor Authentication using TOTP (Time-based One-Time Password).
    Compatible with Google Authenticator apps (conceptually).
    """
    def __init__(self):
        self.logger = logging.getLogger("MFA")
        # In a real scenario, this secret would be unique per user and securely stored.
        # For simulation, we use a fixed base32 secret or generate one.
        self.secret = pyotp.random_base32()
        self.totp = pyotp.TOTP(self.secret)
        self.enabled = False

    def enable_mfa(self):
        self.enabled = True
        self.logger.info("MFA Enabled. Secret generated.")
        return self.secret

    def get_provisioning_uri(self, user="admin@cyberlab.local"):
        return self.totp.provisioning_uri(name=user, issuer_name="CyberLab")

    def verify_token(self, token):
        """
        Verifies the 6-digit code.
        """
        if not self.enabled:
            return True # Bypass if not enabled
            
        return self.totp.verify(token)

    def generate_current_token(self):
        """
        For simulation testing purposes only.
        """
        return self.totp.now()
