import pytest
from src.normalization import normalize_scores

def test_normalize_scores_basic():
    """Teste unitário básico de escala min-max [0.0, 1.0]."""
    scores = [10.0, 20.0, 30.0]
    expected = [0.0, 0.5, 1.0]
    assert normalize_scores(scores) == pytest.approx(expected)

def test_normalize_scores_custom_range():
    """Teste de normalização com intervalo customizado [-1.0, 1.0]."""
    scores = [0.0, 50.0, 100.0]
    expected = [-1.0, 0.0, 1.0]
    assert normalize_scores(scores, min_target=-1.0, max_target=1.0) == pytest.approx(expected)
