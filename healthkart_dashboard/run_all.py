#!/usr/bin/env python3
"""
run_all.py
Starts in one click:
  - lightweight HTTP server on :8000 (serves landing page / static assets)
  - Streamlit app          on :8503 (dashboard.py inside  src/ )
Dependencies:
  pip install streamlit requests cryptography
"""

import atexit
import os
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from contextlib import closing

import http.server
import socketserver

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime

# ------------------------------------------------------------------
# Ports
# ------------------------------------------------------------------
STATIC_SERVER_PORT = 8000
STREAMLIT_PORT = 8502

# ------------------------------------------------------------------
# Generate self-signed certificate (optional, kept for completeness)
# ------------------------------------------------------------------
CERT_PATH = "localhost.crt"
KEY_PATH = "localhost.key"


def generate_self_signed_cert(cert_path: str, key_path: str) -> None:
    """Generate PEM files only if they do not already exist."""
    if os.path.isfile(cert_path) and os.path.isfile(key_path):
        return  # already generated once

    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=365))
        .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False)
        .sign(key, hashes.SHA256(), default_backend())
    )

    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


# ------------------------------------------------------------------
# Static file server (plain HTTP)
# ------------------------------------------------------------------
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # suppress clutter inside the main console
        pass


def run_static_server(port: int = STATIC_SERVER_PORT) -> None:
    """Serve files from the directory where this script lives."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", port), QuietHandler) as httpd:
        print(f"Static server running at http://localhost:{port}")
        httpd.serve_forever()


# ------------------------------------------------------------------
# Streamlit helper
# ------------------------------------------------------------------
def run_streamlit() -> subprocess.Popen:
    streamlit_script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "src", "dashboard.py"
    )

    if not os.path.isfile(streamlit_script_path):
        sys.exit(f"ERROR: Streamlit script not found at {streamlit_script_path}")

    cmd = [
        sys.executable, "-m", "streamlit", "run", streamlit_script_path,
        "--server.port", str(STREAMLIT_PORT),
        "--server.headless", "true",
    ]
    proc = subprocess.Popen(cmd)
    return proc


# ------------------------------------------------------------------
# TCP port wait helpers
# ------------------------------------------------------------------
def wait_for_port(host: str, port: int, timeout: int = 60) -> bool:
    """Poll until given TCP port starts accepting connections."""
    started = time.time()
    while True:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                return True
        if time.time() - started > timeout:
            return False
        time.sleep(1)


# ------------------------------------------------------------------
# Main orchestration
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("HealthKart Dashboard – starting all services…\n")

    # 1. Create self-signed certificate (harmless, can be removed if unused)
    generate_self_signed_cert(CERT_PATH, KEY_PATH)

    # 2. Launch Streamlit (the slowest service) first
    streamlit_proc = run_streamlit()
    atexit.register(lambda p=streamlit_proc: p.terminate())  # auto-cleanup on CTRL-C

    print("Waiting for Streamlit to become ready …")
    ok = wait_for_port("localhost", STREAMLIT_PORT, timeout=120)
    if not ok:
        streamlit_proc.terminate()
        sys.exit("ERROR: Streamlit did not start within 120 s. Aborting.")

    print(f"Streamlit is up on http://localhost:{STREAMLIT_PORT}\n")

    # 3. Fire up the light-weight static server in a daemon thread
    static_t = threading.Thread(
        target=run_static_server,
        daemon=True,
        name="StaticServerThread",
    )
    static_t.start()

    time.sleep(0.5)  # tiny pause to be sure the thread grabbed the port
    print("Static server started.\n")

    # 4. Open browser to the landing page
    webbrowser.open(f"http://localhost:{STATIC_SERVER_PORT}")

    # 5. Stay alive; subprocesses are cleaned by atexit
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nReceived interrupt – shutting down…")