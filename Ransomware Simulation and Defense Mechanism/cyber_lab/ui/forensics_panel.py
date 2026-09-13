from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGroupBox, QListWidget, QTextEdit, QMessageBox, QGridLayout, QFrame
)
from PySide6.QtCore import Qt

class ForensicsPanel(QWidget):
    def __init__(self, pen_test, forensics):
        super().__init__()
        self.pen_test = pen_test
        self.forensics = forensics

        # Global Dark Cybersecurity Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #030712;
                color: #FFFFFF;
                font-family: 'Segoe UI', 'Inter', system-ui, sans-serif;
            }
            QGroupBox {
                border: 1px solid #101F42;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 16px;
                font-size: 11px;
                font-weight: 800;
                color: #00D2FF;
                letter-spacing: 0.8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 6px;
                background-color: #030712;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 14, 18, 14)
        main_layout.setSpacing(12)

        # =========================================================================
        # 1. HEADER BAR
        # =========================================================================
        top_header = QHBoxLayout()
        header = QLabel("FORENSIC LAB & PENETRATION TESTING")
        header.setObjectName("Header")
        header.setStyleSheet("font-size: 18px; font-weight: 800; letter-spacing: 1px; color: #FFFFFF;")

        lab_badge = QLabel("🧪 Interactive Sandbox")
        lab_badge.setStyleSheet("""
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
        top_header.addWidget(lab_badge)
        main_layout.addLayout(top_header)

        # =========================================================================
        # 2. MAIN SPLIT GRID (OFFENSIVE VS DEFENSIVE)
        # =========================================================================
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(14)
        grid_layout.setVerticalSpacing(12)

        # --- LEFT COLUMN: OFFENSIVE PEN-TESTING ---
        pen_group = QGroupBox("PENETRATION TEST SIMULATION (OFFENSIVE)")
        pen_layout = QVBoxLayout(pen_group)
        pen_layout.setContentsMargins(14, 14, 14, 14)
        pen_layout.setSpacing(10)

        # Pen-Test Action Header
        pen_top = QHBoxLayout()
        pen_lbl = QLabel("Vulnerability Assessor")
        pen_lbl.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700;")
        
        self.scan_btn = QPushButton("🔍 Run Vulnerability Scan")
        self.scan_btn.clicked.connect(self.run_scan)
        self.scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563EB; 
                color: white; 
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 800;
                font-size: 11px;
                border: none;
            }
            QPushButton:hover { background-color: #3B82F6; }
        """)

        pen_top.addWidget(pen_lbl)
        pen_top.addStretch()
        pen_top.addWidget(self.scan_btn)
        pen_layout.addLayout(pen_top)

        # Scan Findings List View
        arch_lbl = QLabel("DISCOVERED VULNERABILITIES")
        arch_lbl.setStyleSheet("color: #00D2FF; font-size: 10px; font-weight: 800; margin-top: 4px;")
        pen_layout.addWidget(arch_lbl)

        self.finding_list = QListWidget()
        self.finding_list.setStyleSheet("""
            QListWidget {
                background-color: #01040D;
                color: #F43F5E;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                border: 1px solid #0B1936;
                border-radius: 6px;
                padding: 6px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #0B1936;
            }
            QListWidget::item:selected {
                background-color: #1E1B4B;
                color: #FB7185;
            }
        """)
        pen_layout.addWidget(self.finding_list, stretch=1)

        # Launch Exploit Bar
        exploit_bar = QHBoxLayout()
        exploit_bar.addStretch()
        
        self.exploit_btn = QPushButton("☣️ Launch Simulated Exploit")
        self.exploit_btn.clicked.connect(self.run_exploit)
        self.exploit_btn.setStyleSheet("""
            QPushButton {
                background-color: #E11D48; 
                color: white; 
                padding: 8px 18px;
                border-radius: 6px;
                font-weight: 800;
                font-size: 11px;
                border: none;
            }
            QPushButton:hover { background-color: #F43F5E; }
            QPushButton:pressed { background-color: #BE123C; }
        """)
        exploit_bar.addWidget(self.exploit_btn)
        pen_layout.addLayout(exploit_bar)

        grid_layout.addWidget(pen_group, 0, 0)

        # --- RIGHT COLUMN: DEFENSIVE DIGITAL FORENSICS ---
        for_group = QGroupBox("DIGITAL FORENSICS (DEFENSIVE)")
        for_layout = QVBoxLayout(for_group)
        for_layout.setContentsMargins(14, 14, 14, 14)
        for_layout.setSpacing(10)

        # Forensics Action Header
        for_top = QHBoxLayout()
        for_lbl = QLabel("Memory Artifact Analyzer")
        for_lbl.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 700;")

        self.mem_btn = QPushButton("💾 Capture Memory Artifacts")
        self.mem_btn.clicked.connect(self.capture_mem)
        self.mem_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669; 
                color: white; 
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 800;
                font-size: 11px;
                border: none;
            }
            QPushButton:hover { background-color: #10B981; }
        """)

        for_top.addWidget(for_lbl)
        for_top.addStretch()
        for_top.addWidget(self.mem_btn)
        for_layout.addLayout(for_top)

        # Forensic Terminal Log
        log_lbl = QLabel("FORENSIC DUMP TERMINAL")
        log_lbl.setStyleSheet("color: #00D2FF; font-size: 10px; font-weight: 800; margin-top: 4px;")
        for_layout.addWidget(log_lbl)

        self.forensic_log = QTextEdit()
        self.forensic_log.setReadOnly(True)
        self.forensic_log.setStyleSheet("""
            QTextEdit {
                background-color: #01040D;
                color: #38BDF8;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                border: 1px solid #0B1936;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        for_layout.addWidget(self.forensic_log, stretch=1)

        grid_layout.addWidget(for_group, 0, 1)

        main_layout.addLayout(grid_layout, stretch=1)

    # =========================================================================
    # BACKEND METHODS (100% Untouched Logic)
    # =========================================================================
    def run_scan(self):
        results = self.pen_test.run_scan()
        self.finding_list.clear()
        for f in results['findings']:
            item = f"[{f['severity']}] {f['name']} ({f['id']})"
            self.finding_list.addItem(item)
        
        QMessageBox.information(self, "Scan Complete", f"Scan finished. Found {len(results['findings'])} potential issues.\nThreat Score: {results['threat_score']}")

    def run_exploit(self):
        item = self.finding_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Missing Target", "Please select a finding from the scan results first.")
            return
            
        vuln_id = item.text().split('(')[-1].strip(')')
        success, msg = self.pen_test.simulate_exploit(vuln_id)
        
        if success:
            QMessageBox.critical(self, "EXPLOIT SUCCESS", msg)
        else:
            QMessageBox.information(self, "Attack Blocked", msg)

    def capture_mem(self):
        artifacts = self.forensics.generate_memory_dump()
        self.forensic_log.append(f"\n--- Forensic Dump {artifacts['dump_id']} ---")
        self.forensic_log.append(f"Suspicious Strings: {', '.join(artifacts['suspicious_strings'])}")
        self.forensic_log.append(f"I/O Anomalies: {', '.join(artifacts['io_patterns'])}")
        self.forensic_log.append("Analysis Complete: Key artifacts found in memory.")