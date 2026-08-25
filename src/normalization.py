"""Módulo de normalização de dados para pipelines de ML."""

import math

def normalize_scores(
    scores: list[float],
    min_target: float = 0.0,
    max_target: float = 1.0
) -> list[float]:
    """
    Normaliza uma lista de scores de modelo ML para o intervalo [min_target, max_target].

    Decisões de Design (Tratamento de Edge Cases):
    1. Entradas vazias: Retorna lista vazia [].
    2. Intervalo inválido (min_target >= max_target): Lança ValueError.
    3. NaNs: Valores NaN são substituídos pela média dos valores válidos (finitos) da lista.
       Se todos forem NaN, substitui por min_target.
    4. Infs (+inf e -inf): Valores infinitos são truncados para o maior/menor valor finito
       encontrado na amostra.
    5. Divisão por zero (valores constantes, max == min): Retorna min_target para todos os elementos.
    """
    if min_target >= max_target:
        raise ValueError(f"min_target ({min_target}) deve ser menor que max_target ({max_target})")
    
    if not scores:
        return []

    # 1. Trata NaNs identificando valores finitos
    finites = [x for x in scores if not math.isnan(x) and not math.isinf(x)]
    
    if not finites:
        # Se nenhum valor finito existir, preenche com min_target
        return [min_target] * len(scores)

    mean_val = sum(finites) / len(finites)
    min_finite = min(finites)
    max_finite = max(finites)

    # Clean e clip da lista de entrada
    cleaned_scores: list[float] = []
    for x in scores:
        if math.isnan(x):
            cleaned_scores.append(mean_val)
        elif math.isinf(x):
            cleaned_scores.append(max_finite if x > 0 else min_finite)
        else:
            cleaned_scores.append(x)

    # Recalcula min e max após limpeza
    min_val = min(cleaned_scores)
    max_val = max(cleaned_scores)
    diff = max_val - min_val

    # Se todos os valores forem iguais após limpos (divisão por zero)
    if diff == 0.0:
        return [min_target] * len(scores)

    target_range = max_target - min_target
    return [min_target + (x - min_val) * target_range / diff for x in cleaned_scores]
