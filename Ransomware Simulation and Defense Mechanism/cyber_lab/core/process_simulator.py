import time
import random
import threading
import concurrent.futures
import logging
from pathlib import Path

class ProcessSimulator:
    """
    Simulates various ransomware behavior patterns.
    - Burst Mode: Multi-threaded rapid encryption.
    - Stealth Mode: Slow, delayed encryption to evade detection.
    - Random Walk: Encrypts files in random order.
    """
    def __init__(self, encryption_engine, sandbox_manager):
        self.engine = encryption_engine
        self.sandbox = sandbox_manager
        self.logger = logging.getLogger("ProcessSimulator")
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def simulate_attack(self, key, mode="standard", callback=None):
        """
        Orchestrates the attack based on the selected mode.
        """
        self._stop_event.clear()
        files = self.sandbox.list_files()
        total_files = len(files)
        
        if mode == "burst":
            self._burst_attack(files, key, callback)
        elif mode == "stealth":
            self._stealth_attack(files, key, callback)
        else:
            # Standard sequential
            self.engine.encrypt_sandbox(key, callback)

    def _burst_attack(self, files, key, callback):
        """
        Uses ThreadPoolExecutor to encrypt files in parallel.
        Simulates high-speed "LockBit" style attacks.
        """
        self.logger.info("Starting BURST attack simulation...")
        processed = 0
        total = len(files)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(self.engine.encrypt_file, f, key): f for f in files}
            
            for future in concurrent.futures.as_completed(futures):
                if self._stop_event.is_set():
                    break
                try:
                    future.result()
                    processed += 1
                    if callback:
                        progress = int((processed / total) * 100)
                        callback(progress)
                except Exception as e:
                    self.logger.error(f"Encryption failed: {e}")

    def _stealth_attack(self, files, key, callback):
        """
        Encrypts files with random delays between operations.
        Designed to evade heuristic rate-limiters.
        """
        self.logger.info("Starting STEALTH attack simulation...")
        random.shuffle(files)
        
        for i, f in enumerate(files):
            if self._stop_event.is_set():
                break
            
            try:
                self.engine.encrypt_file(f, key)
                # Random delay 0.5s to 2.0s
                time.sleep(random.uniform(0.5, 2.0))
                
                if callback:
                    progress = int(((i + 1) / len(files)) * 100)
                    callback(progress)
            except Exception as e:
                self.logger.error(f"Encryption failed: {e}")
