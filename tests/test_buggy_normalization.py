from hypothesis import given, strategies as st
import pytest
from src.buggy_normalization import buggy_normalize_scores

finite_floats = st.floats(allow_nan=False, allow_infinity=False, min_value=-1e9, max_value=1e9)
valid_scores = st.lists(finite_floats, min_size=2, max_size=50)


@pytest.mark.xfail(strict=True, reason="Inversao de ordem detectada via teste de propriedade")
@given(scores=valid_scores)
def test_buggy_property_monotonicity_fails(scores: list[float]):
    min_target, max_target = 0.0, 1.0
    result = buggy_normalize_scores(scores, min_target, max_target)

    tol = 1e-6
    for i in range(len(scores)):
        for j in range(len(scores)):
            if scores[i] < scores[j]:
                assert result[i] <= result[j] + tol
