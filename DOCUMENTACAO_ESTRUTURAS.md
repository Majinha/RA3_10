# Documentação das Estruturas de Controle

## 📋 Visão Geral

Este documento descreve a sintaxe, semântica e validações das **estruturas de controle** implementadas no compilador RPN: IF, WHILE e FOR.

---

## 🔀 Estrutura Condicional: IF

### Sintaxe EBNF

```ebnf
if ::= condicao expressao_then expressao_else "IF"

condicao ::= expressao    (* Deve resultar em tipo booleano *)
expressao_then ::= expressao
expressao_else ::= expressao
```

### Sintaxe RPN

```
(condicao) (expressao_then) (expressao_else) IF
```

### Estrutura da AST

```
NoAST {
    tipo_no: "ESTRUTURA_IF"
    filhos: [
        condicao: NoAST,         // Filho 0
        expressao_then: NoAST,   // Filho 1
        expressao_else: NoAST    // Filho 2
    ]
    tipo_dado: <tipo_resultado>
}
```

### Semântica

O comando IF avalia:
1. A **condição** primeiro
2. Se a condição é **verdadeira**: executa e retorna `expressao_then`
3. Se a condição é **falsa**: executa e retorna `expressao_else`

### Regras de Tipo

#### Regra Principal
```
Γ ⊢ c : booleano    Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂
─────────────────────────────────────────────────
Γ ⊢ if c then e₁ else e₂ : promover_tipo(T₁, T₂)
```

#### Validações

1. **Condição deve ser booleana**
   ```
   Γ ⊢ c : T    T ≠ booleano
   ─────────────────────────────────
   Erro: "Condição de IF deve ser booleana"
   ```

2. **Tipo do resultado**
   - Se `T₁ = T₂`: resultado tem tipo `T₁`
   - Se `T₁ ≠ T₂`: resultado tem tipo `promover_tipo(T₁, T₂)`

### Exemplos

#### Exemplo 1: IF Simples com Inteiros

**Código:**
```
5 3 > (10 2 +) (20 2 +) IF
```

**Tradução:**
```
if (5 > 3) then (10 + 2) else (20 + 2)
```

**Derivação de Tipos:**
```
Γ ⊢ (5 > 3) : booleano    
Γ ⊢ (10 + 2) : int    
Γ ⊢ (20 + 2) : int
────────────────────────────────────
Γ ⊢ IF : int
```

**Resultado:** 12 (pois 5 > 3 é verdadeiro)

#### Exemplo 2: IF com Promoção de Tipo

**Código:**
```
10 5 >= (100) (3.14) IF
```

**Tradução:**
```
if (10 >= 5) then 100 else 3.14
```

**Derivação:**
```
Γ ⊢ (10 >= 5) : booleano    
Γ ⊢ 100 : int    
Γ ⊢ 3.14 : real
────────────────────────────────────
Γ ⊢ IF : promover_tipo(int, real) = real
```

**Resultado:** 100.0 (convertido para real)

#### Exemplo 3: IF Aninhado

**Código:**
```
x 0 > (x 10 < (1) (0) IF) (-1) IF
```

**Tradução:**
```
if (x > 0) then
    if (x < 10) then 1 else 0
else
    -1
```

**Análise:**
```
Condição externa: x > 0 → booleano ✓
Ramo then: IF interno
    Condição interna: x < 10 → booleano ✓
    Then: 1 → int ✓
    Else: 0 → int ✓
    Resultado: int
Ramo else: -1 → int ✓
Resultado final: int ✓
```

#### Exemplo 4: Erro - Condição Não-Booleana

**Código:**
```
5 (10) (20) IF
```

**Erro:**
```
ERRO SEMÂNTICO [Linha X]: Condição de IF deve ser booleana, encontrado int
Contexto: (5 (10) (20) IF)
```

---

## 🔄 Estrutura de Repetição: WHILE

### Sintaxe EBNF

```ebnf
while ::= condicao corpo "WHILE"

condicao ::= expressao    (* Deve resultar em tipo booleano *)
corpo ::= expressao
```

### Sintaxe RPN

```
(condicao) (corpo) WHILE
```

### Estrutura da AST

