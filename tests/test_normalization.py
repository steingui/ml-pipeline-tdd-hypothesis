import math
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

def test_normalize_scores_empty():
    """Lista vazia deve retornar lista vazia."""
    assert normalize_scores([]) == []

def test_normalize_scores_constant():
    """Lista com valores constantes deve retornar min_target sem erro de divisão por zero."""
    scores = [5.0, 5.0, 5.0]
    assert normalize_scores(scores, min_target=0.0) == [0.0, 0.0, 0.0]

def test_normalize_scores_invalid_bounds():
    """Intervalos inválidos devem lançar ValueError."""
    with pytest.raises(ValueError):
        normalize_scores([1.0, 2.0], min_target=1.0, max_target=0.0)

def test_normalize_scores_handles_nan():
    """Valores NaN devem ser substituídos pela média dos finitos antes da escala."""
    scores = [0.0, math.nan, 100.0]
    # Média dos finitos (0 e 100) é 50
    # Scores limpos: [0, 50, 100] -> Normalizados: [0.0, 0.5, 1.0]
    expected = [0.0, 0.5, 1.0]
    assert normalize_scores(scores) == pytest.approx(expected)

def test_normalize_scores_handles_inf():
    """Valores infinitos devem ser truncados para os extremos finitos."""
    scores = [-math.inf, 10.0, 20.0, math.inf]
    # Finitos min=10, max=20 -> Limpos: [10, 10, 20, 20]
    # Normalizados: [0.0, 0.0, 1.0, 1.0]
    expected = [0.0, 0.0, 1.0, 1.0]
    assert normalize_scores(scores) == pytest.approx(expected)
