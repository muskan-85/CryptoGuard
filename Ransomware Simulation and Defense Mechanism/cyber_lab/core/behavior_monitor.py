from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from pathlib import Path
import time
from .sandbox_manager import SandboxManager

class BehaviorMonitor(FileSystemEventHandler):
    """
    Monitors file system events within the sandbox to detect suspicious activity.
    """
    def __init__(self, sandbox_manager: SandboxManager, defense_system):
        self.sandbox = sandbox_manager
        self.defense_system = defense_system
        self.observer = Observer()
        self.logger = logging.getLogger("BehaviorMonitor")
        self.is_monitoring = False

    def start_monitoring(self):
        """
        Starts the directory monitoring.
        """
        if self.is_monitoring:
            return
        
        target_dir = str(self.sandbox.sandbox_path)
        self.observer.schedule(self, target_dir, recursive=True)
        self.observer.start()
        self.is_monitoring = True
        self.logger.info(f"Started monitoring {target_dir}")

    def stop_monitoring(self):
        """
        Stops the directory monitoring.
        """
        if not self.is_monitoring:
            return
            
        self.observer.stop()
        self.observer.join()
        self.is_monitoring = False
        self.logger.info("Stopped monitoring.")

    def on_modified(self, event):
        if not event.is_directory:
            self.defense_system.record_event("modified", event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.defense_system.record_event("created", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.defense_system.record_event("deleted", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.defense_system.record_event("renamed", event.src_path)