```
NoAST {
    tipo_no: "ESTRUTURA_WHILE"
    filhos: [
        condicao: NoAST,    // Filho 0
        corpo: NoAST        // Filho 1
    ]
    tipo_dado: <tipo_corpo>
}
```

### Semântica

O comando WHILE:
1. Avalia a **condição**
2. Se **verdadeira**: executa o corpo e repete o passo 1
3. Se **falsa**: termina e retorna o último valor do corpo
4. Retorna o tipo do corpo

### Regras de Tipo

#### Regra Principal
```
Γ ⊢ c : booleano    Γ ⊢ e : T
─────────────────────────────────
Γ ⊢ while c do e : T
```

#### Validações

1. **Condição deve ser booleana**
   ```
   Γ ⊢ c : T    T ≠ booleano
   ─────────────────────────────────
   Erro: "Condição de WHILE deve ser booleana"
   ```

2. **Tipo do resultado**: igual ao tipo do corpo

### Exemplos

#### Exemplo 1: WHILE Simples

**Código:**
```
0 i MEM
(i 10 <) (i 1 + i MEM) WHILE
```

**Tradução:**
```
i = 0
while (i < 10) do
    i = i + 1
```

**Análise:**
```
Linha 1: 
    Γ ⊢ 0 : int
    Γ₁ = Γ[i ↦ int]

Linha 2:
    Γ₁ ⊢ (i < 10) : booleano ✓
    Γ₁ ⊢ (i + 1) : int
    Γ₁ ⊢ ((i + 1) i MEM) : int ✓
    ────────────────────────────────
    Γ₁ ⊢ WHILE : int
```

#### Exemplo 2: WHILE com Condição Complexa

**Código:**
```
100 sum MEM
0 i MEM
(i 5 <) (sum 10 >=) (sum i + sum MEM i 1 + i MEM) WHILE
```

**Tradução:**
```
sum = 100
i = 0
while (i < 5 && sum >= 10) do {
    sum = sum + i
    i = i + 1
}
```

#### Exemplo 3: Erro - Condição Não-Booleana

**Código:**
```
(5) (i 1 + i MEM) WHILE
```

**Erro:**
```
ERRO SEMÂNTICO [Linha X]: Condição de WHILE deve ser booleana, encontrado int
```

---

## 🔢 Estrutura de Repetição: FOR

### Sintaxe EBNF

```ebnf
for ::= inicializacao condicao incremento corpo "FOR"

inicializacao ::= expressao
condicao ::= expressao    (* Deve resultar em tipo booleano *)
incremento ::= expressao
corpo ::= expressao
```

### Sintaxe RPN

```
(inicializacao) (condicao) (incremento) (corpo) FOR
```

### Estrutura da AST

```
NoAST {
    tipo_no: "ESTRUTURA_FOR"
    filhos: [
        inicializacao: NoAST,    // Filho 0
        condicao: NoAST,         // Filho 1
        incremento: NoAST,       // Filho 2
        corpo: NoAST             // Filho 3
    ]
    tipo_dado: <tipo_corpo>
}
```

### Semântica

O comando FOR:
1. Executa **inicialização** uma vez
2. Avalia **condição**
3. Se **verdadeira**:
   - Executa **corpo**
   - Executa **incremento**
   - Volta ao passo 2
4. Se **falsa**: termina e retorna último valor do corpo

### Regras de Tipo

#### Regra Principal
```
Γ ⊢ init : T_i    Γ ⊢ cond : booleano    Γ ⊢ incr : T_incr    Γ ⊢ body : T_b
──────────────────────────────────────────────────────────────────────────────
Γ ⊢ for init; cond; incr do body : T_b
```

#### Validações

1. **Condição deve ser booleana**
   ```
   Γ ⊢ cond : T    T ≠ booleano
   ─────────────────────────────────
   Erro: "Condição de FOR deve ser booleana"
   ```

2. **Tipo do resultado**: igual ao tipo do corpo

### Exemplos

#### Exemplo 1: FOR Simples

**Código:**
```
(0 i MEM) (i 10 <) (i 1 + i MEM) (i i *) FOR
```

