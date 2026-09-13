import logging
import random
from PySide6.QtWidgets import QMessageBox

class SocialEngineeringSim:
    """
    Simulates Social Engineering attacks.
    - Phishing Popups
    - 'Update Required' fake prompts
    """
    def __init__(self):
        self.logger = logging.getLogger("SocialEng")
    
    def trigger_phishing_attempt(self, parent_widget):
        """
        Launches a mock phishing dialog.
        Returns True if user 'fell for it' (clicked Yes/Open).
        """
        scenarios = [
            ("URGENT: Payroll Update Required", "Your payroll details are outdated. Click OK to update immediately to avoid payment delays."),
            ("Security Alert", "Microsoft Windows has detected a virus. Click OK to install the patch."),
            ("FREE GIFT CARD", "You won a $500 Amazon Gift Card! Claim now?")
        ]
        
        title, text = random.choice(scenarios)
        
        # We use a standard MessageBox for simulation
        msg = QMessageBox(parent_widget)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Ok)
        
        ret = msg.exec_()
        
        if ret == QMessageBox.Ok:
            self.logger.warning(f"USER FAILED PHISHING TEST: {title}")
            return True # Failed
        else:
            self.logger.info(f"User passed phishing test: {title}")
            return False # Passed
