# Erros Semânticos Detectados - Última Execução

## 📋 Relatório de Erros

**Arquivo Analisado:** `main.py`  
**Data da Análise:** 07/11/2025  
**Total de Erros:** 5 erros semânticos detectados

---

## ❌ Erro #1: Expoente Não-Inteiro na Potenciação

**Linha:** 10  
**Código:** `(2 3.5 ^)`

**Erro Detectado:**
```
ERRO SEMÂNTICO [Linha 10]: Expoente de potenciação deve ser inteiro, encontrado real
Contexto: (2 3.5 ^)
```

**Explicação:**
- O operador de potenciação (`^`) exige que o **expoente seja do tipo inteiro**
- A base pode ser `int` ou `real`, mas o expoente deve ser `int`
- Neste caso, `3.5` é do tipo `real`, violando a regra

**Regra Violada:**
```
Γ ⊢ base : T    Γ ⊢ exp : real    real ≠ int
──────────────────────────────────────────────
Γ ⊢ (base exp ^) : erro
```

**Correção:**
```
(2 3 ^)     # ✅ Correto: expoente inteiro
(2 4 ^)     # ✅ Correto: 16
(2 -2 ^)    # ✅ Correto: expoente negativo permitido
```

---

## ❌ Erro #2: Divisão Inteira com Operando Real

**Linha:** 13  
**Código:** `(10.5 2 /)`

**Erro Detectado:**
```
ERRO SEMÂNTICO [Linha 13]: Operação DIV_INT requer operando1 inteiro, encontrado real
Contexto: (10.5 2 /)
```

**Explicação:**
- O operador de divisão inteira (`/`) requer que **ambos os operandos sejam inteiros**
- O primeiro operando `10.5` é do tipo `real`
- Para divisão com reais, use o operador de divisão real (`|`)

**Regra Violada:**
```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : int
──────────────────────────────────
Γ ⊢ (e₁ e₂ /) : erro
```

**Correção:**
```
(10 2 /)      # ✅ Correto: divisão inteira → 5
(10.5 2 |)    # ✅ Correto: divisão real → 5.25
(11 2 /)      # ✅ Correto: divisão inteira → 5
```

---

## ❌ Erro #3: Divisão por Zero

**Linha:** 16  
**Código:** `(10 0 /)`

**Erro Detectado:**
```
ERRO SEMÂNTICO [Linha 16]: Divisão por zero detectada
Contexto: (10 0 /)
```

**Explicação:**
- Divisão ou módulo por zero é **matematicamente indefinido**
- O compilador detecta divisão por zero quando o divisor é um literal `0`
- Este erro se aplica aos operadores `/`, `|` e `%`

**Regra Violada:**
```
Γ ⊢ e₁ : int    Γ ⊢ 0 : int
────────────────────────────────
Γ ⊢ (e₁ 0 /) : erro
```

**Correção:**
```
(10 2 /)    # ✅ Correto: 5
(10 5 /)    # ✅ Correto: 2
(10 1 /)    # ✅ Correto: 10
```

---

## ❌ Erro #4: Variável Não Declarada

**Linha:** 28  
**Código:** `(y 3 +)`

**Erro Detectado:**
```
ERRO SEMÂNTICO [Linha 28]: Variável 'y' não declarada
Contexto: (y 3 +)
```

**Explicação:**
- Tentativa de usar a variável `y` antes de sua declaração
- Todas as variáveis devem ser declaradas com `MEM` antes do uso
- A variável `x` foi declarada anteriormente (linha 22), mas `y` não

**Regra Violada:**
```
y ∉ Γ
──────────────────────────
Γ ⊢ y : erro
```

**Correção:**
```
(5 y MEM)     # Primeiro declare
(y 3 +)       # ✅ Agora pode usar
```

---

## ❌ Erro #5: Módulo com Operando Real

**Linha:** 47  
**Código:** `(10.5 3 %)`

**Erro Detectado:**
```
ERRO SEMÂNTICO [Linha 47]: Operação MOD requer operando1 inteiro, encontrado real
Contexto: (10.5 3 %)
```

**Explicação:**
- O operador de módulo (`%`) requer que **ambos os operandos sejam inteiros**
- O módulo é definido apenas para números inteiros
- O primeiro operando `10.5` é do tipo `real`

**Regra Violada:**
```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : int
──────────────────────────────────
Γ ⊢ (e₁ e₂ %) : erro
```

**Correção:**
```
(10 3 %)     # ✅ Correto: 1
(15 4 %)     # ✅ Correto: 3
(7 2 %)      # ✅ Correto: 1
```

---

## ✅ Casos Válidos Identificados

Durante a análise, os seguintes casos foram **validados com sucesso**:

### 1. Operação Aritmética Simples
```
(5 3 +)    → int
```
- Ambos operandos são `int`
- Resultado: `int`

