# tests/test_quality.py
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from transform import transform
from quality import validate

def test_transform_has_core_columns():
    df = transform()
    assert {'id','title','author','score','time'}.issubset(df.columns)

def test_quality_validate_passes():
    df = transform()
    validate(df)