from hypothesis import given, strategies as st
import pytest
from src.normalization import normalize_scores

finite_floats = st.floats(allow_nan=False, allow_infinity=False, min_value=-1e9, max_value=1e9)
valid_scores = st.lists(finite_floats, min_size=1, max_size=200)


@given(scores=valid_scores, min_target=st.floats(-100, 100), max_target=st.floats(-100, 100))
def test_property_boundedness(scores: list[float], min_target: float, max_target: float):
    if min_target >= max_target:
        with pytest.raises(ValueError):
            normalize_scores(scores, min_target, max_target)
        return

    result = normalize_scores(scores, min_target, max_target)
    assert len(result) == len(scores)

    tol = 1e-6
    for val in result:
        assert min_target - tol <= val <= max_target + tol


@given(scores=valid_scores)
def test_property_monotonicity(scores: list[float]):
    min_target, max_target = 0.0, 1.0
    result = normalize_scores(scores, min_target, max_target)

    tol = 1e-6
    for i in range(len(scores)):
        for j in range(len(scores)):
            if scores[i] <= scores[j]:
                assert result[i] <= result[j] + tol
