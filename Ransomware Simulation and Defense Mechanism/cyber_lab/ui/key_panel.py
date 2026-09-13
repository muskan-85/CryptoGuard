from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QGroupBox, QLineEdit, QListWidget, QMessageBox, QFrame, QGridLayout
)
from PySide6.QtCore import Qt, QTimer

class KeyPanel(QWidget):
    def __init__(self, key_manager, mfa_auth):
        super().__init__()
        self.keys = key_manager
        self.mfa = mfa_auth

        # High-Tech Dark Theme Palette
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
        header = QLabel("ADVANCED KEY MANAGEMENT & IDENTITY")
        header.setObjectName("Header")
        header.setStyleSheet("font-size: 18px; font-weight: 800; letter-spacing: 1px; color: #FFFFFF;")

        key_badge = QLabel("🔑 Cryptographic Vault")
        key_badge.setStyleSheet("""
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
        top_header.addWidget(key_badge)
        main_layout.addLayout(top_header)

        # =========================================================================
        # 2. MAIN TWO-COLUMN LAYOUT
        # =========================================================================
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(14)
        grid_layout.setVerticalSpacing(12)

        # --- LEFT COLUMN: KEY LIFECYCLE ---
        key_group = QGroupBox("ENCRYPTION KEY LIFECYCLE")
        key_layout = QVBoxLayout(key_group)
        key_layout.setContentsMargins(14, 14, 14, 14)
        key_layout.setSpacing(10)

        # Status & Age Telemetry Cards
        status_layout = QHBoxLayout()
        status_layout.setSpacing(10)

        status_card = QFrame()
        status_card.setStyleSheet("background: #050B18; border: 1px solid #101F42; border-radius: 6px;")
        sc_layout = QVBoxLayout(status_card)
        sc_layout.setContentsMargins(10, 8, 10, 8)
        
        sc_tag = QLabel("ACTIVE STATUS")
        sc_tag.setStyleSheet("color: #64748B; font-size: 9px; font-weight: 800; border: none;")
        self.key_status_lbl = QLabel("Status: Checking...")
        self.key_status_lbl.setStyleSheet("font-size: 12px; font-weight: 800; border: none;")
        sc_layout.addWidget(sc_tag)
        sc_layout.addWidget(self.key_status_lbl)

        age_card = QFrame()
        age_card.setStyleSheet("background: #050B18; border: 1px solid #101F42; border-radius: 6px;")
        ac_layout = QVBoxLayout(age_card)
        ac_layout.setContentsMargins(10, 8, 10, 8)
        
        ac_tag = QLabel("KEY AGE")
        ac_tag.setStyleSheet("color: #64748B; font-size: 9px; font-weight: 800; border: none;")
        self.key_age_lbl = QLabel("Age: 0s")
        self.key_age_lbl.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 700; border: none;")
        ac_layout.addWidget(ac_tag)
        ac_layout.addWidget(self.key_age_lbl)

        status_layout.addWidget(status_card, stretch=1)
        status_layout.addWidget(age_card, stretch=1)
        key_layout.addLayout(status_layout)

        # Action Button Row (Right aligned & proportional)
        btn_bar = QHBoxLayout()
        btn_bar.addStretch()
        self.rotate_btn = QPushButton("🔄 Rotate Key (Archive Current)")
        self.rotate_btn.clicked.connect(self.rotate_key)
        self.rotate_btn.setStyleSheet("""
            QPushButton {
                background-color: #D97706; 
                color: white; 
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 800;
                font-size: 11px;
                border: none;
            }
            QPushButton:hover { background-color: #F59E0B; }
            QPushButton:pressed { background-color: #B45309; }
        """)
        btn_bar.addWidget(self.rotate_btn)
        key_layout.addLayout(btn_bar)

        # Archived Keys List View
        arch_lbl = QLabel("ARCHIVED KEYS VAULT")
        arch_lbl.setStyleSheet("color: #00D2FF; font-size: 10px; font-weight: 800; margin-top: 4px;")
        key_layout.addWidget(arch_lbl)

        self.archive_list = QListWidget()
        self.archive_list.setStyleSheet("""
            QListWidget {
                background-color: #01040D;
                color: #38BDF8;
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
                background-color: #0B1936;
                color: #00D2FF;
            }
        """)
        key_layout.addWidget(self.archive_list, stretch=1)
        grid_layout.addWidget(key_group, 0, 0)

        # --- RIGHT COLUMN: MFA AUTHENTICATION ---
        mfa_group = QGroupBox("MULTI-FACTOR AUTHENTICATION (MFA)")
        mfa_layout = QVBoxLayout(mfa_group)
        mfa_layout.setContentsMargins(14, 14, 14, 14)
        mfa_layout.setSpacing(12)

        mfa_top = QHBoxLayout()
        self.mfa_status_lbl = QLabel("MFA Status: DISABLED")
        self.mfa_status_lbl.setStyleSheet("color: #EF4444; font-weight: 800; font-size: 12px;")

        self.enable_mfa_btn = QPushButton("Enable MFA (Simulate)")
        self.enable_mfa_btn.clicked.connect(self.enable_mfa)
        self.enable_mfa_btn.setStyleSheet("""
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
            QPushButton:disabled { background-color: #1E293B; color: #64748B; }
        """)

        mfa_top.addWidget(self.mfa_status_lbl)
        mfa_top.addStretch()
        mfa_top.addWidget(self.enable_mfa_btn)
        mfa_layout.addLayout(mfa_top)

        # Token Card Display
        token_box = QFrame()
        token_box.setStyleSheet("background: #01040D; border: 1px solid #0B1936; border-radius: 6px;")
        tb_layout = QVBoxLayout(token_box)
        tb_layout.setContentsMargins(12, 10, 12, 10)

        t_title = QLabel("CURRENT SIMULATED MFA TOKEN")
        t_title.setStyleSheet("color: #64748B; font-size: 9px; font-weight: 800; border: none;")

        self.token_display = QLabel("Current Token: ---")
        self.token_display.setStyleSheet("font-family: 'Consolas', monospace; font-size: 14px; color: #10B981; font-weight: 700; border: none;")
        
        tb_layout.addWidget(t_title)
        tb_layout.addWidget(self.token_display)
        mfa_layout.addWidget(token_box)

        # MFA Instructions Box
        info_box = QFrame()
        info_box.setStyleSheet("background: #050B18; border: 1px solid #101F42; border-radius: 6px;")
        ib_layout = QVBoxLayout(info_box)
        ib_layout.setContentsMargins(12, 10, 12, 10)
        
        ib_title = QLabel("SECURITY POLICY")
        ib_title.setStyleSheet("color: #00D2FF; font-size: 10px; font-weight: 800;")
        ib_desc = QLabel("Rotating cryptographic keys regularly guarantees forward secrecy. Enabling MFA forces interactive TOTP verification prior to decrypting isolated target vaults.")
        ib_desc.setWordWrap(True)
        ib_desc.setStyleSheet("color: #94A3B8; font-size: 11px; line-height: 1.4;")
        
        ib_layout.addWidget(ib_title)
        ib_layout.addWidget(ib_desc)
        mfa_layout.addWidget(info_box)

        mfa_layout.addStretch()
        grid_layout.addWidget(mfa_group, 0, 1)

        main_layout.addLayout(grid_layout, stretch=1)

        # =========================================================================
        # 3. UNLOCK / DECRYPT TEST BAR (FULL WIDTH BOTTOM)
        # =========================================================================
        test_group = QGroupBox("UNLOCK / DECRYPT TEST")
        test_layout = QHBoxLayout(test_group)
        test_layout.setContentsMargins(14, 12, 14, 12)
        test_layout.setSpacing(12)

        self.mfa_input = QLineEdit()
        self.mfa_input.setPlaceholderText("Enter 6-digit verification code...")
        self.mfa_input.setStyleSheet("""
            QLineEdit {
                background-color: #01040D;
                color: #FFFFFF;
                border: 1px solid #101F42;
                border-radius: 6px;
                padding: 8px 12px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #00D2FF;
            }
        """)

        self.verify_btn = QPushButton("🔓 Verify & Unlock")
        self.verify_btn.clicked.connect(self.verify_code)
        self.verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669; 
                color: white; 
                padding: 8px 20px;
                border-radius: 6px;
                font-weight: 800;
                font-size: 11px;
                border: none;
            }
            QPushButton:hover { background-color: #10B981; }
        """)

        test_layout.addWidget(self.mfa_input, stretch=1)
        test_layout.addWidget(self.verify_btn)
        main_layout.addWidget(test_group)

        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

    # =========================================================================
    # BACKEND METHODS (100% Untouched Logic)
    # =========================================================================
    def update_ui(self):
        status, age = self.keys.get_key_status()
        self.key_status_lbl.setText(f"Status: {status}")
        self.key_age_lbl.setText(f"Age: {age}")
        
        if status == "Expired":
            self.key_status_lbl.setStyleSheet("color: #EF4444; font-size: 12px; font-weight: 800; border: none;")
        else:
            self.key_status_lbl.setStyleSheet("color: #10B981; font-size: 12px; font-weight: 800; border: none;")

        if self.mfa.enabled:
            self.mfa_status_lbl.setText("MFA Status: ENABLED")
            self.mfa_status_lbl.setStyleSheet("color: #10B981; font-weight: 800; font-size: 12px;")
            self.enable_mfa_btn.setEnabled(False)
            
            token = self.mfa.generate_current_token()
            self.token_display.setText(f"Token: {token}")
        
        if self.archive_list.count() == 0: 
            self.refresh_archives()

    def rotate_key(self):
        self.keys.generate_key()
        self.refresh_archives()
        QMessageBox.information(self, "Success", "Key Rotated Successfully!")

    def refresh_archives(self):
        self.archive_list.clear()
        for k in self.keys.list_archived_keys():
            self.archive_list.addItem(k)

    def enable_mfa(self):
        secret = self.mfa.enable_mfa()
        QMessageBox.information(self, "MFA Enabled", f"MFA is now active.\nSecret: {secret}\n\n(See 'Current Token' for codes)")

    def verify_code(self):
        code = self.mfa_input.text()
        if self.mfa.verify_token(code):
            QMessageBox.information(self, "Access Granted", "Identity Verified! Decryption Authenticated.")
        else:
            QMessageBox.warning(self, "Access Denied", "Invalid Token! Access Blocked.")