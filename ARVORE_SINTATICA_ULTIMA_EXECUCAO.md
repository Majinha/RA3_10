# Árvores Sintáticas Abstratas - Última Execução

## 📋 Informações da Análise

**Arquivo Analisado:** `teste_semantica.txt`  
**Data:** 07/11/2025  
**Total de Árvores Geradas:** 12  
**Árvores Válidas:** 8  
**Árvores com Erro:** 4

---

## 🌳 Estrutura das Árvores Sintáticas Abstratas (AST)

Cada árvore representa a estrutura hierárquica de uma expressão em notação polonesa reversa (RPN), anotada com **tipos inferidos** pela análise semântica.

### Formato da AST

```json
{
  "tipo_vertice": "<tipo do nó>",
  "tipo_inferido": "<tipo de dado>",
  "valor": <valor literal ou null>,
  "linha": <número da linha>,
  "filhos": [<lista de sub-árvores>]
}
```

---

## ✅ Árvore #1: Operação Aritmética Simples

### Código Fonte (Linha 4)
```
(5 3 +)
```

### Interpretação Infixa
```
5 + 3
```

### Árvore Sintática Abstrata

```
EXPRESSAO [int]
├── OPERANDO [int] = 5
├── OPERANDO [int] = 3
└── OPERADOR [+]
```

### JSON Completo
```json
{
  "tipo_vertice": "EXPRESSAO",
  "tipo_inferido": "int",
  "valor": null,
  "linha": 4,
  "filhos": [
    {
      "tipo_vertice": "OPERANDO",
      "tipo_inferido": "int",
      "valor": 5,
      "linha": 4,
      "filhos": []
    },
    {
      "tipo_vertice": "OPERANDO",
      "tipo_inferido": "int",
      "valor": 3,
      "linha": 4,
      "filhos": []
    },
    {
      "tipo_vertice": "OPERADOR",
      "tipo_inferido": "nao_determinado",
      "valor": "PLUS",
      "linha": 4,
      "filhos": []
    }
  ]
}
```

### Análise Semântica

**Regra Aplicada:**
```
Γ ⊢ 5 : int    Γ ⊢ 3 : int
───────────────────────────
Γ ⊢ (5 + 3) : int
```

**Tipo Inferido:** `int`  
**Valor Calculado:** 8  
**Status:** ✅ Válido

---

## ✅ Árvore #2: Promoção de Tipos

### Código Fonte (Linha 7)
```
(5 3.5 +)
```

### Interpretação Infixa
```
5 + 3.5
```

### Árvore Sintática Abstrata

```
EXPRESSAO [real]
├── OPERANDO [int] = 5
├── OPERANDO [real] = 3.5
└── OPERADOR [+]
```

### JSON Completo
```json
{
  "tipo_vertice": "EXPRESSAO",
  "tipo_inferido": "real",
  "valor": null,
  "linha": 7,
  "filhos": [
    {
      "tipo_vertice": "OPERANDO",
      "tipo_inferido": "int",
      "valor": 5,
      "linha": 7,
      "filhos": []
    },
    {
      "tipo_vertice": "OPERANDO",
      "tipo_inferido": "real",
      "valor": 3.5,
      "linha": 7,
      "filhos": []
    },
    {
      "tipo_vertice": "OPERADOR",
      "tipo_inferido": "nao_determinado",
      "valor": "PLUS",
      "linha": 7,
      "filhos": []
    }
  ]
}
```

### Análise Semântica

**Regra Aplicada:**
```
Γ ⊢ 5 : int    Γ ⊢ 3.5 : real
──────────────────────────────────
Γ ⊢ (5 + 3.5) : promover_tipo(int, real) = real
```

**Tipo Inferido:** `real` (promoção automática)  
**Valor Calculado:** 8.5  
**Status:** ✅ Válido

---

## ❌ Árvore #3: Erro - Expoente Não-Inteiro

### Código Fonte (Linha 10)
```
(2 3.5 ^)
```

### Interpretação Infixa
```
2 ^ 3.5
```

### Árvore Sintática Abstrata

```
EXPRESSAO [erro]
├── OPERANDO [int] = 2
├── OPERANDO [real] = 3.5
└── OPERADOR [^]
```

### Análise Semântica

**Regra Aplicada:**
```
Γ ⊢ 2 : int    Γ ⊢ 3.5 : real    real ≠ int
──────────────────────────────────────────────
Γ ⊢ (2 ^ 3.5) : erro
```

**Tipo Inferido:** `erro`  
**Erro:** Expoente deve ser inteiro, encontrado real  
**Status:** ❌ Inválido

---

## ❌ Árvore #4: Erro - Divisão Inteira com Real

### Código Fonte (Linha 13)
```
(10.5 2 /)
```

### Interpretação Infixa
```
10.5 / 2
```

### Árvore Sintática Abstrata

