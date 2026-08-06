#!/usr/bin/env python3
"""Headless test runner untuk grok-register - bypass GUI, run registration langsung."""
import sys
import os
import time

# Setup display & path
os.environ['DISPLAY'] = ':99'
sys.path.insert(0, '/root/grok-register')
os.chdir('/root/grok-register')

# Load module to bind all globals (config, mail_service, browser_runtime, etc)
print("[*] Loading grok_register_ttk module...")
import grok_register_ttk
from app_config import load_config, validate_run_requirements

# CLI args: --count N (default: config.json register_count)
import argparse
_parser = argparse.ArgumentParser(description="Grok headless register batch")
_parser.add_argument("--count", type=int, default=None, help="Jumlah akun (default: config.json register_count)")
_parser.add_argument("--output", type=str, default=None, help="File output akun (default: accounts_headless_test.txt)")
_args, _ = _parser.parse_known_args()

# Force load config from file
print("[*] Loading config from config.json...")
loaded = load_config()
print(f"[*] Loaded email_provider: {loaded.get('email_provider')}")
print(f"[*] Loaded auth_mode: {loaded.get('cloudflare_auth_mode')}")

# Validate
try:
    validated = validate_run_requirements(loaded)
    grok_register_ttk.config.clear()
    grok_register_ttk.config.update(validated)
    print(f"[*] Config validated & applied to grok_register_ttk.config")
except Exception as e:
    print(f"[!] Validation failed: {e}")
    sys.exit(1)

# Verify config loaded
print(f"[*] email_provider: {grok_register_ttk.config.get('email_provider')}")
print(f"[*] api_base: {grok_register_ttk.config.get('cloudflare_api_base')[:30]}...")
print(f"[*] auth_mode: {grok_register_ttk.config.get('cloudflare_auth_mode')}")
print(f"[*] register_count: {grok_register_ttk.config.get('register_count')}")

# Resolve count & output from CLI args
_run_count = _args.count if _args.count is not None else int(grok_register_ttk.config.get('register_count', 1))
if _args.output:
    accounts_output_file = _args.output
else:
    accounts_output_file = '/root/grok-register/accounts_headless_test.txt'

# Setup callback & cancel
class CancelController:
    def __init__(self):
        self.stop = False
    def __call__(self):
        return self.stop

cancel = CancelController()

# Setup log file
log_file_path = f'/tmp/grok_headless_{int(time.time())}.log'
log_lines = []

def log_callback(msg):
    ts = time.strftime('%H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    log_lines.append(line)
    with open(log_file_path, 'a') as f:
        f.write(line + '\n')

# Observer
def observer(batch, account, output):
    if account is not None:
        log_callback(f"[OBSERVER] ✅ Registered: {account.email}")

print(f"\n[*] Starting registration run...")
print(f"[*] Log file: {log_file_path}")
print(f"[*] Accounts file: {accounts_output_file}")
print(f"[*] Count: {_run_count}\n")

try:
    batch = grok_register_ttk.run_registration_common(
        count=_run_count,
        log_callback=log_callback,
        cancel_callback=cancel,
        accounts_output_file=accounts_output_file,
        observer=observer,
    )

    print(f"\n=== BATCH RESULT ===")
    print(f"Success: {batch.success_count}")
    print(f"Fail: {batch.fail_count}")
    print(f"Registered unsaved: {batch.registered_unsaved_count}")
    print(f"Postprocess warnings: {batch.postprocess_warning_count}")
    print(f"Results: {len(batch.results)}")
    for r in batch.results:
        print(f"  - {r}")

except Exception as e:
    print(f"\n[!] Fatal error: {e}")
    import traceback
    traceback.print_exc()
finally:
    print(f"\n[*] Full log: {log_file_path}")
    if os.path.exists(accounts_output_file):
        print(f"[*] Accounts: {accounts_output_file}")
        with open(accounts_output_file) as f:
            print(f.read())