**Tradução:**
```
for (i = 0; i < 10; i = i + 1) {
    return i * i
}
```

**Análise:**
```
Inicialização: (0 i MEM)
    Γ ⊢ 0 : int
    Γ₁ = Γ[i ↦ int]

Condição: (i 10 <)
    Γ₁ ⊢ (i < 10) : booleano ✓

Incremento: (i 1 + i MEM)
    Γ₁ ⊢ (i + 1) : int
    Γ₁ ⊢ MEM : int ✓

Corpo: (i i *)
    Γ₁ ⊢ (i * i) : int ✓

Resultado: int
```

#### Exemplo 2: FOR com Acumulador

**Código:**
```
(0 sum MEM 1 i MEM) (i 10 <=) (i 1 + i MEM) (sum i + sum MEM) FOR
```

**Tradução:**
```
for (sum = 0, i = 1; i <= 10; i = i + 1) {
    sum = sum + i
}
```

#### Exemplo 3: FOR com Expressões Complexas

**Código:**
```
(1 fib1 MEM 1 fib2 MEM 0 i MEM) 
(i 10 <) 
(fib2 fib1 MEM fib1 fib2 + fib2 MEM i 1 + i MEM) 
(fib2) 
FOR
```

**Tradução:**
```
for (fib1 = 1, fib2 = 1, i = 0; i < 10; 
     fib1 = fib2, fib2 = fib1 + fib2, i = i + 1) {
    return fib2
}
```

#### Exemplo 4: Erro - Condição Não-Booleana

**Código:**
```
(0 i MEM) (10) (i 1 + i MEM) (i) FOR
```

**Erro:**
```
ERRO SEMÂNTICO [Linha X]: Condição de FOR deve ser booleana, encontrado int
```

---

## 🎯 Comparação das Estruturas

| Aspecto | IF | WHILE | FOR |
|---------|-----|-------|-----|
| **Número de partes** | 3 | 2 | 4 |
| **Condição obrigatória** | Sim (booleana) | Sim (booleana) | Sim (booleana) |
| **Tipo do resultado** | Promoção dos ramos | Tipo do corpo | Tipo do corpo |
| **Execução** | Única vez | Múltiplas (loop) | Múltiplas (loop) |
| **Inicialização** | Não tem | Não tem | Tem |
| **Incremento** | Não tem | Não tem | Tem |

---

## 📝 Regras Semânticas Comuns

### 1. Validação de Condição Booleana

Todas as estruturas validam que a condição resulta em tipo `booleano`:

```python
def validar_condicao_booleana(condicao: NoAST, estrutura: str, 
                               linha: int, erros: List):
    if condicao.tipo_dado != "booleano":
        erros.append({
            "linha": linha,
            "tipo": "ERRO_SEMANTICO",
            "mensagem": f"ERRO SEMÂNTICO [Linha {linha}]: "
                       f"Condição de {estrutura} deve ser booleana, "
                       f"encontrado {condicao.tipo_dado}",
            "contexto": condicao.contexto
        })
        return False
    return True
```

### 2. Análise Recursiva

Todas as estruturas analisam suas sub-expressões recursivamente:

```python
def analisar_estrutura(no: NoAST, gramatica: Dict, 
                       tabela: Dict, linha: int, erros: List):
    # Analisa cada filho
    for i, filho in enumerate(no.filhos):
        if filho.tipo_no in ["EXPRESSAO", "ESTRUTURA_IF", ...]:
            no.filhos[i] = analisarSemantica(
                filho, gramatica, tabela, linha, erros
            )
    
    # Valida condição
    if not validar_condicao_booleana(condicao, nome_estrutura, linha, erros):
        no.tipo_dado = "erro"
        return no
    
    # Define tipo do resultado
    no.tipo_dado = inferir_tipo_resultado(no)
    return no
```

---

## 🔬 Casos de Teste

### Teste 1: IF Básico
```
# Entrada
5 3 > (10) (20) IF

# Esperado
Tipo: int
Valor: 10
```

### Teste 2: WHILE Contador
```
# Entrada
0 count MEM
(count 5 <) (count 1 + count MEM) WHILE

# Esperado
Tipo: int
Tabela: {count: {tipo: int, valor_final: 5}}
```