### 2. Promoção de Tipos
```
(5 3.5 +)  → real
```
- `int` + `real` → `real` (promoção automática)
- Regra: `promover_tipo(int, real) = real`

### 3. Potenciação com Expoente Negativo ✨
```
(2 -3 ^)   → int
```
- Expoente negativo **é permitido**!
- Expoente é `int` (mesmo sendo negativo)
- Esta é uma **melhoria implementada** na última versão

### 4. Declaração de Variável
```
(42 x MEM) → int
```
- Armazena valor `42` em variável `x`
- Tipo inferido: `int`

### 5. Uso de Variável
```
(x 2 *)    → int
```
- Usa variável `x` previamente declarada
- `int` * `int` → `int`

### 6. Operador Relacional
```
(10 5 >)   → booleano
```
- Comparação entre inteiros
- Retorna tipo `booleano`

### 7. Condição IF Válida
```
((10 5 >) (100) (200) IF) → int
```
- Condição é booleana: `(10 5 >)` ✓
- Ambos ramos são `int`
- Resultado: `int`

### 8. Módulo com Inteiros
```
(10 3 %)   → int
```
- Ambos operandos são `int` ✓
- Resultado: `1`

---

## 📊 Estatísticas da Análise

| Métrica | Valor |
|---------|-------|
| **Total de linhas processadas** | 15 |
| **Linhas válidas** | 10 (66.7%) |
| **Linhas com erro** | 5 (33.3%) |
| **Erros de tipo** | 4 (80%) |
| **Erros de memória** | 1 (20%) |
| **Erros de divisão** | 1 (20%) |

---

## 🎯 Categorização dos Erros

### Erros de Tipo (4 erros)
1. Expoente não-inteiro
2. Divisão inteira com real
3. Módulo com real
4. *(Variável não declarada também envolve tipo)*

### Erros de Memória (1 erro)
1. Variável não declarada

### Erros de Operação (1 erro)
1. Divisão por zero

---

## 🔍 Análise Detalhada por Categoria

### Categoria 1: Restrições de Tipo em Operadores

Três erros (#1, #2, #5) foram causados por **violação de restrições de tipo**:
- `^` requer expoente `int`
- `/` requer ambos operandos `int`
- `%` requer ambos operandos `int`

**Lição:** Operadores especiais têm restrições específicas de tipo.

### Categoria 2: Divisão por Zero

Erro #3 é um **erro de operação matemática**:
- Detectado quando divisor é literal `0`
- Previne erros em tempo de execução

**Lição:** O compilador detecta alguns erros matemáticos durante análise estática.

### Categoria 3: Gerenciamento de Memória

Erro #4 é um **erro de gerenciamento de escopo**:
- Variável usada antes da declaração
- Violação da tabela de símbolos

**Lição:** Todas as variáveis devem ser declaradas antes do uso.

---

## ✨ Melhorias Implementadas

### Potenciação com Expoente Negativo

**Antes:**
```
(2 -3 ^)  ❌ ERRO: expoente deve ser positivo
```

**Agora:**
```
(2 -3 ^)  ✅ VÁLIDO: expoente negativo permitido!
```

Esta melhoria permite expressões como:
- `2^-1` → potências negativas
- `10^-3` → notação científica simplificada
- `x^-n` → inversões

**Justificativa:** Expoentes negativos são matemat icamente válidos e úteis.

---

## 📝 Formato de Mensagens de Erro

Todas as mensagens seguem o padrão:
```
ERRO SEMÂNTICO [Linha X]: <descrição clara do problema>
Contexto: <trecho de código relevante>
```

**Benefícios:**
- Localização precisa do erro
- Descrição clara do problema
- Contexto para facilitar correção

---

## 🔗 Regras Semânticas Aplicadas

### Regras de Inferência Usadas

1. **Potenciação:** `Γ ⊢ base : T, Γ ⊢ exp : int ⇒ Γ ⊢ (base exp ^) : T`
2. **Divisão Inteira:** `Γ ⊢ e₁ : int, Γ ⊢ e₂ : int ⇒ Γ ⊢ (e₁ e₂ /) : int`
3. **Módulo:** `Γ ⊢ e₁ : int, Γ ⊢ e₂ : int ⇒ Γ ⊢ (e₁ e₂ %) : int`
4. **Variável:** `x : T ∈ Γ ⇒ Γ ⊢ x : T`

---

## 📖 Referências

- **GRAMATICA_ATRIBUTOS.md**: Regras formais completas
- **REGRAS_DEDUCAO.md**: Exemplos de aplicação das regras
- **MANUAL_USUARIO.md**: Guia de uso e solução de erros

---

**Análise Realizada Por:** Compilador RPN v3.0  
**Data:** 07/11/2025  
**Autores do Compilador:** João Victor Roth, Mariana Trentiny Barbosa  
**Instituição:** PUCPR
