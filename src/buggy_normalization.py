def buggy_normalize_scores(
    scores: list[float],
    min_target: float = 0.0,
    max_target: float = 1.0,
) -> list[float]:
    """Versão com bug de inversão para teste de propriedade."""
    if not scores:
        return []
    min_val = min(scores)
    max_val = max(scores)
    diff = max_val - min_val
    return [min_target + (max_val - x) * (max_target - min_target) / diff for x in scores]
