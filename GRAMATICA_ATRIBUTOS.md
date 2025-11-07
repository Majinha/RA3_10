# Gramática de Atributos - Analisador Semântico RPN

## 📋 Introdução

Este documento descreve formalmente a **gramática de atributos** utilizada no analisador semântico do compilador RPN. A gramática define as regras semânticas para verificação de tipos, promoção automática e validação de operadores.

---

## 🎯 Definições Fundamentais

### Tipos de Dados

O sistema de tipos suporta três tipos primitivos:

```
T ::= int | real | booleano | erro
```

- **int**: Números inteiros (ex: 5, -3, 42)
- **real**: Números com ponto decimal (ex: 3.14, -0.5, 2.0)
- **booleano**: Resultado de operações relacionais (true/false)
- **erro**: Tipo especial para expressões com erro semântico

### Notação Matemática

Usamos a notação de dedução natural:

```
Γ ⊢ e : T
```

Significado:
- **Γ** (Gamma): Ambiente/contexto com a tabela de símbolos
- **⊢**: Símbolo de dedução ("pode deduzir")
- **e**: Expressão sendo analisada
- **T**: Tipo inferido da expressão

---

## 📝 Atributos

### Atributos Sintetizados

Atributos calculados de baixo para cima na árvore (dos filhos para o pai):

| Atributo | Símbolo | Descrição |
|----------|---------|-----------|
| **tipo** | τ | Tipo de dado da expressão |
| **valor** | v | Valor literal (quando aplicável) |
| **linha** | l | Número da linha no código |

### Atributos Herdados

Atributos calculados de cima para baixo (do pai para os filhos):

| Atributo | Símbolo | Descrição |
|----------|---------|-----------|
| **contexto** | Γ | Tabela de símbolos disponível |
| **esperado** | T_esp | Tipo esperado pelo contexto |

---

## 🔤 Gramática EBNF Anotada

### Estrutura Geral

```ebnf
(* Programa completo *)
programa ::= linha+

(* Linha de código *)
linha ::= expressao | comando | estrutura_controle

(* Expressão com atributos *)
expressao ::= operando operando operador
    {τ := inferir_tipo(operando₁.τ, operando₂.τ, operador.tipo)}

(* Operando com atributos *)
operando ::= literal | identificador | expressao
    {τ := tipo_literal ∨ tipo_identificador ∨ τ_expressao}

(* Literal *)
literal ::= INT_LITERAL {τ := int} 
          | REAL_LITERAL {τ := real}

(* Identificador *)
identificador ::= ID
    {τ := Γ(ID).tipo, se ID ∈ Γ
     erro := "Variável não declarada", caso contrário}

(* Operador *)
operador ::= op_aritmetico | op_relacional

op_aritmetico ::= '+' | '-' | '*' | '|' | '/' | '%' | '^'
op_relacional ::= '>' | '<' | '>=' | '<=' | '==' | '!='
    {τ := booleano}

(* Comandos *)
comando ::= MEM | RES

MEM ::= expressao identificador 'MEM'
    {Γ := Γ ∪ {identificador ↦ expressao.τ}
     erro := se expressao.τ = booleano}

RES ::= INT_LITERAL 'RES'
    {τ := tipo_resultado(INT_LITERAL)
     erro := se INT_LITERAL < 0 ∨ INT_LITERAL ≥ |resultados|}

(* Estruturas de Controle *)
estrutura_controle ::= IF | WHILE | FOR

IF ::= condicao expressao_then expressao_else 'IF'
    {τ := promover_tipo(expressao_then.τ, expressao_else.τ)
     erro := se condicao.τ ≠ booleano}

WHILE ::= condicao expressao 'WHILE'
    {τ := expressao.τ
     erro := se condicao.τ ≠ booleano}

FOR ::= inicio condicao incremento expressao 'FOR'
    {τ := expressao.τ
     erro := se condicao.τ ≠ booleano}
```

---

## 🎯 Regras de Produção com Atributos

### 1. Literal Inteiro

```
─────────────────────
Γ ⊢ n : int

Onde n ∈ ℤ
```

**Exemplo:**
```
─────────────────────
Γ ⊢ 42 : int
```

### 2. Literal Real

```
─────────────────────
Γ ⊢ r : real

Onde r ∈ ℝ
```

**Exemplo:**
```
─────────────────────
Γ ⊢ 3.14 : real
```

