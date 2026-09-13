from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGroupBox, QProgressBar, QFrame, QTextEdit
)
from PySide6.QtCore import Qt, QTimer


class CyberRangePanel(QWidget):
    def __init__(self, cyber_range, net_sim, social_eng):
        super().__init__()
        self.range_mode = cyber_range
        self.net_sim = net_sim
        self.social_eng = social_eng

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

        # Header
        top_header = QHBoxLayout()
        header = QLabel("CYBER RANGE & GAMIFICATION")
        header.setObjectName("Header")
        header.setStyleSheet("font-size: 18px; font-weight: 800; letter-spacing: 1px; color: #FFFFFF;")

        status_badge = QLabel("⚔️ Live Adversary Simulation")
        status_badge.setStyleSheet("""
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
        top_header.addWidget(status_badge)
        main_layout.addLayout(top_header)

        # Scoreboard Section (Red vs Blue)
        score_board = QGroupBox("LIVE SCOREBOARD (RED VS BLUE)")
        sb_layout = QHBoxLayout()
        sb_layout.setContentsMargins(14, 12, 14, 12)
        sb_layout.setSpacing(16)

        # Blue Team Card
        blue_card = QFrame()
        blue_card.setStyleSheet("background: #050B18; border: 1px solid #1E3A8A; border-radius: 8px;")
        bc_layout = QVBoxLayout(blue_card)
        bc_layout.setContentsMargins(16, 10, 16, 10)
        
        blue_sub = QLabel("DEFENSIVE OPERATIONS")
        blue_sub.setStyleSheet("color: #60A5FA; font-size: 9px; font-weight: 800; border: none;")
        self.blue_lbl = QLabel("BLUE TEAM: 0")
        self.blue_lbl.setStyleSheet("color: #38BDF8; font-size: 20px; font-weight: 800; border: none;")
        
        bc_layout.addWidget(blue_sub)
        bc_layout.addWidget(self.blue_lbl)

        # VS Indicator
        self.vs_lbl = QLabel("VS")
        self.vs_lbl.setAlignment(Qt.AlignCenter)
        self.vs_lbl.setStyleSheet("color: #475569; font-size: 16px; font-weight: 900; border: none;")

        # Red Team Card
        red_card = QFrame()
        red_card.setStyleSheet("background: #050B18; border: 1px solid #881337; border-radius: 8px;")
        rc_layout = QVBoxLayout(red_card)
        rc_layout.setContentsMargins(16, 10, 16, 10)
        
        red_sub = QLabel("OFFENSIVE ADVERSARY")
        red_sub.setStyleSheet("color: #F87171; font-size: 9px; font-weight: 800; border: none;")
        self.red_lbl = QLabel("RED TEAM: 0")
        self.red_lbl.setStyleSheet("color: #EF4444; font-size: 20px; font-weight: 800; border: none;")

        rc_layout.addWidget(red_sub)
        rc_layout.addWidget(self.red_lbl)

        sb_layout.addWidget(blue_card, stretch=1)
        sb_layout.addWidget(self.vs_lbl)
        sb_layout.addWidget(red_card, stretch=1)

        score_board.setLayout(sb_layout)
        main_layout.addWidget(score_board)

        # Controls Section
        ctrl_group = QGroupBox("SIMULATION CONTROLS")
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setContentsMargins(14, 12, 14, 12)
        ctrl_layout.setSpacing(12)

        self.start_btn = QPushButton("🚀 Start Range Round (60s)")
        self.start_btn.clicked.connect(self.start_round)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669; 
                color: white; 
                padding: 10px; 
                font-weight: 800;
                font-size: 12px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover { background-color: #10B981; }
            QPushButton:disabled { background-color: #064E3B; color: #6EE7B7; }
        """)

        self.phish_btn = QPushButton("🎣 Test Awareness (Phishing)")
        self.phish_btn.clicked.connect(self.test_phishing)
        self.phish_btn.setStyleSheet("""
            QPushButton {
                background-color: #D97706; 
                color: white; 
                padding: 10px;
                font-weight: 800;
                font-size: 12px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover { background-color: #F59E0B; }
        """)

        ctrl_layout.addWidget(self.start_btn)
        ctrl_layout.addWidget(self.phish_btn)
        ctrl_group.setLayout(ctrl_layout)
        main_layout.addWidget(ctrl_group)

        # Network Traffic Terminal Console View
        net_group = QGroupBox("NETWORK TRAFFIC SIMULATOR")
        net_layout = QVBoxLayout()
        net_layout.setContentsMargins(12, 10, 12, 10)
        net_layout.setSpacing(6)

        c_bar = QHBoxLayout()
        c_title = QLabel("REAL-TIME PACKET FEED")
        c_title.setStyleSheet("color: #00D2FF; font-size: 10px; font-weight: 800; border: none;")
        dots_lbl = QLabel("🔴 🟡 🟢")
        dots_lbl.setStyleSheet("border: none; font-size: 9px;")
        c_bar.addWidget(c_title)
        c_bar.addStretch()
        c_bar.addWidget(dots_lbl)
        net_layout.addLayout(c_bar)

        self.net_log = QTextEdit()
        self.net_log.setReadOnly(True)
        self.net_log.setText("Waiting for traffic...")
        self.net_log.setStyleSheet("""
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
        net_layout.addWidget(self.net_log)
        net_group.setLayout(net_layout)
        main_layout.addWidget(net_group, stretch=1)

        # Round Countdown Status Bar
        timer_frame = QFrame()
        timer_frame.setStyleSheet("""
            QFrame {
                background-color: #050B18;
                border: 1px solid #101F42;
                border-radius: 8px;
            }
        """)
        tf_layout = QHBoxLayout(timer_frame)
        tf_layout.setContentsMargins(14, 10, 14, 10)

        tf_label = QLabel("ROUND TIMER")
        tf_label.setStyleSheet("color: #00D2FF; font-size: 10px; font-weight: 800;")

        self.time_lbl = QLabel("Time Left: 0s")
        self.time_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.time_lbl.setStyleSheet("font-size: 12px; font-weight: 800; color: #FFFFFF;")

        tf_layout.addWidget(tf_label)
        tf_layout.addStretch()
        tf_layout.addWidget(self.time_lbl)
        main_layout.addWidget(timer_frame)

        self.setLayout(main_layout)

        # Update Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_state)
        self.timer.start(500)

    # =========================================================================
    # BACKEND METHODS (Untouched Logic)
    # =========================================================================
    def start_round(self):
        self.range_mode.start_round()
        self.net_sim.start_simulation()
        self.start_btn.setEnabled(False)
        self.start_btn.setText("⏳ Round Active...")
        if isinstance(self.net_log, QTextEdit):
            self.net_log.clear()

    def test_phishing(self):
        failed = self.social_eng.trigger_phishing_attempt(self)
        if failed:
            self.range_mode.update_score("encryption_success", points=50) # Huge penalty
            if isinstance(self.net_log, QTextEdit):
                self.net_log.append("[ALERT] Social Engineering Attempt Succeeded! Red Team +50 pts")
        else:
            self.range_mode.update_score("attack_blocked", points=20) # Bonus
            if isinstance(self.net_log, QTextEdit):
                self.net_log.append("[SUCCESS] User Identified Phishing Trap! Blue Team +20 pts")

    def update_state(self):
        status = self.range_mode.get_status()
        
        # Update Score
        self.red_lbl.setText(f"RED TEAM: {status['red_score']}")
        self.blue_lbl.setText(f"BLUE TEAM: {status['blue_score']}")
        self.time_lbl.setText(f"Time Left: {status['time_left']}s")
        
        # Update Network
        tick = self.net_sim.simulate_tick()
        if tick:
            log_line = f"[{tick['protocol']}] {tick['src']} -> {tick['dst']} ({tick['type']})"
            if isinstance(self.net_log, QTextEdit):
                self.net_log.append(log_line)
                sb = self.net_log.verticalScrollBar()
                sb.setValue(sb.maximum())
            else:
                self.net_log.setText(log_line)
        
        if not status['active'] and not self.start_btn.isEnabled():
            self.start_btn.setEnabled(True)
            self.start_btn.setText("🚀 Start Range Round (60s)")
            self.net_sim.stop_simulation()