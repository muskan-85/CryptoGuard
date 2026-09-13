import logging
import logging.handlers
from pathlib import Path

class LoggingEngine:
    """
    Centralized logging for the application.
    Handles security audits and general application logs.
    """
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir).resolve()
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True)
        
        self.log_file = self.log_dir / "security.log"
        self._setup_logging()

    def _setup_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # File Handler (Rotating)
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_file, maxBytes=1024*1024, backupCount=5
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    def log_event(self, event_type, message, level="info"):
        """
        Custom method to log security events.
        """
        logger = logging.getLogger("SecurityAudit")
        log_msg = f"[{event_type.upper()}] {message}"
        
        if level == "info":
            logger.info(log_msg)
        elif level == "warning":
            logger.warning(log_msg)
        elif level == "error":
            logger.error(log_msg)
        elif level == "critical":
            logger.critical(log_msg)

    def get_logs(self, limit=50):
        """
        Retrieves the last N lines from the log file.
        """
        if not self.log_file.exists():
            return []
        
        with open(self.log_file, "r") as f:
            lines = f.readlines()
            return lines[-limit:]
