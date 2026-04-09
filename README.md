# Security Scripts

A growing collection of cybersecurity scripts built while learning the fundamentals and beyond.

## Projects

### `passwordstrength.py`
A command-line tool that evaluates password strength based on common security criteria.

**Checks:**
- Minimum length (8+ characters)
- Uppercase and lowercase letters
- Numbers
- Special characters

**Output:** Strength rating (Very Weak → Very Strong), improvement suggestions, and a SHA-256 hash of the password.

**Usage:**
```bash
python passwordstrength.py
```

---

### `caesar_cipher.py`
A command-line tool to encrypt and decrypt text using the Caesar cipher.

**Features:**
- Encrypt or decrypt any text with a custom shift (1-25)
- ROT13 encoding/decoding
- Brute-force decode — tries all 25 possible shifts
- Preserves case and non-alphabetic characters

**Usage:**
```bash
python3 caesar_cipher.py
```

---

### `port_scanner.py`
A command-line TCP port scanner with service banner grabbing.

> **Educational use only.**
> Only scan hosts you own or have explicit written permission to scan.
> Scanning systems without authorization may be illegal under the Computer Fraud and Abuse Act (CFAA), the UK Computer Misuse Act, and equivalent laws in other jurisdictions. The author assumes no liability for misuse.

**Features:**
- Scans ports 1-1024 by default (custom range supported)
- Concurrent scanning via thread pool for fast results
- Banner grabbing — connects to each open port and captures the service response
- Service identification — matches port numbers and banner text to known services (SSH, FTP, HTTP, MySQL, etc.)

**Usage:**
```bash
python3 port_scanner.py
```

**Example output:**
```
  PORT     SERVICE          BANNER
  ------- --------------- -----------------------------------
  22       SSH              SSH-2.0-OpenSSH_8.9p1 Ubuntu...
  80       HTTP             HTTP/1.1 200 OK Server: nginx...
```

---

### `LogAnalyzer.py`
A GUI tool for analyzing log files and flagging suspicious security activity.

**Features:**
- Browse and load any `.log` or `.txt` file
- Separates output into **Errors** and **Warnings** sections
- Highlights security-relevant lines (failed logins, SQL injection, XSS attacks, unauthorized access, DDoS, malware, and more) in a distinct color
- Dark-themed scrollable results panel with color-coded severity

**Requirements:**
- Python 3.x (tkinter is included in the standard library)

**Usage:**
```bash
python LogAnalyzer.py
```

---

*More scripts to come as learning progresses.*
