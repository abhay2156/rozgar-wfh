from pathlib import Path
import runpy

# AIC Cloud starts main.py. Run the actual Streamlit application.
app_path = Path(__file__).with_name("app.py")
if not app_path.is_file():
    raise FileNotFoundError(f"Expected app.py next to main.py: {app_path}")
runpy.run_path(str(app_path), run_name="__main__")
