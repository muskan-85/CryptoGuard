from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, 
    QTextEdit, QPushButton, QFrame, QGridLayout
)
from PySide6.QtCore import QTimer, Qt, Signal, Slot


class DefensePanel(QWidget):
    # Signal to broadcast risk updates across the application
    risk_changed = Signal(float)

    def __init__(self, monitor_engine, defense_system, logger_engine, threat_intel=None):
        super().__init__()
        self.monitor = monitor_engine
        self.defense = defense_system
        self.logger = logger_engine
        self.threat_intel = threat_intel

        # Dark Cybersecurity Palette
        self.setStyleSheet("""
            QWidget {
                background-color: #030712;
                color: #FFFFFF;
                font-family: 'Segoe UI', 'Inter', system-ui, sans-serif;
            }
            QCheckBox {
                background: transparent;
                border: none;
            }
            QCheckBox::indicator {
                width: 36px;
                height: 18px;
                border-radius: 9px;
                background-color: #1E293B;
            }
            QCheckBox::indicator:checked {
                background-color: #10B981;
            }
        """)

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 14, 18, 14)
        main_layout.setSpacing(12)

        # =========================================================================
        # 1. TOP HEADER BAR
        # =========================================================================
        top_header = QHBoxLayout()
        header_title = QLabel("DEFENSE OPERATIONS CENTER")
        header_title.setStyleSheet("font-size: 18px; font-weight: 800; letter-spacing: 1px; color: #FFFFFF;")

        top_right_layout = QHBoxLayout()
        top_right_layout.setSpacing(10)

        doc_status = QLabel("🟢 Real-time Shield Active")
        doc_status.setStyleSheet("""
            color: #10B981;
            font-size: 11px;
            font-weight: 700;
            background: #022C22;
            border: 1px solid #10B981;
            border-radius: 12px;
            padding: 4px 12px;
        """)

        self.intel_btn = QPushButton("📡 Sync Threat Intel Feed")
        self.intel_btn.setStyleSheet("""
            QPushButton {
                background-color: #0B1936;
                color: #00D2FF;
                border: 1px solid #102A5C;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #102A5C;
                color: #FFFFFF;
            }
        """)
        self.intel_btn.clicked.connect(self.check_threat_intel)

        top_right_layout.addWidget(doc_status)
        top_right_layout.addWidget(self.intel_btn)

        top_header.addWidget(header_title)
        top_header.addStretch()
        top_header.addLayout(top_right_layout)
        main_layout.addLayout(top_header)

        # =========================================================================
        # 2. ACTIVE PROTECTION CARDS
        # =========================================================================
        prot_section = QVBoxLayout()
        prot_section.setSpacing(6)

        prot_title = QLabel("ACTIVE PROTECTION")
        prot_title.setStyleSheet("color: #00D2FF; font-size: 11px; font-weight: 800; letter-spacing: 0.8px;")
        prot_section.addWidget(prot_title)

        cards_grid = QGridLayout()
        cards_grid.setHorizontalSpacing(12)

        # Card 1: Monitoring
        card1, self.monitor_chk = self.create_protection_card("🛡️ Real-time File Monitoring", "Active process scanning")
        self.monitor_chk.toggled.connect(self.toggle_monitoring)

        # Card 2: Auto-Restore
        card2, self.restore_chk = self.create_protection_card("🔄 Auto-Restore Engine", "Automated shadow snapshot recovery")
        self.restore_chk.toggled.connect(self.toggle_restore)

        # Card 3: Honeypot Traps
        card3, self.honeypot_chk = self.create_protection_card("🪤 Deploy Honeypot Traps", "Canary file lures active")
        self.honeypot_chk.toggled.connect(self.toggle_honeypots)

        cards_grid.addWidget(card1, 0, 0)
        cards_grid.addWidget(card2, 0, 1)
        cards_grid.addWidget(card3, 0, 2)
        prot_section.addLayout(cards_grid)

        main_layout.addLayout(prot_section)

        # =========================================================================
        # 3. SECURITY LOGS CONSOLE TERMINAL
        # =========================================================================
        logs_frame = QFrame()
        logs_frame.setStyleSheet("""
            QFrame {
                background-color: #020617;
                border: 1px solid #101F42;
                border-radius: 8px;
            }
        """)
        logs_layout = QVBoxLayout(logs_frame)
        logs_layout.setContentsMargins(12, 10, 12, 10)
        logs_layout.setSpacing(6)

        console_bar = QHBoxLayout()
        console_title = QLabel("SECURITY LOGS CONSOLE")
        console_title.setStyleSheet("color: #00D2FF; font-size: 11px; font-weight: 800; letter-spacing: 0.8px; border: none;")
        
        dots_lbl = QLabel("🔴 🟡 🟢")
        dots_lbl.setStyleSheet("border: none; font-size: 9px;")

        console_bar.addWidget(console_title)
        console_bar.addStretch()
        console_bar.addWidget(dots_lbl)
        logs_layout.addLayout(console_bar)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("""
            QTextEdit {
                background-color: #01040D;
                color: #10B981;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                border: 1px solid #0B1936;
                border-radius: 4px;
                padding: 8px;
                line-height: 1.4;
            }
        """)
        logs_layout.addWidget(self.log_view)
        
        main_layout.addWidget(logs_frame, stretch=2)

        # =========================================================================
        # 4. AI ANOMALY ENGINE
        # =========================================================================
        ai_card = QFrame()
        ai_card.setStyleSheet("""
            QFrame {
                background-color: #050B18;
                border: 1px solid #101F42;
                border-radius: 8px;
            }
        """)
        ai_layout = QVBoxLayout(ai_card)
        ai_layout.setContentsMargins(14, 10, 14, 10)
        ai_layout.setSpacing(6)

        ai_header = QLabel("AI ANOMALY ENGINE")
        ai_header.setStyleSheet("color: #00D2FF; font-size: 11px; font-weight: 800; letter-spacing: 0.8px; border: none;")
        
        ai_stats_row = QHBoxLayout()
        
        self.risk_lbl = QLabel("Risk Score: 0%")
        self.risk_lbl.setStyleSheet("color: #10B981; font-size: 14px; font-weight: 800; border: none;")
        
        self.baseline_lbl = QLabel("Baseline: Learning...")
        self.baseline_lbl.setStyleSheet("""
            color: #F59E0B;
            font-size: 11px;
            font-weight: 700;
            background-color: #1C1917;
            border: 1px solid #78350F;
            border-radius: 6px;
            padding: 4px 10px;
        """)

        ai_stats_row.addWidget(self.risk_lbl)
        ai_stats_row.addStretch()
        ai_stats_row.addWidget(self.baseline_lbl)

        ai_layout.addWidget(ai_header)
        ai_layout.addLayout(ai_stats_row)
        main_layout.addWidget(ai_card)

        # =========================================================================
        # 5. FULL-WIDTH ALERT STATUS BANNER
        # =========================================================================
        self.alert_box = QLabel("🛡️  SYSTEM SECURE — ZERO THREATS DETECTED")
        self.alert_box.setAlignment(Qt.AlignCenter)
        self.alert_box.setFixedHeight(38)
        self.alert_box.setStyleSheet("""
            background-color: #10B981;
            color: #01040D;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1px;
            border-radius: 6px;
        """)
        main_layout.addWidget(self.alert_box)

        # Real-time backend timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_logs)
        self.timer.timeout.connect(self.update_ai_stats)
        self.timer.start(1000)

    def create_protection_card(self, title, description):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #050B18;
                border: 1px solid #101F42;
                border-radius: 8px;
            }
            QFrame:hover {
                border: 1px solid #00D2FF;
            }
        """)
        c_layout = QHBoxLayout(card)
        c_layout.setContentsMargins(12, 10, 12, 10)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: 700; border: none;")

        sub_lbl = QLabel(description)
        sub_lbl.setStyleSheet("color: #64748B; font-size: 10px; border: none;")

        info_layout.addWidget(t_lbl)
        info_layout.addWidget(sub_lbl)

        chk = QCheckBox()

        c_layout.addLayout(info_layout)
        c_layout.addStretch()
        c_layout.addWidget(chk)

        return card, chk

    # =========================================================================
    # BACKEND METHODS & GLOBAL SYNCHRONIZATION
    # =========================================================================
    def reset_defense_alarm(self):
        """Forces the defense engine, risk scores, and UI banners to reset to secure baseline."""
        if hasattr(self, 'defense') and self.defense:
            if hasattr(self.defense, 'alarm_triggered'):
                self.defense.alarm_triggered = False
            if hasattr(self.defense, 'risk_score'):
                self.defense.risk_score = 0.0

        self.risk_lbl.setText("Risk Score: 0%")
        self.risk_lbl.setStyleSheet("color: #10B981; font-size: 14px; font-weight: 800; border: none;")
        
        self.alert_box.setText("🛡️  SYSTEM SECURE — ZERO THREATS DETECTED")
        self.alert_box.setStyleSheet("""
            background-color: #10B981; 
            color: #01040D; 
            border-radius: 6px; 
            font-weight: 800; 
            font-size: 12px;
            letter-spacing: 1px;
        """)

        # Force broadcast 0% risk to Dashboard immediately
        self.risk_changed.emit(0.0)

    def append_log(self, text):
        self.log_view.append(text)
        sb = self.log_view.verticalScrollBar()
        sb.setValue(sb.maximum())

    def update_ai_stats(self):
        score_val = 0.0
        
        # 1. Check if alarm is actively triggered on the backend
        is_alarm = getattr(self.defense, 'alarm_triggered', False)
        
        # IF NO ALARM IS ACTIVE, FORCE SCORE TO 0.0
        if not is_alarm:
            if hasattr(self.defense, 'risk_score'):
                self.defense.risk_score = 0.0
            score_val = 0.0
        else:
            score_val = getattr(self.defense, 'risk_score', 0.0)

        pct = int(score_val * 100)
        self.risk_lbl.setText(f"Risk Score: {pct}%")
        
        if is_alarm and score_val > 0.4:
            self.risk_lbl.setStyleSheet("color: #EF4444; font-size: 14px; font-weight: 800; border: none;")
        else:
            self.risk_lbl.setStyleSheet("color: #10B981; font-size: 14px; font-weight: 800; border: none;")

        # Emit signal for interested listeners
        self.risk_changed.emit(score_val)

        # 2. Update Baseline Status
        if hasattr(self.defense, 'baseline_status'):
            status = self.defense.baseline_status
            self.baseline_lbl.setText(f"Baseline: {status}")
            
            if status == "Active":
                self.baseline_lbl.setStyleSheet("""
                    color: #10B981;
                    font-size: 11px;
                    font-weight: 700;
                    background-color: #022C22;
                    border: 1px solid #10B981;
                    border-radius: 6px;
                    padding: 4px 10px;
                """)
            else:
                self.baseline_lbl.setStyleSheet("""
                    color: #F59E0B;
                    font-size: 11px;
                    font-weight: 700;
                    background-color: #1C1917;
                    border: 1px solid #78350F;
                    border-radius: 6px;
                    padding: 4px 10px;
                """)

        # 3. Cross-Tab Dynamic Sync with MainWindow & Dashboard
        main_win = self.window()
        if hasattr(main_win, 'update_global_threat_level'):
            main_win.update_global_threat_level(pct if is_alarm else 0)

    def check_threat_intel(self):
        if self.threat_intel:
            summary = self.threat_intel.get_feed_summary()
            self.append_log(f"[INTEL] Connected to {summary['source']}")
            self.append_log(f"[INTEL] Loaded {summary['total_signatures']} signatures.")
            self.alert_box.setText("📡 THREAT INTELLIGENCE FEED ACTIVE")
            self.alert_box.setStyleSheet("background-color: #0B1936; color: #00D2FF; border: 1px solid #102A5C; border-radius: 6px; font-weight: 800; font-size: 12px;")
        else:
            self.append_log("[INTEL] Threat Intelligence Module skipped")

    def toggle_monitoring(self, checked):
        if checked:
            self.monitor.start_monitoring()
            self.append_log("[SYSTEM] Real-time file monitoring ENABLED")
        else:
            self.monitor.stop_monitoring()
            self.append_log("[SYSTEM] Real-time file monitoring DISABLED")

    def toggle_restore(self, checked):
        self.defense.set_auto_restore(checked)
        status = "ENABLED" if checked else "DISABLED"
        self.append_log(f"[SYSTEM] Auto-Restore engine {status}")

    def toggle_honeypots(self, checked):
        if checked:
            self.defense.enable_honeypots()
            self.append_log("[SYSTEM] Honeypot canary traps DEPLOYED")
        else:
            self.append_log("[SYSTEM] Honeypot deployment cannot be undone in this version.")

    def update_logs(self):
        logs = self.logger.get_logs(10)
        self.log_view.clear()
        for line in logs:
            self.log_view.append(line.strip())
        
        sb = self.log_view.verticalScrollBar()
        sb.setValue(sb.maximum())

        if getattr(self.defense, 'alarm_triggered', False):
            self.alert_box.setText("⚠️ RANSOMWARE ACTIVITY DETECTED!")
            self.alert_box.setStyleSheet("""
                background-color: #EF4444; 
                color: #FFFFFF; 
                border-radius: 6px; 
                font-weight: 800; 
                font-size: 12px;
                letter-spacing: 1px;
            """)
        else:
            self.alert_box.setText("🛡️  SYSTEM SECURE — ZERO THREATS DETECTED")
            self.alert_box.setStyleSheet("""
                background-color: #10B981; 
                color: #01040D; 
                border-radius: 6px; 
                font-weight: 800; 
                font-size: 12px;
                letter-spacing: 1px;
            """)