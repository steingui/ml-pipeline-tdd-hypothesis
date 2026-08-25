import math
import pytest
from src.normalization import normalize_scores


def test_normalize_scores_basic():
    scores = [10.0, 20.0, 30.0]
    expected = [0.0, 0.5, 1.0]
    assert normalize_scores(scores) == pytest.approx(expected)


def test_normalize_scores_custom_range():
    scores = [0.0, 50.0, 100.0]
    expected = [-1.0, 0.0, 1.0]
    assert normalize_scores(scores, min_target=-1.0, max_target=1.0) == pytest.approx(expected)


def test_normalize_scores_empty():
    assert normalize_scores([]) == []


def test_normalize_scores_constant():
    scores = [5.0, 5.0, 5.0]
    assert normalize_scores(scores, min_target=0.0) == [0.0, 0.0, 0.0]


def test_normalize_scores_invalid_bounds():
    with pytest.raises(ValueError):
        normalize_scores([1.0, 2.0], min_target=1.0, max_target=0.0)


def test_normalize_scores_handles_nan():
    scores = [0.0, math.nan, 100.0]
    expected = [0.0, 0.5, 1.0]
    assert normalize_scores(scores) == pytest.approx(expected)


def test_normalize_scores_handles_inf():
    scores = [-math.inf, 10.0, 20.0, math.inf]
    expected = [0.0, 0.0, 1.0, 1.0]
    assert normalize_scores(scores) == pytest.approx(expected)
