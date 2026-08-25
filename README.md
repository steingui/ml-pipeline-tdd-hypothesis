# ML Pipeline - Normalização de Scores com TDD e Testes de Propriedade (Hypothesis)

Este repositório contém a implementação da função `normalize_scores` para pipelines de Machine Learning, desenvolvida com rigor técnico aplicando **TDD (Test-Driven Development)** e **Property-Based Testing (Hypothesis)**.

- **Repositório GitHub:** [https://github.com/steingui/ml-pipeline-tdd-hypothesis](https://github.com/steingui/ml-pipeline-tdd-hypothesis)

---

## 📌 1. Função Escolhida: Normalização Min-Max de Scores em Batch (`normalize_scores`)

Em pipelines de aprendizado de máquina, previsões ou scores brutos oriundos de múltiplos modelos precisam ser normalizados para um intervalo padronizado (ex.: `[0.0, 1.0]` ou `[-1.0, 1.0]`) antes de etapas de ranking, ensembling ou tomada de decisão.

### 📝 Documentação das Decisões de Design (Edge Cases)

| Cenário de Borda | Comportamento Adoptado | Justificativa no Pipeline de ML |
| :--- | :--- | :--- |
| **Entradas Vazias (`[]`)** | Retorna `[]` | Garante segurança operacional sem lançar exceção ao processar lotes vazios. |
| **Valores `NaN`** | Imputação pela média dos valores finitos do lote (`mean_val`) | Evita propagação de contaminação por valores ausentes no modelo. |
| **Valores `Inf` (`+inf` / `-inf`)** | *Clipping* (truncamento) para os limites finitos max/min do lote | Preserva a escala sem estourar cálculos de ponto flutuante. |
| **Divisão por Zero (`max == min`)** | Retorna vetor constante com valor `min_target` | Evita erro de divisão por zero quando todos os dados de entrada são idênticos. |
| **Limites Inválidos (`min_target >= max_target`)** | Lança `ValueError` | Evita configurações inconsistentes na escala de saída. |

---

## 🔄 2. Histórico do Ciclo TDD (Red → Green → Refactor)

O desenvolvimento seguiu rigorosamente o ciclo TDD com commits atômicos para cada fase:

```bash
* 08cc069 test: adiciona testes de propriedade Hypothesis e prova de captura de bug (PROPERTY)
* f70e12e refactor: adiciona tratamento de NaN, Inf, divisao por zero e testes (REFACTOR)
* c4c4559 feat: implementa codigo minimo de normalizacao (GREEN)
* d9e17ed test: adiciona testes unitarios de normalizacao de scores (RED)
```

1. **🔴 RED (`d9e17ed`)**: Criação da suíte inicial de testes unitários em `tests/test_normalization.py` com stub lançando `NotImplementedError`.
2. **🟢 GREEN (`c4c4559`)**: Implementação do algoritmo básico de escala min-max estritamente necessário para fazer os testes passarem.
3. **🔵 REFACTOR (`f70e12e`)**: Refatoração do código com suporte a `NaN`, `Inf`, tolerância numérica e validações de borda, além de novos testes unitários cobrindo cenários limite.

---

## 🧪 3. Testes de Propriedade (Hypothesis)

Usando a biblioteca **Hypothesis**, foram definidos testes baseados em **invariantes** matemáticas que devem ser válidas para qualquer entrada:

1. **Invariante 1: Limitabilidade (Boundedness)**
   - *Regra:* $\forall x_i \in \text{scores}, \quad \text{min\_target} \le y_i \le \text{max\_target}$
   - Testa milhares de combinações de listas de floats geradas aleatoriamente.
2. **Invariante 2: Monotonicidade / Preservação de Ordem**
   - *Regra:* $x_i \le x_j \implies y_i \le y_j$
   - Garante que a ordem relativa de pontuação do modelo ML não é alterada após a normalização.

---

## 🐛 4. Prova de Captura de Bug Real

Para demonstrar o valor prático do teste de propriedade, foi criada a função `buggy_normalize_scores` em `src/buggy_normalization.py` que introduz um bug comum de produção: **inversão de ordem** (calculando `max_val - x` em vez de `x - min_val`).

Ao rodar o teste de propriedade de monotonicidade contra a função bugada (`tests/test_buggy_normalization.py`), o Hypothesis encontra o menor contraexemplo em milissegundos e falha com o seguinte relatório:

```text
Falsifying example: test_buggy_property_monotonicity_fails(
    scores=[0.0, 1.0]
)
> assert result[i] <= result[j] + tol
E AssertionError: assert 1.0 <= 0.0 + 1e-06
```

---

## 🚀 Como Executar os Testes Localmente

```bash
# 1. Clonar o repositório
git clone https.github.com/steingui/ml-pipeline-tdd-hypothesis.git
cd ml-pipeline-tdd-hypothesis

# 2. Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar a suíte de testes completa com pytest
PYTHONPATH=. pytest -v
```
