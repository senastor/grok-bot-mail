# Grok Farming

> **⚠️ For Research & Educational Purposes Only**  
> This project is intended for automation research, testing environments, and personal learning. Users must comply with target website terms of service, local laws, and third-party service restrictions. Do not use this project for abuse, platform circumvention, or unauthorized commercial purposes.

Automated x.ai/Grok account registration toolkit with GUI/CLI interfaces, Turnstile solver integration, and multi-mailbox support.

![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Browser: Chromium](https://img.shields.io/badge/Browser-Chromium%2FChrome-4285F4.svg)

---

## Features

- **Browser Automation**: Real Chromium/Chrome automation for registration, CAPTCHA solving, and SSO cookie retrieval
- **Multi-Mailbox Support**:
  - DuckMail
  - YYDS
  - Cloudflare Temp Mail
  - Cloud Mail (unattended mode)
- **GUI + CLI Modes**: Tkinter GUI or headless CLI operation
- **Robust Recovery**: Failed writes automatically saved to `*.pending.jsonl` for idempotent recovery
- **Token Pool Integration**: Optional export to grok2api local/remote pools
- **CPA/OIDC Export**: Optional CLIProxyAPI-compatible xAI OIDC credential export
- **NSFW Toggle**: Attempts to enable NSFW mode post-registration (non-blocking)
- **Batch Progress Tracking**:
  - Successful registrations
  - Failures
  - Pending recoveries
  - Post-processing warnings

---

## How It Works

Single account registration flow:

```text
Open registration page
  → Create temporary mailbox and submit
  → Poll and fill verification code
  → Fill profile details
  → Wait for SSO cookie
  → [Optional] Enable NSFW
  → Save account credentials
  → [Optional] Write to grok2api pool
  → [Optional] Export CPA/OIDC
```

Post-processing (token pooling, CPA export) failures only increment "post-processing warnings" — successfully registered accounts are always saved regardless of optional feature failures.

---

## Requirements

- **Python 3.9+**
- **Google Chrome or Chromium**
- Network access to registration pages and selected mailbox APIs
- **Tkinter** (for GUI mode; CLI mode works without it)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/senastor/grok-farming.git
cd grok-farming
```

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuration

Copy the example config and customize:

```bash
cp config.example.json config.json
```

Edit `config.json` to configure:

- **Mailbox service** (DuckMail, YYDS, Cloudflare, CloudMail)
- **Turnstile solver endpoint** (waguri/captcha-solver at `:8877`)
- **Proxy settings** (if required)
- **grok2api pool paths** (optional)
- **CPA export directory** (optional)

**Important:** Never commit `config.json` — it's in `.gitignore` by default.

---

## Usage

### GUI Mode

```bash
python grok_register_ttk.py
```

Interactive Tkinter interface with real-time batch progress.

### CLI Mode (Headless)

```bash
DISPLAY=:99 python run_headless.py --count 10
```

Register 10 accounts in headless mode (requires Xvfb or virtual display).

### Options

- `--count N`: Number of accounts to register
- `--display :99`: Specify display (for Xvfb)
- `--solver-url http://localhost:8877`: Turnstile solver endpoint

---

## Output & Pending Recovery

- **Successful accounts**: Saved immediately to `accounts_batch_*.txt` (format: `email:password:username`)
- **Pending writes**: Failed file writes → `*.pending.jsonl` (can be recovered later with idempotent replay)
- **Logs**: Detailed logs in terminal/GUI

---

## Project Structure

```
grok-farming/
├── grok_register_ttk.py       # GUI entry point
├── run_headless.py             # CLI entry point
├── registration_flow.py        # Core registration logic
├── registration_browser.py     # Browser automation driver
├── mail_service.py             # Multi-mailbox adapters
├── app_config.py               # Config loader
├── account_outputs.py          # Account persistence
├── cpa_export.py               # CPA/OIDC export
├── requirements.txt            # Python dependencies
├── config.example.json         # Example configuration
└── README.md                   # This file
```

---

## Stability & Safety Mechanisms

- **Browser restart on hang**: Automatic recovery from stuck browser states
- **Mailbox rotation**: Switches mailbox on repeated failures
- **Memory cleanup**: Periodic cleanup to prevent resource exhaustion
- **Safe cancellation**: Graceful shutdown on user interrupt
- **Idempotent recovery**: Pending writes can be replayed without duplicate entries

---

## Troubleshooting

### Turnstile solver not responding
Ensure waguri/captcha-solver is running:
```bash
docker ps | grep captcha-solver
curl http://localhost:8877/health
```

### Browser crashes or hangs
- Check available memory (`free -h`)
- Verify Xvfb is running for headless: `ps aux | grep Xvfb`
- Check Chrome/Chromium installation: `which google-chrome chromium`

### "No verification code received"
- Verify mailbox API credentials in `config.json`
- Check network connectivity to mailbox provider
- Try a different mailbox service

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Contributing

Pull requests welcome! Please ensure:
- Code follows existing style
- No credentials/cookies in commits
- Test with both GUI and CLI modes

---

## Acknowledgments

- [waguri/captcha-solver](https://github.com/waguri/captcha-solver) for Turnstile solving
- [DrissionPage](https://github.com/g1879/DrissionPage) for browser automation (if used)
- Community contributors and testers

---

**⚠️ Reminder**: Use responsibly and in compliance with applicable laws and terms of service.