### 3. Variável (Identificador)

```
x : T ∈ Γ
─────────────────────
Γ ⊢ x : T
```

**Exemplo:**
```
x : int ∈ Γ
─────────────────────
Γ ⊢ x : int
```

### 4. Adição de Inteiros

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
Γ ⊢ e₁ + e₂ : int
```

**Exemplo:**
```
Γ ⊢ 5 : int    Γ ⊢ 3 : int
───────────────────────────
Γ ⊢ 5 + 3 : int
```

### 5. Adição com Promoção de Tipo

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : real
─────────────────────────────────
Γ ⊢ e₁ + e₂ : real
```

Ou usando a função `promover_tipo`:

```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂
─────────────────────────────────────────
Γ ⊢ e₁ + e₂ : promover_tipo(T₁, T₂)
```

**Exemplo:**
```
Γ ⊢ 5 : int    Γ ⊢ 3.5 : real
──────────────────────────────────
Γ ⊢ 5 + 3.5 : real
```

### 6. Potenciação (Expoente Inteiro)

```
Γ ⊢ base : T    Γ ⊢ exp : int    T ∈ {int, real}
───────────────────────────────────────────────────
Γ ⊢ base ^ exp : T
```

**Regra de erro:**
```
Γ ⊢ base : T    Γ ⊢ exp : T'    T' ≠ int
───────────────────────────────────────────────────
Γ ⊢ base ^ exp : erro
    "Expoente deve ser inteiro, encontrado T'"
```

**Exemplo válido:**
```
Γ ⊢ 2 : int    Γ ⊢ -3 : int
─────────────────────────────
Γ ⊢ 2 ^ -3 : int
```

**Exemplo inválido:**
```
Γ ⊢ 2 : int    Γ ⊢ 3.5 : real
─────────────────────────────────────────
Γ ⊢ 2 ^ 3.5 : erro
    "Expoente deve ser inteiro"
```

### 7. Divisão Inteira

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    e₂ ≠ 0
─────────────────────────────────────────
Γ ⊢ e₁ / e₂ : int
```

**Regra de erro (tipo):**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    T₁ ≠ int ∨ T₂ ≠ int
───────────────────────────────────────────────────
Γ ⊢ e₁ / e₂ : erro
    "Divisão inteira requer operandos inteiros"
```

**Regra de erro (divisão por zero):**
```
Γ ⊢ e₁ : int    Γ ⊢ 0 : int
───────────────────────────────────────
Γ ⊢ e₁ / 0 : erro
    "Divisão por zero"
```

### 8. Divisão Real

```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    T₁, T₂ ∈ {int, real}
─────────────────────────────────────────────────────
Γ ⊢ e₁ | e₂ : promover_tipo(T₁, T₂)
```

### 9. Módulo

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    e₂ ≠ 0
─────────────────────────────────────────
Γ ⊢ e₁ % e₂ : int
```

### 10. Operadores Relacionais

```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    T₁, T₂ ∈ {int, real}    op ∈ {>, <, >=, <=, ==, !=}
──────────────────────────────────────────────────────────────────────────────────
Γ ⊢ e₁ op e₂ : booleano
```

**Exemplo:**
```
Γ ⊢ 5 : int    Γ ⊢ 3 : int
───────────────────────────
Γ ⊢ 5 > 3 : booleano
```

### 11. Declaração de Variável (MEM)

```
Γ ⊢ e : T    T ≠ booleano    x ∉ Γ
─────────────────────────────────────
Γ[x ↦ T] ⊢ (x : T ← e) : T
```

**Regra de erro:**
```
Γ ⊢ e : booleano
─────────────────────────────────────────────
Γ ⊢ (x : booleano ← e) : erro
    "Booleano não pode ser armazenado"
```

**Exemplo:**
```
Γ ⊢ 42 : int    x ∉ Γ
─────────────────────────────
Γ[x ↦ int] ⊢ (x : int ← 42) : int
```

### 12. Leitura de Variável

```
x : T ∈ Γ    Γ(x).inicializada = true
─────────────────────────────────────
Γ ⊢ x : T
```

**Regra de erro:**
```
x ∉ Γ
─────────────────────────────────────────
Γ ⊢ x : erro
    "Variável não declarada"