### Teste 3: FOR Soma
```
# Entrada
(0 sum MEM) (sum 100 <) (sum 10 + sum MEM) (sum) FOR

# Esperado
Tipo: int
Valor final: 100
```

### Teste 4: IF Aninhado
```
# Entrada
x 0 == (0) (x 0 > (1) (-1) IF) IF

# Esperado
Tipo: int
Lógica: retorna 0 se x==0, 1 se x>0, -1 se x<0
```

### Teste 5: Erro - Condição Inválida
```
# Entrada
5 (10) (20) IF

# Esperado
ERRO: Condição de IF deve ser booleana, encontrado int
```

---

## 🎨 Visualização da AST

### Exemplo: `5 3 > (10 2 +) (20 2 +) IF`

```
ESTRUTURA_IF [tipo: int]
├── EXPRESSAO [tipo: booleano]
│   ├── OPERANDO [tipo: int, valor: 5]
│   ├── OPERANDO [tipo: int, valor: 3]
│   └── OPERADOR [tipo: >, retorno: booleano]
├── EXPRESSAO [tipo: int]
│   ├── OPERANDO [tipo: int, valor: 10]
│   ├── OPERANDO [tipo: int, valor: 2]
│   └── OPERADOR [tipo: +]
└── EXPRESSAO [tipo: int]
    ├── OPERANDO [tipo: int, valor: 20]
    ├── OPERANDO [tipo: int, valor: 2]
    └── OPERADOR [tipo: +]
```

---

## 📚 Exemplos Avançados

### Exemplo 1: Fatorial Iterativo

```
# Fatorial de n usando FOR
(n input MEM) 
(1 result MEM 1 i MEM) 
(i n <=) 
(result i * result MEM i 1 + i MEM) 
(result) 
FOR
```

### Exemplo 2: Fibonacci com WHILE

```
# n-ésimo número de Fibonacci
(n input MEM)
(0 a MEM 1 b MEM 0 count MEM)
(count n <) (
    a b + temp MEM
    b a MEM
    temp b MEM
    count 1 + count MEM
) WHILE
b
```

### Exemplo 3: Busca Binária Simplificada

```
# Verificação se elemento existe (simplificado)
(0 left MEM 10 right MEM 5 target MEM 0 found MEM)
(left right <=) (found 0 ==) (
    left right + 2 / mid MEM
    mid target == (1 found MEM) (
        mid target < (mid 1 + left MEM) (mid 1 - right MEM) IF
    ) IF
) WHILE
found
```

---

## ✅ Checklist de Validação

Para cada estrutura de controle, o compilador verifica:

### IF
- [ ] Condição é booleana
- [ ] Ramo then é válido
- [ ] Ramo else é válido
- [ ] Tipos são compatíveis ou promovíveis
- [ ] Contexto correto nas mensagens de erro

### WHILE
- [ ] Condição é booleana
- [ ] Corpo é válido
- [ ] Variáveis usadas estão declaradas
- [ ] Tipo do resultado é consistente

### FOR
- [ ] Inicialização é válida
- [ ] Condição é booleana
- [ ] Incremento é válido
- [ ] Corpo é válido
- [ ] Sequência de execução é correta

---

## 🔗 Integração com Outras Fases

### Fase 1 (Léxica)
- Reconhece tokens: `IF`, `WHILE`, `FOR`
- Identifica parênteses para delimitar partes

### Fase 2 (Sintática)
- Constrói AST com nós específicos
- Valida estrutura sintática
- Garante número correto de filhos

### Fase 3 (Semântica) ⭐
- Valida tipos das condições
- Verifica compatibilidade de tipos
- Detecta erros semânticos
- Anota tipos na AST

---

## 📖 Referências

- **Notação Polonesa Reversa**: Para sintaxe base
- **Estruturas de Controle Imperativas**: Para semântica
- **Type Systems**: Para validação de tipos
- **Compiladores Modernos**: Para implementação

---

**Autores:** João Victor Roth, Mariana Trentiny Barbosa  
**Instituição:** PUCPR  
**Disciplina:** Linguagens Formais e Compiladores  
**Ano:** 2025
