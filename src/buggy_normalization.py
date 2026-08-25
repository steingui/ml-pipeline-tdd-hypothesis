"""Implementação propositalmente bugada para demonstrar a eficácia dos testes de propriedade."""

def buggy_normalize_scores(scores: list[float], min_target: float = 0.0, max_target: float = 1.0) -> list[float]:
    """
    Versão propositalmente bugada.
    
    Bugs contidos:
    1. Inversão de ordem (Monotonicidade violada): Calcula (max_val - x) em vez de (x - min_val).
    2. ZeroDivisionError: Não trata o caso em que min_val == max_val.
    """
    if not scores:
        return []
    min_val = min(scores)
    max_val = max(scores)
    diff = max_val - min_val
    # BUG: Fórmula inverte os valores (maior vira menor e vice-versa)
    return [min_target + (max_val - x) * (max_target - min_target) / diff for x in scores]
