"""Módulo de normalização de dados para pipelines de ML."""

def normalize_scores(scores: list[float], min_target: float = 0.0, max_target: float = 1.0) -> list[float]:
    """Normaliza uma lista de scores para o intervalo [min_target, max_target]."""
    if not scores:
        return []
    min_val = min(scores)
    max_val = max(scores)
    diff = max_val - min_val
    if diff == 0:
        return [min_target] * len(scores)
    return [min_target + (x - min_val) * (max_target - min_target) / diff for x in scores]
