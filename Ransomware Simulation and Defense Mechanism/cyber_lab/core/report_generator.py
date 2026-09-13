import json
import logging
from datetime import datetime
from pathlib import Path

class ReportGenerator:
    """
    Generates incident reports in JSON and HTML formats.
    """
    def __init__(self, sandbox_manager, timeline_builder=None):
        self.sandbox = sandbox_manager
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        self.timeline = timeline_builder
        self.logger = logging.getLogger("ReportGenerator")

    def generate_report(self, incident_id, stats):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_data = {
            "incident_id": incident_id,
            "timestamp": timestamp,
            "sandbox_path": str(self.sandbox.sandbox_path),
            "affected_files_count": stats.get('encrypted_count', 0),
            "defense_metrics": stats.get('defense_metrics', {}),
            "status": "CONTAINED"
        }

        if self.timeline:
            report_data["attack_timeline"] = self.timeline.get_timeline()

        # Save JSON
        json_path = self.reports_dir / f"incident_{incident_id}.json"
        with open(json_path, "w") as f:
            json.dump(report_data, f, indent=4)
            
        # Save HTML
        html_path = self.reports_dir / f"incident_{incident_id}.html"
        self._generate_html(html_path, report_data)
        
        self.logger.info(f"Report generated: {html_path}")
        return str(html_path)

    def _generate_html(self, filepath, data):
        timeline_html = ""
        if "attack_timeline" in data:
            for event in data["attack_timeline"]:
                timeline_html += f"""
                <div class='event'>
                    <span class='time'>{event['timestamp']}</span>
                    <span class='entity'>[{event['entity']}]</span>
                    <span class='action'>{event['action']}</span>
                    <span class='details'>{event['details']}</span>
                </div>
                """

        defense_html = ""
        if data.get('defense_metrics'):
             defense_html = f"<pre>{json.dumps(data['defense_metrics'], indent=2)}</pre>"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Incident Report {data['incident_id']}</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a1a; color: #e0e0e0; padding: 20px; }}
                h1 {{ color: #e94560; border-bottom: 2px solid #e94560; padding-bottom: 10px; }}
                h2 {{ color: #4ecca3; margin-top: 20px; }}
                .metric-box {{ background: #16213e; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .event {{ border-left: 3px solid #0f3460; margin: 10px 0; padding: 10px; background: #222; }}
                .time {{ color: #888; font-size: 0.9em; margin-right: 15px; }}
                .entity {{ color: #4ecca3; font-weight: bold; margin-right: 10px; }}
                .action {{ color: #e94560; font-weight: bold; margin-right: 10px; }}
                .details {{ color: #ccc; }}
            </style>
        </head>
        <body>
            <h1>⚠️ CyberLab Incident Report</h1>
            <div class='metric-box'>
                <p><strong>ID:</strong> {data['incident_id']}</p>
                <p><strong>Time:</strong> {data['timestamp']}</p>
                <p><strong>Files Affected:</strong> {data['affected_files_count']}</p>
                <p><strong>Status:</strong> {data['status']}</p>
            </div>
            
            <h2>🛡️ Defense Metrics</h2>
            <div class='metric-box'>
                {defense_html}
            </div>

            <h2>⏱️ Attack Timeline</h2>
            {timeline_html}
        </body>
        </html>
        """
        
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(html_content)
