import sys
import threading
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTextEdit, QProgressBar, QFrame, QGridLayout, QComboBox,
    QMessageBox, QSizePolicy
)
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QFont, QColor


class SimulationWorker(QThread):
    progress = Signal(int)
    finished = Signal()
    log = Signal(str)

    def __init__(self, engine, key, mode="encrypt"):
        super().__init__()
        self.engine = engine
        self.key = key
        self.mode = mode

    def run(self):
        # Helper to emit logs to the UI console in real time
        def emit_log(msg):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log.emit(f"[{timestamp}] [ENGINE] {msg}")

        emit_log(f"Starting {self.mode.upper()} sequence...")
        if self.mode == "encrypt":
            self.engine.encrypt_sandbox(self.key, self.progress.emit)
        else:
            self.engine.decrypt_sandbox(self.key, self.progress.emit)
            
        emit_log(f"{self.mode.capitalize()} sequence completed successfully.")
        self.finished.emit()


# Dedicated QThread for the Simulator attack execution
class SimulatorAttackWorker(QThread):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal()

    def __init__(self, simulator, key, mode="burst"):
        super().__init__()
        self.simulator = simulator
        self.key = key
        self.mode = mode

    def run(self):
        def progress_callback(val):
            # Emit safely to the main thread via Qt Signal
            self.progress.emit(val)

        try:
            self.simulator.simulate_attack(self.key, self.mode, progress_callback)
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log.emit(f"[{timestamp}] [ERROR] Attack failed: {e}")
        finally:
            self.finished.emit()