```
EXPRESSAO [erro]
├── OPERANDO [real] = 10.5
├── OPERANDO [int] = 2
└── OPERADOR [/]
```

### Análise Semântica

**Regra Aplicada:**
```
Γ ⊢ 10.5 : real    Γ ⊢ 2 : int
──────────────────────────────────────────
Γ ⊢ (10.5 / 2) : erro
    "DIV_INT requer operandos inteiros"
```

**Tipo Inferido:** `erro`  
**Erro:** Operando1 deve ser inteiro  
**Status:** ❌ Inválido

---

## ❌ Árvore #5: Erro - Divisão por Zero

### Código Fonte (Linha 16)
```
(10 0 /)
```

### Interpretação Infixa
```
10 / 0
```

### Árvore Sintática Abstrata

```
EXPRESSAO [erro]
├── OPERANDO [int] = 10
├── OPERANDO [int] = 0
└── OPERADOR [/]
```

### Análise Semântica

**Regra Aplicada:**
```
Γ ⊢ 10 : int    Γ ⊢ 0 : int
────────────────────────────────────
Γ ⊢ (10 / 0) : erro
    "Divisão por zero"
```

**Tipo Inferido:** `erro`  
**Erro:** Divisão por zero detectada  
**Status:** ❌ Inválido

---

## ✅ Árvore #6: Potenciação com Expoente Negativo

### Código Fonte (Linha 19)
```
(2 -3 ^)
```

### Interpretação Infixa
```
2 ^ -3
```

### Árvore Sintática Abstrata

```
EXPRESSAO [int]
├── OPERANDO [int] = 2
├── OPERANDO [int] = -3
└── OPERADOR [^]
```

### JSON Completo
```json
{
  "tipo_vertice": "EXPRESSAO",
  "tipo_inferido": "int",
  "valor": null,
  "linha": 19,
  "filhos": [
    {
      "tipo_vertice": "OPERANDO",
      "tipo_inferido": "int",
      "valor": 2,
      "linha": 19,
      "filhos": []
    },
    {
      "tipo_vertice": "OPERANDO",
      "tipo_inferido": "int",
      "valor": -3,
      "linha": 19,
      "filhos": []
    },
    {
      "tipo_vertice": "OPERADOR",
      "tipo_inferido": "nao_determinado",
      "valor": "POW",
      "linha": 19,
      "filhos": []
    }
  ]
}
```

### Análise Semântica

**Regra Aplicada:**
```
Γ ⊢ 2 : int    Γ ⊢ -3 : int
─────────────────────────────
Γ ⊢ (2 ^ -3) : int
```

**Tipo Inferido:** `int`  
**Observação:** ✨ Expoente negativo **permitido** (melhoria implementada)  
**Valor Calculado:** 0 (em divisão inteira: 2^-3 = 1/8 = 0)  
**Status:** ✅ Válido

---

## ✅ Árvore #7: Declaração de Variável

### Código Fonte (Linha 22)
```
(42 x MEM)
```

### Interpretação
```
x = 42
```

### Árvore Sintática Abstrata

```
COMANDO_MEM [int]
├── OPERANDO [int] = 42
└── ID = "x"
```

### Análise Semântica

**Regra Aplicada:**
```
Γ ⊢ 42 : int    x ∉ Γ    int ≠ booleano
─────────────────────────────────────────
Γ[x ↦ int] ⊢ (42 x MEM) : int
```

**Tipo Inferido:** `int`  
**Efeito Colateral:** Adiciona `x : int` à tabela de símbolos  
**Status:** ✅ Válido

### Tabela de Símbolos Atualizada

| Variável | Tipo | Inicializada | Linha Declaração |
|----------|------|--------------|------------------|
| x | int | ✅ | 22 |

---

## ✅ Árvore #8: Uso de Variável

### Código Fonte (Linha 25)
```
(x 2 *)
```

### Interpretação Infixa
```
x * 2
```

### Árvore Sintática Abstrata

```
EXPRESSAO [int]
├── LEITURA_MEM [int]
│   └── ID = "x"
├── OPERANDO [int] = 2
└── OPERADOR [*]
```

### Análise Semântica

**Regra Aplicada:**
```
x : int ∈ Γ    Γ ⊢ x : int    Γ ⊢ 2 : int
───────────────────────────────────────────
Γ ⊢ (x * 2) : int
```

**Tipo Inferido:** `int`  
**Valor (se x = 42):** 84  
**Status:** ✅ Válido

---

## ❌ Árvore #9: Erro - Variável Não Declarada

### Código Fonte (Linha 28)
```
(y 3 +)
```

### Interpretação Infixa
```
y + 3
```

### Árvore Sintática Abstrata

```
EXPRESSAO [erro]
├── ID = "y" [erro]
├── OPERANDO [int] = 3
└── OPERADOR [+]
```

### Análise Semântica

**Regra Aplicada:**
```
y ∉ Γ
──────────────────────────────────
Γ ⊢ y : erro
    "Variável não declarada"
```

