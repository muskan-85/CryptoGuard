# 🛡️ Security Policy

## 📌 Project Overview

**CryptoGuard: Ransomware Detection and Endpoint Response Prototype** is an **educational cybersecurity sandbox** designed to simulate ransomware attacks and defense strategies in a controlled, non-malicious environment.

This project does **not** contain real malware. All encryption and attack simulations are confined to a local `sandbox` directory.

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

### 📬 How to Report

Please open a GitHub issue or reach out via LinkedIn with the following details:

* Description of the vulnerability
* Steps to reproduce
* Potential impact
* Suggested remediation (if known)
* Screenshots or logs (if applicable)

Please do **NOT** create a public GitHub issue for security vulnerabilities that could be actively exploited.

## ⏳ Response Timeline

| Stage                  | Timeline            |
| ---------------------- | ------------------- |
| Initial acknowledgment | Within 72 hours     |
| Triage & assessment    | Within 7 days       |
| Fix development        | Depends on severity |
| Public disclosure      | After patch release |

## 🔐 Supported Versions

| Version            | Supported |
| ------------------ | --------- |
| Latest main branch | ✅ Yes     |
| Older versions     | ❌ No      |

## ⚠️ Security Scope & Limitations

### What This Project Is:

* A **controlled ransomware simulation**
* An **educational research tool**
* A **local sandbox-only encryption engine**

### What This Project Is NOT:

* Real ransomware
* A penetration testing framework for unauthorized systems
* A production-ready enterprise security solution

## 🧪 Safe Usage Guidelines

1. Always ensure the encryption path points to the internal `/sandbox` directory.
2. Never use generated encryption keys on personal or sensitive data.
3. Do not modify the encryption engine to operate outside the sandbox.
4. Run the application inside a virtual environment.

## 🛑 Prohibited Use

* Using the code or techniques against systems without explicit permission.
* Modifying the project into real malware.
* Deploying any part of this project in production systems.
* Using the encryption engine outside the sandbox environment.

Misuse may violate local and international cybersecurity laws.

## 🧰 Secure Development Practices

* Least privilege (RBAC roles: Admin vs Operator)
* MFA for sensitive operations (TOTP)
* Immutable backup snapshots
* Behavioral anomaly detection
* Local-only file operations
* No network exfiltration capabilities

## 📦 Dependencies

* `cryptography`
* `PySide6`
* `watchdog`
* `matplotlib`
* `pyotp`
* `qrcode`

Check for outdated packages:

```bash
pip list --outdated
```

## 🔍 Security Design Principles

CryptoGuard follows a **Defense-in-Depth** model:

1. Detection (Behavior Monitoring + AI Anomaly Engine)
2. Prevention (MFA, RBAC)
3. Recovery (Immutable Backups)
4. Visibility (Audit Logs & Telemetry)

## 🏛 Legal Disclaimer

This project is intended strictly for educational use, academic research, and cybersecurity awareness training. The author is not responsible for misuse, illegal activities, or damages caused by modifying or deploying this project outside its intended scope.

## 👩‍💻 Author

**Muskan** — BCA Student

[![GitHub](https://img.shields.io/badge/GitHub-muskan--85-181717?logo=github)](https://github.com/muskan-85)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Muskan-0A66C2?logo=linkedin)](https://www.linkedin.com/in/muskan-9b5b99389)

© 2026 Muskan. All rights reserved.