# tests/test_quality.py
import sys, pathlib, subprocess
import pytest

# allow importing project modules
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

RAW_DIR = pathlib.Path("data/raw")

@pytest.fixture(scope="session", autouse=True)
def ensure_raw_data():
    # If no raw snapshot exists, fetch one before tests run
    if not list(RAW_DIR.glob("hn_*.json")):
        subprocess.check_call([sys.executable, "ingest.py"])

from transform import transform
from quality import validate

def test_transform_has_core_columns():
    df = transform()
    assert {'id','title','author','score','time'}.issubset(df.columns)

def test_quality_validate_passes():
    df = transform()
    validate(df)