**Tipo Inferido:** `erro`  
**Erro:** Variável 'y' não foi declarada  
**Status:** ❌ Inválido

---

## ✅ Árvore #10: Operador Relacional

### Código Fonte (Linha 35)
```
(10 5 >)
```

### Interpretação Infixa
```
10 > 5
```

### Árvore Sintática Abstrata

```
EXPRESSAO [booleano]
├── OPERANDO [int] = 10
├── OPERANDO [int] = 5
└── OPERADOR [>]
```

### JSON Completo
```json
{
  "tipo_vertice": "EXPRESSAO",
  "tipo_inferido": "booleano",
  "valor": null,
  "linha": 35,
  "filhos": [
    {
      "tipo_vertice": "OPERANDO",
      "tipo_inferido": "int",
      "valor": 10,
      "linha": 35,
      "filhos": []
    },
    {
      "tipo_vertice": "OPERANDO",
      "tipo_inferido": "int",
      "valor": 5,
      "linha": 35,
      "filhos": []
    },
    {
      "tipo_vertice": "OPERADOR",
      "tipo_inferido": "booleano",
      "valor": "GT",
      "linha": 35,
      "filhos": []
    }
  ]
}
```

### Análise Semântica

**Regra Aplicada:**
```
Γ ⊢ 10 : int    Γ ⊢ 5 : int
───────────────────────────────
Γ ⊢ (10 > 5) : booleano
```

**Tipo Inferido:** `booleano`  
**Valor Lógico:** `true`  
**Status:** ✅ Válido

---

## 📊 Estatísticas das Árvores

### Distribuição de Tipos

| Tipo Inferido | Quantidade | Percentual |
|---------------|------------|------------|
| int | 5 | 41.7% |
| real | 1 | 8.3% |
| booleano | 2 | 16.7% |
| erro | 4 | 33.3% |

### Distribuição de Nós

| Tipo de Nó | Quantidade |
|------------|------------|
| EXPRESSAO | 9 |
| OPERANDO | 24 |
| OPERADOR | 9 |
| COMANDO_MEM | 1 |
| LEITURA_MEM | 1 |
| ID | 2 |

### Operadores Utilizados

| Operador | Símbolo | Frequência |
|----------|---------|------------|
| Adição | + | 3 |
| Multiplicação | * | 1 |
| Potenciação | ^ | 2 |
| Divisão inteira | / | 2 |
| Módulo | % | 1 |
| Maior que | > | 1 |

---

## 🎯 Análise Qualitativa

### Aspectos Positivos

1. **Promoção de Tipos Automática**
   - Conversão correta de `int` para `real`
   - Exemplo: `(5 3.5 +)` → `real`

2. **Validação Rigorosa**
   - Detecção de incompatibilidade de tipos
   - Verificação de divisão por zero
   - Controle de declaração de variáveis

3. **Expoente Negativo Permitido** ✨
   - Flexibilidade matemática
   - Exemplo: `(2 -3 ^)` aceito

### Aspectos para Atenção

1. **Restrições de Operadores**
   - `/` e `%` requerem ambos operandos `int`
   - `^` requer expoente `int`

2. **Gerenciamento de Memória**
   - Variáveis devem ser declaradas antes do uso
   - Booleanos não podem ser armazenados

---

## 🔍 Visualização Comparativa

### Árvore Válida vs. Árvore com Erro

#### Válida: `(5 3 +)`
```
EXPRESSAO [int] ✅
├── OPERANDO [int] = 5
├── OPERANDO [int] = 3
└── OPERADOR [+]

Resultado: 8
```

#### Com Erro: `(2 3.5 ^)`
```
EXPRESSAO [erro] ❌
├── OPERANDO [int] = 2
├── OPERANDO [real] = 3.5 ⚠️
└── OPERADOR [^]

Erro: Expoente deve ser inteiro
```

---

## 📖 Legenda

### Símbolos Usados

| Símbolo | Significado |
|---------|-------------|
| ✅ | Válido - sem erros |
| ❌ | Inválido - com erros |
| ⚠️ | Atenção - ponto crítico |
| ✨ | Novo recurso/melhoria |

### Tipos de Dados

| Tipo | Descrição |
|------|-----------|
| `int` | Número inteiro |
| `real` | Número com ponto decimal |
| `booleano` | Valor lógico (true/false) |
| `erro` | Tipo de erro semântico |

---

## 🔗 Documentação Relacionada

- **GRAMATICA_ATRIBUTOS.md**: Regras formais de tipo
- **REGRAS_DEDUCAO.md**: Dedução de tipos detalhada
- **ERROS_SEMANTICOS_DETECTADOS.md**: Análise dos erros

---

**Gerado Por:** Compilador RPN v3.0  
**Data:** 07/11/2025  
**Autores:** João Victor Roth, Mariana Trentiny Barbosa  
**Instituição:** PUCPR
