import os
import json
import webbrowser
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGroupBox, QTextEdit, QFrame, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt, QTimer


class ReportPanel(QWidget):
    def __init__(self, report_generator, metrics_engine):
        super().__init__()
        self.report_gen = report_generator
        self.metrics = metrics_engine
        self.last_generated_path = None
        
        # Dark Cybersecurity Palette Matching Main Interface
        self.setStyleSheet("""
            QWidget {
                background-color: #030712;
                color: #FFFFFF;
                font-family: 'Segoe UI', 'Inter', system-ui, sans-serif;
            }
            QGroupBox {
                border: 1px solid #101F42;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 14px;
                font-size: 11px;
                font-weight: 800;
                color: #00D2FF;
                letter-spacing: 0.8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 4px;
                background-color: #030712;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 14, 18, 14)
        main_layout.setSpacing(12)
        
        # ---------------- 1. HEADER ----------------
        top_header = QHBoxLayout()
        header = QLabel("ENTERPRISE REPORTING & ANALYTICS")
        header.setObjectName("Header")
        header.setStyleSheet("font-size: 18px; font-weight: 800; letter-spacing: 1px; color: #FFFFFF;")
        
        header_badge = QLabel("📊 Real-time Telemetry Engine")
        header_badge.setStyleSheet("""
            color: #00D2FF;
            font-size: 11px;
            font-weight: 700;
            background: #0B1936;
            border: 1px solid #102A5C;
            border-radius: 12px;
            padding: 4px 12px;
        """)

        top_header.addWidget(header)
        top_header.addStretch()
        top_header.addWidget(header_badge)
        main_layout.addLayout(top_header)

        # ---------------- 2. LIVE METRICS DASHBOARD ----------------
        metrics_group = QGroupBox("LIVE SYSTEM TELEMETRY")
        metrics_layout = QHBoxLayout()
        metrics_layout.setContentsMargins(12, 12, 12, 12)
        metrics_layout.setSpacing(12)
        
        self.enc_rate_lbl = self._create_metric_lbl("Encryption Rate: 0.0 file/s")
        self.cpu_lbl = self._create_metric_lbl("CPU Load: 0%")
        self.ram_lbl = self._create_metric_lbl("RAM Usage: 0%")
        self.rto_lbl = self._create_metric_lbl("Est. RTO: N/A")
        
        metrics_layout.addWidget(self.enc_rate_lbl)
        metrics_layout.addWidget(self.cpu_lbl)
        metrics_layout.addWidget(self.ram_lbl)
        metrics_layout.addWidget(self.rto_lbl)
        
        metrics_group.setLayout(metrics_layout)
        main_layout.addWidget(metrics_group)

        # ---------------- 3. ACTIONS & REPORT GENERATION ----------------
        btn_group = QGroupBox("INCIDENT RESPONSE & ACTIONS")
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(12, 10, 12, 10)
        btn_layout.setSpacing(10)
        
        action_subtext = QLabel("Generate and export incident logs in browser (HTML) or structured data (JSON).")
        action_subtext.setStyleSheet("color: #64748B; font-size: 11px; border: none;")

        # Button 1: Generate & Terminal View
        self.gen_report_btn = QPushButton("📄  Generate Forensic Report")
        self.gen_report_btn.clicked.connect(self.generate_report)
        self.gen_report_btn.setStyleSheet("""
            QPushButton {
                background-color: #EF4444; 
                color: white; 
                padding: 8px 14px;
                border-radius: 6px; 
                font-weight: 800;
                font-size: 11px;
                border: none;
            }
            QPushButton:hover { background-color: #DC2626; }
            QPushButton:pressed { background-color: #B91C1C; }
        """)

        # Button 2: Open HTML in Browser
        self.btn_open_html = QPushButton("🌐  Open HTML Report")
        self.btn_open_html.clicked.connect(self.open_html_report)
        self.btn_open_html.setStyleSheet("""
            QPushButton {
                background-color: #0B1936;
                color: #00D2FF;
                border: 1px solid #102A5C;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: 800;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #102A5C;
                color: #FFFFFF;
            }
        """)

        # Button 3: Export JSON Data
        self.btn_export_json = QPushButton("💾  Export JSON Report")
        self.btn_export_json.clicked.connect(self.export_json_report)
        self.btn_export_json.setStyleSheet("""
            QPushButton {
                background-color: #052E16;
                color: #10B981;
                border: 1px solid #059669;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: 800;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #047857;
                color: #FFFFFF;
            }
        """)
        
        btn_layout.addWidget(action_subtext)
        btn_layout.addStretch()
        btn_layout.addWidget(self.gen_report_btn)
        btn_layout.addWidget(self.btn_open_html)
        btn_layout.addWidget(self.btn_export_json)
        
        btn_group.setLayout(btn_layout)
        main_layout.addWidget(btn_group)

        # ---------------- 4. REPORT VIEWER CONSOLE TERMINAL ----------------
        console_frame = QFrame()
        console_frame.setStyleSheet("""
            QFrame {
                background-color: #020617;
                border: 1px solid #101F42;
                border-radius: 8px;
            }
        """)
        console_layout = QVBoxLayout(console_frame)
        console_layout.setContentsMargins(12, 10, 12, 10)
        console_layout.setSpacing(6)

        c_bar = QHBoxLayout()
        c_title = QLabel("FORENSIC AUDIT TERMINAL")
        c_title.setStyleSheet("color: #00D2FF; font-size: 11px; font-weight: 800; letter-spacing: 0.8px; border: none;")
        
        c_dots = QLabel("🔴 🟡 🟢")
        c_dots.setStyleSheet("border: none; font-size: 9px;")

        c_bar.addWidget(c_title)
        c_bar.addStretch()
        c_bar.addWidget(c_dots)
        console_layout.addLayout(c_bar)

        self.report_view = QTextEdit()
        self.report_view.setReadOnly(True)
        self.report_view.setPlaceholderText("Generated reports and event telemetry output will appear here...")
        self.report_view.setStyleSheet("""
            QTextEdit {
                background-color: #01040D;
                color: #38BDF8;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                border: 1px solid #0B1936;
                border-radius: 4px;
                padding: 10px;
                line-height: 1.4;
            }
        """)
        console_layout.addWidget(self.report_view)
        
        main_layout.addWidget(console_frame, stretch=1)

        self.setLayout(main_layout)

        # Telemetry Refresh Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000)

    def _create_metric_lbl(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("""
            QLabel {
                background-color: #050B18; 
                color: #10B981; 
                padding: 12px; 
                border-radius: 6px; 
                font-weight: 800; 
                font-size: 12px;
                border: 1px solid #101F42;
            }
            QLabel:hover {
                border: 1px solid #00D2FF;
            }
        """)
        lbl.setAlignment(Qt.AlignCenter)
        return lbl

    def update_metrics(self):
        if self.metrics:
            try:
                m = self.metrics.get_metrics()
                self.enc_rate_lbl.setText(f"Enc Rate: {m.get('encryption_rate', '0.0 B/s')}")
                self.cpu_lbl.setText(f"CPU: {m.get('cpu', '0%')}")
                self.ram_lbl.setText(f"RAM: {m.get('ram', '0%')}")
                
                total = m.get('files_total', 0)
                if total > 0:
                    self.rto_lbl.setText(f"Impact: {total} files")
                    self.rto_lbl.setStyleSheet("""
                        background-color: #1C1917; color: #EF4444; padding: 12px; 
                        border-radius: 6px; font-weight: 800; font-size: 12px; border: 1px solid #7F1D1D;
                    """)
                else:
                    self.rto_lbl.setText("System Healthy")
                    self.rto_lbl.setStyleSheet("""
                        background-color: #050B18; color: #10B981; padding: 12px; 
                        border-radius: 6px; font-weight: 800; font-size: 12px; border: 1px solid #101F42;
                    """)
            except Exception:
                pass

    # =========================================================================
    # REPORT GENERATION & EXPORT HANDLERS
    # =========================================================================
    def generate_report(self):
        stats = {"encrypted_count": 0, "defense_metrics": {"alerts": 0}}
        if self.metrics and hasattr(self.metrics, 'files_encrypted_total'):
            stats["encrypted_count"] = self.metrics.files_encrypted_total
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_id = f"MANUAL_{timestamp}"
            
            if self.report_gen:
                self.last_generated_path = self.report_gen.generate_report(report_id, stats)
            else:
                self.last_generated_path = os.path.abspath(f"reports/incident_{report_id}.html")

            self.report_view.append(f"[SUCCESS] Forensic Report Generated: {self.last_generated_path}")
            self.report_view.append("-" * 55)
            self.report_view.append("[INFO] Click 'Open HTML Report' to launch it in your browser.")
        except Exception as e:
            self.report_view.append(f"[ERROR] Error generating report: {str(e)}")

    def open_html_report(self):
        """Launches the latest generated HTML report or scans the reports folder for the newest .html file."""
        try:
            target_path = getattr(self, 'last_generated_path', None)

            # If no recent report stored, find the most recently created HTML file in /reports
            if not target_path or not os.path.exists(target_path):
                reports_dir = os.path.abspath("reports")
                if os.path.exists(reports_dir):
                    html_files = [
                        os.path.join(reports_dir, f) for f in os.listdir(reports_dir) 
                        if f.endswith('.html')
                    ]
                    if html_files:
                        target_path = max(html_files, key=os.path.getmtime)

            if target_path and os.path.exists(target_path):
                os.startfile(target_path)
                self.report_view.append(f"[SUCCESS] Opened HTML Report: {target_path}")
            else:
                self.generate_report()
                if hasattr(self, 'last_generated_path') and self.last_generated_path and os.path.exists(self.last_generated_path):
                    os.startfile(self.last_generated_path)
                    self.report_view.append(f"[SUCCESS] Opened newly generated HTML Report: {self.last_generated_path}")
                else:
                    self.report_view.append("[ERROR] Could not find any generated HTML report on disk.")
        except Exception as e:
            self.report_view.append(f"[ERROR] Failed to open HTML report: {str(e)}")

    def export_json_report(self):
        """Compiles system metrics/logs into JSON and opens the reports folder in Explorer."""
        try:
            reports_dir = os.path.abspath("reports")
            os.makedirs(reports_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = os.path.join(reports_dir, f"forensic_audit_{timestamp}.json")
            
            metrics_data = {}
            if self.metrics and hasattr(self.metrics, 'get_metrics'):
                metrics_data = self.metrics.get_metrics()

            audit_payload = {
                "report_metadata": {
                    "title": "CryptoGuard Forensic Audit Log",
                    "generated_at": datetime.now().isoformat(),
                    "environment": "Simulation & EDR Sandbox"
                },
                "system_telemetry": metrics_data,
                "terminal_logs": self.report_view.toPlainText().split("\n")
            }

            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(audit_payload, f, indent=4)

            self.report_view.append(f"[SUCCESS] JSON Report exported to: {json_filename}")
            
            # Automatically open the reports folder in Windows File Explorer
            os.startfile(reports_dir)
            self.report_view.append("[INFO] Opened reports folder in File Explorer.")
        except Exception as e:
            self.report_view.append(f"[ERROR] Failed to export JSON report: {str(e)}")