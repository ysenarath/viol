import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from bootstrap.app import app

if __name__ == "__main__":
    app.run(port=8000, debug=True)