```

### 13. Comando RES

```
Γ ⊢ i : int    i ≥ 0    i < |resultados|    resultados[i] : T
──────────────────────────────────────────────────────────────
Γ ⊢ RES(i) : T
```

**Regras de erro:**
```
Γ ⊢ i : T    T ≠ int
──────────────────────────────────────
Γ ⊢ RES(i) : erro
    "Índice deve ser inteiro"

Γ ⊢ i : int    i < 0
──────────────────────────────────────
Γ ⊢ RES(i) : erro
    "Índice deve ser não-negativo"

Γ ⊢ i : int    i ≥ 0    i ≥ |resultados|
──────────────────────────────────────────
Γ ⊢ RES(i) : erro
    "Índice fora dos limites"
```

### 14. Estrutura Condicional (IF)

```
Γ ⊢ c : booleano    Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂
─────────────────────────────────────────────────
Γ ⊢ if c then e₁ else e₂ : promover_tipo(T₁, T₂)
```

**Regra de erro:**
```
Γ ⊢ c : T    T ≠ booleano
─────────────────────────────────────────
Γ ⊢ if c then e₁ else e₂ : erro
    "Condição deve ser booleana"
```

**Exemplo:**
```
Γ ⊢ (5 > 3) : booleano    Γ ⊢ 10 : int    Γ ⊢ 20 : int
──────────────────────────────────────────────────────────
Γ ⊢ if (5 > 3) then 10 else 20 : int
```

### 15. Estrutura de Repetição (WHILE)

```
Γ ⊢ c : booleano    Γ ⊢ e : T
─────────────────────────────────
Γ ⊢ while c do e : T
```

**Regra de erro:**
```
Γ ⊢ c : T    T ≠ booleano
─────────────────────────────────────────
Γ ⊢ while c do e : erro
    "Condição deve ser booleana"
```

### 16. Estrutura de Repetição (FOR)

```
Γ ⊢ init : T_init    Γ ⊢ cond : booleano    Γ ⊢ incr : T_incr    Γ ⊢ body : T_body
──────────────────────────────────────────────────────────────────────────────────
Γ ⊢ for init; cond; incr do body : T_body
```

---

## 📊 Tabela de Promoção de Tipos

A função `promover_tipo(T₁, T₂)` é definida pela seguinte tabela:

| T₁ | T₂ | promover_tipo(T₁, T₂) |
|----|----|-----------------------|
| int | int | int |
| int | real | real |
| real | int | real |
| real | real | real |
| booleano | booleano | booleano |
| erro | * | erro |
| * | erro | erro |

**Propriedades:**
- **Comutativa**: `promover_tipo(T₁, T₂) = promover_tipo(T₂, T₁)`
- **Monotônica**: Se `T₁ ⊑ T₂`, então `promover_tipo(T₁, T) ⊑ promover_tipo(T₂, T)`
- **Absorção de erro**: `promover_tipo(erro, T) = erro`

---

## 🔍 Tabela de Símbolos

### Estrutura

A tabela de símbolos Γ é um mapeamento:

```
Γ : Identificador → InfoSimbolo

InfoSimbolo ::= {
    tipo: Tipo,
    inicializada: Booleano,
    linha_declaracao: Inteiro
}
```

### Operações

#### Busca

```
buscar: Γ × Identificador → InfoSimbolo ∪ {∅}

buscar(Γ, x) = {
    Γ(x)  se x ∈ dom(Γ)
    ∅     caso contrário
}
```

#### Adição

```
adicionar: Γ × Identificador × Tipo × Linha → Γ'

Γ' = Γ[x ↦ {tipo: T, inicializada: true, linha_declaracao: l}]

Restrição: T ≠ booleano
```

#### Inicialização

```
inicializar: ∅ → Γ

