import json
import logging
import time
from datetime import datetime

class TimelineBuilder:
    """
    Constructs a chronological timeline of the attack chain.
    Used for forensic analysis and reporting.
    """
    def __init__(self):
        self.logger = logging.getLogger("TimelineBuilder")
        self.events = [] # List of dicts: {timestamp, entity, action, details}

    def add_event(self, entity, action, details=""):
        """
        Records an event in the timeline.
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "epoch": time.time(),
            "entity": entity,
            "action": action,
            "details": details
        }
        self.events.append(event)
        # self.logger.debug(f"Event recorded: {entity} - {action}")

    def get_timeline(self):
        return sorted(self.events, key=lambda x: x['epoch'])

    def export_json(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.get_timeline(), f, indent=4)

    def generate_ascii_graph(self):
        """
        Generates a simple ASCII representation of the timeline.
        """
        graph = ["Attack Chain Timeline:", "======================"]
        sorted_events = self.get_timeline()
        
        if not sorted_events:
            return "No events recorded."

        start_time = sorted_events[0]['epoch']
        
        for e in sorted_events:
            delta = e['epoch'] - start_time
            graph.append(f"[+{delta:6.2f}s] [{e['entity']}] {e['action']} -> {e['details']}")
            
        return "\n".join(graph)
