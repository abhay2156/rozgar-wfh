import os
import sys
from pathlib import Path

app_path = Path(__file__).with_name("app.py")
if not app_path.is_file():
    raise FileNotFoundError(f"Expected app.py next to main.py: {app_path}")

# AIC Cloud starts this file with Python. Start Streamlit's server for app.py.
port = os.environ.get("PORT", "8501")
os.execv(
    sys.executable,
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.address=0.0.0.0",
        f"--server.port={port}",
        "--server.headless=true",
    ],
)