import math


def normalize_scores(
    scores: list[float],
    min_target: float = 0.0,
    max_target: float = 1.0,
) -> list[float]:
    """Normaliza uma lista de scores de modelo para o intervalo [min_target, max_target]."""
    if min_target >= max_target:
        raise ValueError(f"min_target deve ser menor que max_target: {min_target} >= {max_target}")

    if not scores:
        return []

    finites = [x for x in scores if not math.isnan(x) and not math.isinf(x)]
    if not finites:
        return [min_target] * len(scores)

    mean_val = sum(finites) / len(finites)
    min_finite = min(finites)
    max_finite = max(finites)

    cleaned: list[float] = []
    for x in scores:
        if math.isnan(x):
            cleaned.append(mean_val)
        elif math.isinf(x):
            cleaned.append(max_finite if x > 0 else min_finite)
        else:
            cleaned.append(x)

    min_val = min(cleaned)
    max_val = max(cleaned)
    diff = max_val - min_val

    if diff == 0.0:
        return [min_target] * len(scores)

    target_range = max_target - min_target
    return [min_target + (x - min_val) * target_range / diff for x in cleaned]
