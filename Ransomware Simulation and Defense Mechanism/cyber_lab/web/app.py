import os
import sys
import logging
import subprocess
from pathlib import Path
import webbrowser
from flask import Flask, render_template, jsonify

# Correct Path Setup
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# --------------------------------------------------------------------------
# PRE-LOAD ALL HEAVY IMPORTS AT TOP OF FILE (FASTER BUTTON LAUNCH)
# --------------------------------------------------------------------------
from PySide6.QtWidgets import QApplication
from cyber_lab.core.sandbox_manager import SandboxManager
from cyber_lab.core.encryption_engine import EncryptionEngine
from cyber_lab.core.decryption_engine import DecryptionEngine
from cyber_lab.core.key_manager import KeyManager
from cyber_lab.core.behavior_monitor import BehaviorMonitor
from cyber_lab.core.defense_system import DefenseSystem
from cyber_lab.core.logging_engine import LoggingEngine
from cyber_lab.core.backup_engine import BackupEngine
from cyber_lab.core.file_integrity_checker import FileIntegrityChecker
from cyber_lab.core.process_simulator import ProcessSimulator
from cyber_lab.core.threat_intel_engine import ThreatIntelEngine
from cyber_lab.core.ai_anomaly_engine import AIAnomalyEngine
from cyber_lab.core.baseline_profiler import BaselineProfiler
from cyber_lab.core.zero_trust_engine import ZeroTrustEngine
from cyber_lab.core.timeline_builder import TimelineBuilder
from cyber_lab.core.report_generator import ReportGenerator
from cyber_lab.core.live_metrics import LiveMetrics
from cyber_lab.core.cyber_range_mode import CyberRangeMode
from cyber_lab.core.network_simulator import NetworkSimulator
from cyber_lab.core.social_eng import SocialEngineeringSim
from cyber_lab.core.mfa_auth import MFAAuthenticator
from cyber_lab.core.rbac_engine import RBACEngine
from cyber_lab.core.audit_logger import AuditLogger
from cyber_lab.core.pen_test_sim import PenTestSimulator
from cyber_lab.core.forensics_engine import ForensicsEngine
from cyber_lab.ui.main_window import MainWindow

app = Flask(__name__, template_folder='templates', static_folder='static')

def start_desktop_gui():
    # Initialize Logging
    logger_engine = LoggingEngine()
    
    # Initialize Logic Core
    sandbox = SandboxManager()
    keys = KeyManager()
    encryption = EncryptionEngine(sandbox)
    decryption = DecryptionEngine(sandbox)
    
    backup = BackupEngine(sandbox)
    integrity = FileIntegrityChecker(sandbox)
    simulator = ProcessSimulator(encryption, sandbox)
    threat_intel = ThreatIntelEngine()
    
    ai_engine = AIAnomalyEngine()
    profiler = BaselineProfiler() 
    zero_trust = ZeroTrustEngine()
    timeline = TimelineBuilder()
    metrics = LiveMetrics()
    report_gen = ReportGenerator(sandbox, timeline)

    cyber_range = CyberRangeMode()
    net_sim = NetworkSimulator()
    social_eng = SocialEngineeringSim()
    mfa = MFAAuthenticator()
    rbac = RBACEngine()
    audit = AuditLogger()
    pen_test = PenTestSimulator(sandbox)
    forensics = ForensicsEngine(sandbox, backup)

    audit.log_event("SYSTEM", "STARTUP", "CyberLab started.")

    defense = DefenseSystem(
        sandbox_manager=sandbox, 
        ai_engine=ai_engine, 
        profiler=profiler, 
        zero_trust=zero_trust,
        timeline=timeline,
        metrics=metrics
    )
    monitor = BehaviorMonitor(sandbox, defense)

    core_modules = {
        'sandbox': sandbox, 'keys': keys, 'encryption': encryption,
        'decryption': decryption, 'defense': defense, 'monitor': monitor,
        'logger': logger_engine, 'backup': backup, 'integrity': integrity,
        'simulator': simulator, 'threat_intel': threat_intel, 'ai_engine': ai_engine,
        'profiler': profiler, 'zero_trust': zero_trust, 'timeline': timeline,
        'metrics': metrics, 'report_gen': report_gen, 'cyber_range': cyber_range,
        'net_sim': net_sim, 'social_eng': social_eng, 'mfa': mfa,
        'rbac': rbac, 'audit': audit, 'pen_test': pen_test, 'forensics': forensics
    }

    # Initialize UI
    app_qt = QApplication.instance()
    if not app_qt:
        app_qt = QApplication(sys.argv)
        
    window = MainWindow(core_modules)
    window.show()

    try:
        sys.exit(app_qt.exec())
    except SystemExit:
        monitor.stop_monitoring()


@app.route('/')
def portal():
    return render_template('index.html')


@app.route('/launch', methods=['GET', 'POST'])
def launch():
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT)

        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), '--gui'],
            cwd=str(PROJECT_ROOT),
            env=env
        )
        return jsonify({"status": "ok", "message": "Console launched successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        start_desktop_gui()
    else:
        webbrowser.open("http://127.0.0.1:5000/")
        app.run(host='127.0.0.1', port=5000, debug=False)