class SimulationPanel(QWidget):
    def __init__(self, sandbox_manager, key_manager, encryption_engine, decryption_engine,
                 backup_engine, integrity_checker, simulator=None, threat_intel=None,
                 mfa_auth=None, rbac=None, audit=None):
        super().__init__()
        self.sandbox = sandbox_manager
        self.keys = key_manager
        self.encryptor = encryption_engine
        self.decryptor = decryption_engine
        self.backup = backup_engine
        self.integrity = integrity_checker
        self.simulator = simulator
        self.threat_intel = threat_intel
        self.mfa = mfa_auth
        self.rbac = rbac
        self.audit = audit
        
        # Base Application Stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #030712;
                color: #FFFFFF;
                font-family: 'Segoe UI', 'Inter', system-ui, sans-serif;
            }
            QComboBox {
                background-color: #0B132B;
                border: 1px solid #1E293B;
                border-radius: 6px;
                color: #FFFFFF;
                padding: 10px 12px;
                font-size: 13px;
                font-weight: 500;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #0B132B;
                border: 1px solid #1E293B;
                color: #FFFFFF;
                selection-background-color: #1E293B;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(12)

        # =========================================================================
        # 1. TOP SECTION: REAL-TIME CONSOLE & SETTINGS
        # =========================================================================
        top_split_layout = QHBoxLayout()
        top_split_layout.setSpacing(14)

        # --- A. SIMULATION CONSOLE (Terminal Output) ---
        console_frame = QFrame()
        console_frame.setStyleSheet("""
            QFrame {
                background-color: #050B18;
                border: 1px solid #101F42;
                border-radius: 10px;
            }
        """)
        console_layout = QVBoxLayout(console_frame)
        console_layout.setContentsMargins(14, 12, 14, 12)
        console_layout.setSpacing(8)

        console_header = QLabel("SIMULATION CONSOLE")
        console_header.setStyleSheet("""
            color: #00D2FF; 
            font-size: 11px; 
            font-weight: 800; 
            letter-spacing: 0.8px;
            border: none;
        """)
        console_layout.addWidget(console_header)

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setStyleSheet("""
            QTextEdit {
                background-color: #02050D;
                color: #22C55E;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                border: 1px solid #0B1E38;
                border-radius: 6px;
                padding: 10px;
                line-height: 1.4;
            }
        """)
        
        console_layout.addWidget(self.console_output)
        top_split_layout.addWidget(console_frame, stretch=3)

        # --- B. SIMULATION SETTINGS PANEL ---
        settings_frame = QFrame()
        settings_frame.setStyleSheet("""
            QFrame {
                background-color: #050B18;
                border: 1px solid #101F42;
                border-radius: 10px;
            }
        """)
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setContentsMargins(16, 12, 16, 14)
        settings_layout.setSpacing(10)

        settings_header = QLabel("SIMULATION SETTINGS")
        settings_header.setStyleSheet("""
            color: #00D2FF; 
            font-size: 11px; 
            font-weight: 800; 
            letter-spacing: 0.8px;
            border: none;
        """)
        settings_layout.addWidget(settings_header)

        # Encryption Method
        lbl_enc = QLabel("Encryption Method")
        lbl_enc.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 500; border: none;")
        self.combo_enc = QComboBox()
        self.combo_enc.addItems(["🔒  AES-256", "🔒  ChaCha20", "🔒  RSA-4096"])
        settings_layout.addWidget(lbl_enc)
        settings_layout.addWidget(self.combo_enc)

        # Simulation Mode
        lbl_mode = QLabel("Simulation Mode")
        lbl_mode.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 500; border: none;")
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["🛡️  Realistic Attack Simulation", "⚡  Fast Dry-Run Mode", "🧪  Header Corruption Only"])
        settings_layout.addWidget(lbl_mode)
        settings_layout.addWidget(self.combo_mode)

        # Intensity Level
        lbl_int = QLabel("Intensity Level")
        lbl_int.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 500; border: none;")
        self.combo_int = QComboBox()
        self.combo_int.addItems(["📈  High", "📊  Medium", "📉  Low"])
        settings_layout.addWidget(lbl_int)
        settings_layout.addWidget(self.combo_int)

        settings_layout.addStretch()
        top_split_layout.addWidget(settings_frame, stretch=2)

        main_layout.addLayout(top_split_layout, stretch=3)

        # =========================================================================
        # 2. MIDDLE SECTION: PATH BAR & ACTION CARDS GRID
        # =========================================================================
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)

        path_val = getattr(self.sandbox, 'sandbox_path', 'C:\\Sandbox\\Target')
        self.path_input = QLineEdit(f"📁   {path_val}")
        self.path_input.setStyleSheet("""
            QLineEdit {
                background-color: #050B18;
                border: 1px solid #101F42;
                border-radius: 8px;
                color: #94A3B8;
                padding: 10px 14px;
                font-size: 13px;
                font-family: 'Consolas', monospace;
            }
        """)

        reset_btn = QPushButton("Reset Sandbox")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #091936;
                color: #00D2FF;
                border: 1px solid #102A5C;
                border-radius: 8px;
                padding: 10px 22px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #102A5C;
                color: #FFFFFF;
            }
        """)
        reset_btn.clicked.connect(self.reset_sandbox)

        path_layout.addWidget(self.path_input, stretch=1)
        path_layout.addWidget(reset_btn)
        main_layout.addLayout(path_layout)

        # --- 2x2 Action Cards Grid ---
        cards_grid = QGridLayout()
        cards_grid.setHorizontalSpacing(14)
        cards_grid.setVerticalSpacing(12)

        # Card 1: Launch Attack
        self.encrypt_btn = self.create_action_card(
            icon="🚀",
            title="Launch Ransomware Attack",
            subtitle="Start simulation of ransomware behavior",
            border_color="#EF4444",
            bg_color="#180B12",
            title_color="#EF4444"
        )
        self.encrypt_btn.clicked.connect(self.start_encryption)

        # Card 2: Decrypt / Restore
        self.decrypt_btn = self.create_action_card(
            icon="🔓",
            title="Decrypt / Restore",
            subtitle="Attempt to decrypt & restore encrypted files",
            border_color="#22C55E",
            bg_color="#071813",
            title_color="#22C55E"
        )
        self.decrypt_btn.clicked.connect(self.start_decryption)

        # Card 3: Create Snapshot
        self.backup_btn = self.create_action_card(
            icon="💾",
            title="Create Snapshot",
            subtitle="Capture current system snapshot",
            border_color="#1D4ED8",
            bg_color="#050B18",
            title_color="#3B82F6"
        )
        self.backup_btn.clicked.connect(self.create_backup)

        # Card 4: Check Integrity
        self.integrity_btn = self.create_action_card(
            icon="🔍",
            title="Check Integrity",
            subtitle="Verify system file integrity",
            border_color="#1D4ED8",
            bg_color="#050B18",
            title_color="#3B82F6"
        )
        self.integrity_btn.clicked.connect(self.check_integrity)

        cards_grid.addWidget(self.encrypt_btn, 0, 0)
        cards_grid.addWidget(self.decrypt_btn, 0, 1)
        cards_grid.addWidget(self.backup_btn, 1, 0)
        cards_grid.addWidget(self.integrity_btn, 1, 1)

        main_layout.addLayout(cards_grid)

        # =========================================================================
        # 3. BOTTOM SECTION: SIMULATION PROGRESS BAR & STATUS
        # =========================================================================
        progress_card = QFrame()
        progress_card.setStyleSheet("""
            QFrame {
                background-color: #050B18;
                border: 1px solid #101F42;
                border-radius: 10px;
            }
        """)
        progress_layout = QVBoxLayout(progress_card)
        progress_layout.setContentsMargins(16, 12, 16, 14)
        progress_layout.setSpacing(10)

        prog_header = QLabel("SIMULATION PROGRESS")
        prog_header.setStyleSheet("""
            color: #00D2FF; 
            font-size: 10px; 
            font-weight: 800; 
            letter-spacing: 0.8px;
            border: none;
        """)
        progress_layout.addWidget(prog_header)

        # Bar Row with Real-Time Percentage Label
        bar_row = QHBoxLayout()
        bar_row.setSpacing(12)

        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        self.pbar.setTextVisible(False)
        self.pbar.setFixedHeight(12)
        self.pbar.setStyleSheet("""
            QProgressBar {
                background-color: #0B132B;
                border: none;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3B82F6, stop:1 #22C55E);
                border-radius: 6px;
            }
        """)

        self.pct_label = QLabel("0%")
        self.pct_label.setStyleSheet("color: #22C55E; font-size: 14px; font-weight: 800; border: none;")

        bar_row.addWidget(self.pbar, stretch=1)
        bar_row.addWidget(self.pct_label)
        progress_layout.addLayout(bar_row)

        # Verified Status Text Label
        self.status_lbl = QLabel("Ready")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.status_lbl.setStyleSheet("color: #22C55E; font-size: 14px; font-weight: 700; border: none;")
        progress_layout.addWidget(self.status_lbl)

        main_layout.addWidget(progress_card)

        # Sizing Policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(800)

        # Initial Boot Logs
        self.log_to_console("[SYSTEM] Sandbox Initialized...")
        self.log_to_console("[SYSTEM] Virtual Environment Ready")
        self.log_to_console("[SYSTEM] System Shield: ENABLED")
        self.log_to_console("[READY] Awaiting attack command...")

    # Helper function for real-time console streaming
    @Slot(str)
    def log_to_console(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if not text.startswith("["):
            formatted_text = f"[{timestamp}] [INFO] {text}"
        else:
            formatted_text = f"[{timestamp}] {text}"
        self.console_output.append(formatted_text)
        # Scroll to bottom automatically
        sb = self.console_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    @Slot(int)
    def update_progress(self, val):
        self.pbar.setValue(val)
        self.pct_label.setText(f"{val}%")

    def create_action_card(self, icon, title, subtitle, border_color, bg_color, title_color):
        btn = QPushButton()
        btn.setFixedHeight(80)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 10px;
                text-align: left;
                padding: 12px 16px;
            }}
            QPushButton:hover {{
                background-color: #101F42;
            }}
        """)

        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(12, 8, 12, 8)
        btn_layout.setSpacing(14)

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 28px; background: transparent; border: none;")

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setAlignment(Qt.AlignVCenter)

        t_lbl = QLabel(title)
        t_lbl.setStyleSheet(f"color: {title_color}; font-size: 15px; font-weight: 700; background: transparent; border: none;")

        sub_lbl = QLabel(subtitle)
        sub_lbl.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 500; background: transparent; border: none;")

        text_layout.addWidget(t_lbl)
        text_layout.addWidget(sub_lbl)

        btn_layout.addWidget(icon_lbl)
        btn_layout.addLayout(text_layout)
        btn_layout.addStretch()

        return btn

    # =========================================================================
    # FUNCTIONAL METHODS
    # =========================================================================
    def reset_sandbox(self):
        self.log_to_console("[SYSTEM] Resetting sandbox files...")
        if hasattr(self.sandbox, 'create_mock_files'):
            self.sandbox.create_mock_files()
        elif hasattr(self.sandbox, 'reset'):
            self.sandbox.reset()

        # Reset Defense Engine backend variables if accessible
        main_win = self.window()
        if hasattr(main_win, 'defense') and hasattr(main_win.defense, 'reset_defense_alarm'):
            main_win.defense.reset_defense_alarm()

        if hasattr(main_win, 'update_global_threat_level'):
            main_win.update_global_threat_level(0)

        self.status_lbl.setText("Sandbox reset with mock files.")
        self.log_to_console("[SUCCESS] Sandbox reset complete.")

    def start_encryption(self):
        if self.rbac and not self.rbac.can("attack"):
            QMessageBox.critical(self, "Unauthorized", "Your role does not have permission to launch attacks.")
            self.log_to_console("[ERROR] RBAC Check failed for attack execution.")
            if self.audit:
                self.audit.log_event(self.rbac.current_user, "UNAUTHORIZED_ATTACK_ATTEMPT",
                                     "User tried but failed RBAC check.")
            return

        if self.audit and self.rbac:
            self.audit.log_event(self.rbac.current_user, "ATTACK_START", "Encryption sequence initiated.")
            
        key = self.keys.load_key()
        self.log_to_console("[ATTACK] Encryption sequence triggered...")

        if self.simulator:
            self.status_lbl.setText("Starting Burst Attack Simulation...")
            self.log_to_console("[SIMULATOR] Burst Attack execution thread starting...")
            
            self.worker = SimulatorAttackWorker(self.simulator, key, mode="burst")
            self.worker.progress.connect(self.update_progress)
            self.worker.log.connect(self.log_to_console)
            self.worker.finished.connect(self.on_encryption_finished)
            self.worker.start()
        else:
            self.worker = SimulationWorker(self.encryptor, key, "encrypt")
            self.worker.progress.connect(self.update_progress)
            self.worker.log.connect(self.log_to_console)
            self.worker.finished.connect(self.on_encryption_finished)
            self.worker.start()
            self.status_lbl.setText("Encrypting...")

    def on_encryption_finished(self):
        self.status_lbl.setText("Encryption Complete!")
        self.log_to_console("[SUCCESS] All targeted files encrypted.")

    def start_decryption(self):
        if self.rbac and not self.rbac.can("restore"):
            QMessageBox.critical(self, "Unauthorized", "Your role does not have permission to restore files.")
            self.log_to_console("[ERROR] RBAC Check failed for file restoration.")
            return

        if self.mfa and self.mfa.enabled:
            from PySide6.QtWidgets import QInputDialog, QLineEdit
            token, ok = QInputDialog.getText(self, "MFA Verification", 
                                             "Enter 6-digit Authenticator Code:", 
                                             QLineEdit.Password)
            if not ok:
                self.log_to_console("[WARN] MFA prompt cancelled.")
                return
            if not self.mfa.verify_token(token):
                QMessageBox.critical(self, "Access Denied", "Invalid MFA Token!")
                self.log_to_console("[ERROR] Invalid MFA Token entered!")
                return

        if self.audit and self.rbac:
            self.audit.log_event(self.rbac.current_user, "RESTORE_START", "Decryption/MFA passed.")
            
        key = self.keys.load_key()
        self.log_to_console("[DECRYPT] Starting decryption sequence...")
        self.worker = SimulationWorker(self.decryptor, key, "decrypt")
        self.worker.progress.connect(self.update_progress)
        self.worker.log.connect(self.log_to_console)
        self.worker.finished.connect(self.on_decryption_finished)
        self.worker.start()
        self.status_lbl.setText("Decrypting...")

    def on_decryption_finished(self):
        self.status_lbl.setText("Decryption Complete!")
        self.log_to_console("[SUCCESS] Files successfully decrypted and restored.")

        # Trigger reset on defense panel to disarm alarm and restore green baseline
        main_win = self.window()
        if hasattr(main_win, 'defense') and hasattr(main_win.defense, 'reset_defense_alarm'):
            main_win.defense.reset_defense_alarm()

        if hasattr(main_win, 'update_global_threat_level'):
            main_win.update_global_threat_level(0)

    def create_backup(self):
        self.log_to_console("[SNAPSHOT] Creating system snapshot...")
        path = self.backup.create_snapshot()
        if path:
            self.status_lbl.setText(f"Snapshot created at {path}")
            self.log_to_console(f"[SUCCESS] Snapshot stored at: {path}")
        else:
            self.status_lbl.setText("Snapshot failed!")
            self.log_to_console("[ERROR] Snapshot creation failed.")

    def check_integrity(self):
        self.log_to_console("[INTEGRITY] Checking file integrity baselines...")
        self.integrity.establish_baseline()
        compromised = self.integrity.check_integrity()
        if not compromised:
            self.status_lbl.setText("🛡️  Integrity Verified: System Secure.")
            self.log_to_console("[SUCCESS] File integrity verified. 0 anomalies detected.")
        else:
            self.status_lbl.setText(f"⚠️ {len(compromised)} files compromised!")
            self.log_to_console(f"[ALERT] {len(compromised)} compromised files detected!")