inicializar() = {∅}
```

---

## ⚠️ Regras Semânticas de Erro

### Categoria 1: Erros de Tipo

| ID | Regra | Mensagem |
|----|-------|----------|
| E1 | Operação entre tipos incompatíveis | "Tipos incompatíveis: T₁ e T₂" |
| E2 | Expoente não-inteiro | "Expoente deve ser inteiro, encontrado T" |
| E3 | Operando não-inteiro para DIV_INT | "Divisão inteira requer operandos inteiros" |
| E4 | Operando não-inteiro para MOD | "Módulo requer operandos inteiros" |
| E5 | Condição não-booleana | "Condição deve ser booleana, encontrado T" |

### Categoria 2: Erros de Memória

| ID | Regra | Mensagem |
|----|-------|----------|
| M1 | Variável não declarada | "Variável 'x' não declarada" |
| M2 | Variável não inicializada | "Variável 'x' não foi inicializada" |
| M3 | Armazenamento de booleano | "Tipo booleano não pode ser armazenado" |

### Categoria 3: Erros de Operação

| ID | Regra | Mensagem |
|----|-------|----------|
| O1 | Divisão por zero | "Divisão por zero detectada" |
| O2 | Índice RES negativo | "Índice RES deve ser não-negativo" |
| O3 | Índice RES não-inteiro | "Índice RES deve ser inteiro" |
| O4 | Índice RES fora dos limites | "Índice RES fora dos limites (0..n-1)" |

---

## 📐 Exemplos Práticos

### Exemplo 1: Expressão Simples

**Código:**
```
5 3 +
```

**Derivação:**
```
Γ ⊢ 5 : int    Γ ⊢ 3 : int
───────────────────────────
Γ ⊢ 5 + 3 : int
```

### Exemplo 2: Promoção de Tipo

**Código:**
```
5 3.5 +
```

**Derivação:**
```
Γ ⊢ 5 : int    Γ ⊢ 3.5 : real
──────────────────────────────────
Γ ⊢ 5 + 3.5 : promover_tipo(int, real) = real
```

### Exemplo 3: Potenciação com Expoente Negativo

**Código:**
```
2 -3 ^
```

**Derivação:**
```
Γ ⊢ 2 : int    Γ ⊢ -3 : int
─────────────────────────────
Γ ⊢ 2 ^ -3 : int
```

### Exemplo 4: Erro de Tipo em Potenciação

**Código:**
```
2 3.5 ^
```

**Derivação:**
```
Γ ⊢ 2 : int    Γ ⊢ 3.5 : real    real ≠ int
──────────────────────────────────────────────
Γ ⊢ 2 ^ 3.5 : erro
    "Expoente deve ser inteiro, encontrado real"
```

### Exemplo 5: Estrutura Condicional

**Código:**
```
5 3 > (10 2 +) (20 2 +) IF
```

**Derivação:**
```
Γ ⊢ 5 : int    Γ ⊢ 3 : int
───────────────────────────────
Γ ⊢ (5 > 3) : booleano

Γ ⊢ 10 : int    Γ ⊢ 2 : int        Γ ⊢ 20 : int    Γ ⊢ 2 : int
───────────────────────────────    ───────────────────────────────
Γ ⊢ (10 + 2) : int                Γ ⊢ (20 + 2) : int

Γ ⊢ (5 > 3) : booleano    Γ ⊢ (10 + 2) : int    Γ ⊢ (20 + 2) : int
────────────────────────────────────────────────────────────────────
Γ ⊢ if (5 > 3) then (10 + 2) else (20 + 2) : int
```

### Exemplo 6: Declaração e Uso de Variável

**Código:**
```
42 x MEM
x 2 *
```

**Derivação:**
```
Γ₀ ⊢ 42 : int    x ∉ Γ₀
──────────────────────────────────
Γ₁ = Γ₀[x ↦ int] ⊢ (x : int ← 42) : int

x : int ∈ Γ₁    Γ₁ ⊢ 2 : int
────────────────────────────────
Γ₁ ⊢ x * 2 : int
```

---

## 🎓 Referências Teóricas

### Sistemas de Tipos

Esta gramática de atributos implementa um **sistema de tipos simples** com:
- Tipos primitivos (int, real, booleano)
- Promoção automática (subtyping)
- Verificação estática

### Notação Formal

Baseada em:
- **Dedução Natural**: para regras de inferência
- **Cálculo Lambda Tipado**: para função de promoção
- **Lógica de Hoare**: para semântica de comandos

---

## ✅ Conformidade com Especificação

Esta gramática implementa **100%** dos requisitos da Fase 3:

- [x] Gramática de atributos completa
- [x] Atributos sintetizados e herdados
- [x] Regras de produção formais
- [x] Notação matemática (Γ ⊢)
- [x] Tabela de símbolos
- [x] Promoção de tipos
- [x] Validação de operadores
- [x] Detecção de erros semânticos
- [x] Documentação em formato EBNF
- [x] Exemplos práticos

---

**Autores:** João Victor Roth, Mariana Trentiny Barbosa  
**Instituição:** PUCPR  
**Disciplina:** Linguagens Formais e Compiladores  
**Ano:** 2025
