import os
import random
import logging
from pathlib import Path

class HoneypotManager:
    """
    Advanced Honeypot capabilities.
    - Hidden Directories (e.g., .ssh, AppData)
    - Fake Database Files (.sql, .db)
    - Decoy Credentials (config.xml, id_rsa)
    """
    def __init__(self, sandbox_manager):
        self.logger = logging.getLogger("HoneypotManager")
        self.sandbox = sandbox_manager
        self.honeypots = set()
        self.hidden_dirs = [".ssh", ".aws", "AppData/Local/Temp", "Backup"]
        self.decoy_files = [
            ("passwords.txt", "admin:admin123\nroot:toor"),
            ("financials_2024.xlsx", "CONFIDENTIAL DATA"), # Mock content
            ("id_rsa", "-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEA..."),
            ("wallet.dat", "0000000000000000"),
            ("clients.db", "SQLite format 3...")
        ]

    def deploy_honeypots(self):
        """
        Deploys advanced honeypots deep in the sandbox structure.
        """
        base = self.sandbox.sandbox_path
        
        # 1. Create Hidden Directories
        for d in self.hidden_dirs:
            dir_path = base / d
            dir_path.mkdir(parents=True, exist_ok=True)
            self._create_decoy_in_dir(dir_path)

        # 2. Create Root Decoys
        self._create_decoy_in_dir(base)
        
        # 3. Random subdirectory decoys
        subdirs = [x for x in base.iterdir() if x.is_dir()]
        for d in subdirs:
             if random.random() > 0.5:
                 self._create_decoy_in_dir(d)

        self.logger.info(f"Deployed {len(self.honeypots)} advanced honeypots.")

    def _create_decoy_in_dir(self, directory):
        # Pick 1-2 random decoys per directory
        selected = random.sample(self.decoy_files, k=min(2, len(self.decoy_files)))
        
        for name, content in selected:
            path = directory / name
            try:
                # add hidden attribute prefix if on windows? 
                # For now just standard files
                with open(path, "w", encoding='utf-8') as f:
                    f.write(content)
                self.honeypots.add(str(path))
            except Exception as e:
                self.logger.error(f"Failed to create honeypot {path}: {e}")

    def is_honeypot(self, filepath):
        return str(filepath) in self.honeypots
