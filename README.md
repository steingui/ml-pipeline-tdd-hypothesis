# ML Pipeline - Normalização com TDD e Hypothesis

Implementação da função `normalize_scores` para pipelines de ML aplicando TDD e testes de propriedade com Hypothesis.

## Decisões de Design (Edge Cases)

- **NaN**: Substituído pela média dos valores finitos do lote.
- **Inf (`+inf`/`-inf`)**: Truncado para os limites finitos min/max do lote.
- **Divisão por zero (`max == min`)**: Retorna vetor constante com `min_target`.
- **Limites inválidos (`min_target >= max_target`)**: Lança `ValueError`.

## Ciclo TDD (Commits)

1. `d9e17ed` **RED**: Testes unitários iniciais com falha.
2. `c4c4559` **GREEN**: Código mínimo para aprovação dos testes.
3. `f70e12e` **REFACTOR**: Tratamento de `NaN`, `Inf`, divisão por zero e novos testes.

## Testes de Propriedade (Hypothesis)

- **Limitabilidade**: `min_target <= y_i <= max_target` para qualquer entrada válida.
- **Monotonicidade**: Preservação da ordem relativa (`x_i <= x_j => y_i <= y_j`).

## Prova de Captura de Bug Real

A função `buggy_normalize_scores` (`src/buggy_normalization.py`) inverte a ordem dos scores. O Hypothesis detecta o bug e falha no teste de monotonicidade (`tests/test_buggy_normalization.py`):

```text
Falsifying example: test_buggy_property_monotonicity_fails(scores=[0.0, 1.0])
AssertionError: assert 1.0 <= 0.0 + 1e-06
```

## Execução

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest
```
