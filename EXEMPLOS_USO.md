# Exemplos de Uso - Compilador RPN

## 📚 Guia Prático com Exemplos Completos

Este documento apresenta exemplos práticos de uso do compilador RPN, organizados por categoria e nível de complexidade.

---

## 🎯 Índice de Exemplos

1. [Operações Aritméticas Básicas](#1-operações-aritméticas-básicas)
2. [Promoção de Tipos](#2-promoção-de-tipos)
3. [Operadores Especiais](#3-operadores-especiais)
4. [Operadores Relacionais](#4-operadores-relacionais)
5. [Gerenciamento de Memória](#5-gerenciamento-de-memória)
6. [Estruturas de Controle](#6-estruturas-de-controle)
7. [Exemplos Complexos](#7-exemplos-complexos)
8. [Casos de Erro Comuns](#8-casos-de-erro-comuns)

---

## 1. Operações Aritméticas Básicas

### 1.1 Adição

**Exemplo 1: Adição de Inteiros**
```
Entrada: (5 3 +)
Tipo: int
Resultado: 8
```

**Exemplo 2: Adição de Reais**
```
Entrada: (5.5 3.2 +)
Tipo: real
Resultado: 8.7
```

### 1.2 Subtração

**Exemplo 3: Subtração Simples**
```
Entrada: (10 3 -)
Tipo: int
Resultado: 7
```

**Exemplo 4: Subtração com Negativos**
```
Entrada: (-5 -3 -)
Tipo: int
Resultado: -2
```

### 1.3 Multiplicação

**Exemplo 5: Multiplicação de Inteiros**
```
Entrada: (7 3 *)
Tipo: int
Resultado: 21
```

**Exemplo 6: Multiplicação de Reais**
```
Entrada: (2.5 4.0 *)
Tipo: real
Resultado: 10.0
```

### 1.4 Divisão

**Exemplo 7: Divisão Real**
```
Entrada: (10 3 |)
Tipo: int (ou real se operandos diferentes)
Resultado: 3.333...
```

**Exemplo 8: Divisão Inteira**
```
Entrada: (10 3 /)
Tipo: int
Resultado: 3
```

---

## 2. Promoção de Tipos

### 2.1 int + real → real

**Exemplo 9:**
```
Entrada: (5 3.5 +)
Análise:
  - 5 → int
  - 3.5 → real
  - promover_tipo(int, real) = real
Tipo Resultado: real
Valor: 8.5
```

**Exemplo 10:**
```
Entrada: (10 2.0 *)
Análise:
  - 10 → int
  - 2.0 → real
  - promover_tipo(int, real) = real
Tipo Resultado: real
Valor: 20.0
```

### 2.2 real + int → real

**Exemplo 11:**
```
Entrada: (3.14 2 +)
Análise:
  - 3.14 → real
  - 2 → int
  - promover_tipo(real, int) = real
Tipo Resultado: real
Valor: 5.14
```

---

## 3. Operadores Especiais

### 3.1 Potenciação (^)

**Exemplo 12: Potenciação Simples**
```
Entrada: (2 3 ^)
Análise: 2^3
Tipo: int
Resultado: 8
```

**Exemplo 13: Base Real**
```
Entrada: (2.5 2 ^)
Análise: 2.5^2
Tipo: real
Resultado: 6.25
```

**Exemplo 14: Expoente Negativo** ✨
```
Entrada: (2 -3 ^)
Análise: 2^-3 = 1/8
Tipo: int
Resultado: 0 (divisão inteira)
Nota: Expoentes negativos são permitidos!
```

**Exemplo 15: ERRO - Expoente Real**
```
Entrada: (2 3.5 ^)
Erro: ERRO SEMÂNTICO [Linha X]: Expoente deve ser inteiro, encontrado real
```

### 3.2 Divisão Inteira (/)

**Exemplo 16: Divisão Inteira Válida**
```
Entrada: (15 4 /)
Análise: 15 ÷ 4
Tipo: int
Resultado: 3
```

**Exemplo 17: ERRO - Operando Real**
```
Entrada: (15.5 4 /)
Erro: ERRO SEMÂNTICO: Divisão inteira requer operandos inteiros
```

### 3.3 Módulo (%)

**Exemplo 18: Módulo Válido**
```
Entrada: (10 3 %)
Análise: 10 mod 3
Tipo: int
Resultado: 1
```

**Exemplo 19: ERRO - Operando Real**
```
Entrada: (10.5 3 %)
Erro: ERRO SEMÂNTICO: Módulo requer operandos inteiros
```

---

## 4. Operadores Relacionais

### 4.1 Comparações Básicas

**Exemplo 20: Maior que**
```
Entrada: (5 3 >)
Análise: 5 > 3
Tipo: booleano
Resultado: true
```

**Exemplo 21: Menor que**
```
Entrada: (5 10 <)
Análise: 5 < 10
Tipo: booleano
Resultado: true
```

**Exemplo 22: Igual**
```
Entrada: (5 5 ==)
Análise: 5 == 5
Tipo: booleano
Resultado: true
```

**Exemplo 23: Diferente**
```
Entrada: (5 3 !=)
Análise: 5 != 3
Tipo: booleano
Resultado: true
```

### 4.2 Comparações com Tipos Diferentes

**Exemplo 24: Comparação int vs real**
```
Entrada: (5 3.5 >)
Análise: 5 > 3.5
Tipo: booleano
Resultado: true
```

---

## 5. Gerenciamento de Memória

### 5.1 Declaração de Variáveis (MEM)

**Exemplo 25: Armazenar Inteiro**
```
Entrada: (42 x MEM)
Análise: x = 42
Tipo: int
Efeito: Adiciona x : int à tabela de símbolos
```

**Exemplo 26: Armazenar Real**
```
Entrada: (3.14 pi MEM)
Análise: pi = 3.14
Tipo: real
Efeito: Adiciona pi : real à tabela de símbolos
```

**Exemplo 27: ERRO - Armazenar Booleano**
```
Entrada: (5 3 > resultado MEM)
Análise:
  Linha 1: (5 3 >) → booleano
  Linha 2: Tenta armazenar booleano
Erro: ERRO SEMÂNTICO: Tipo booleano não pode ser armazenado
```

### 5.2 Uso de Variáveis

**Exemplo 28: Leitura Simples**
```
Entrada:
  Linha 1: (10 x MEM)
  Linha 2: (x 2 *)
Análise:
  Linha 1: x = 10
  Linha 2: x * 2 = 20
Tipo Linha 2: int
```

**Exemplo 29: Múltiplas Variáveis**
```
Entrada:
  (5 a MEM)
  (3 b MEM)
  (a b +)
Análise:
  a = 5
  b = 3
  a + b = 8
```

**Exemplo 30: ERRO - Variável Não Declarada**
```
Entrada: (y 2 *)
Erro: ERRO SEMÂNTICO: Variável 'y' não declarada
```

### 5.3 Comando RES

**Exemplo 31: Recuperar Resultado Anterior**
```
Entrada:
  Linha 0: (5 3 +)      # Resultado: 8
  Linha 1: (0 RES 2 *)  # Recupera linha 0: 8 * 2 = 16
Tipo: int
```

**Exemplo 32: ERRO - Índice Negativo**
```
Entrada: (-1 RES)
Erro: ERRO SEMÂNTICO: Índice RES deve ser não-negativo
```

**Exemplo 33: ERRO - Índice Não-Inteiro**
```
Entrada: (2.5 RES)
Erro: ERRO SEMÂNTICO: Índice RES deve ser inteiro
```

---

## 6. Estruturas de Controle

### 6.1 IF (Condicional)

**Exemplo 34: IF Simples**
```
Entrada: ((5 3 >) (10) (20) IF)
Análise:
  Condição: 5 > 3 → true
  Then: 10
  Else: 20
  Como condição é true, retorna 10
Tipo: int
Resultado: 10
```

**Exemplo 35: IF com Expressões**
```
Entrada: ((10 5 >) (100 2 *) (50 2 /) IF)
Análise:
  Condição: 10 > 5 → true
  Then: 100 * 2 = 200
  Else: 50 / 2 = 25
Tipo: int
Resultado: 200
```

**Exemplo 36: IF com Promoção de Tipos**
```
Entrada: ((5 3 >) (10) (3.5) IF)
Análise:
  Condição: booleano ✓
  Then: int
  Else: real
  Tipo: promover_tipo(int, real) = real
Tipo: real
```

**Exemplo 37: ERRO - Condição Não-Booleana**
```
Entrada: (5 (10) (20) IF)
Análise:
  Condição: 5 → int (não é booleano!)
Erro: ERRO SEMÂNTICO: Condição de IF deve ser booleana
```

### 6.2 WHILE (Loop)

**Exemplo 38: WHILE Simples**
```
Entrada:
  (0 i MEM)
  ((i 5 <) (i 1 + i MEM) WHILE)
Análise:
  i = 0
  while (i < 5) { i = i + 1 }
  Resultado final: i = 5
Tipo: int
```

**Exemplo 39: ERRO - Condição Não-Booleana**
```
Entrada: (5 (x 1 + x MEM) WHILE)
Erro: ERRO SEMÂNTICO: Condição de WHILE deve ser booleana
```

### 6.3 FOR (Loop Iterativo)

**Exemplo 40: FOR Contador**
```
Entrada:
  ((0 i MEM) (i 10 <) (i 1 + i MEM) (i i *) FOR)
Análise:
  for (i=0; i<10; i++) { return i*i }
  Retorna quadrados: 0, 1, 4, 9, ..., 81
Tipo: int
```

### 6.4 IF Aninhado

**Exemplo 41: IF Aninhado**
```
Entrada:
  ((x 0 >) 
    ((x 10 <) (1) (0) IF) 
    (-1) 
  IF)
Análise:
  if (x > 0)
    if (x < 10) return 1
    else return 0
  else
    return -1
Tipo: int
```

---

## 7. Exemplos Complexos

### 7.1 Cálculo de Fatorial (Iterativo)

```
# Fatorial de 5
(5 n MEM)
(1 result MEM)
(1 i MEM)
((i n <=) (result i * result MEM i 1 + i MEM) WHILE)
(result)
# Resultado: 120
```

### 7.2 Sequência de Fibonacci

```
# Primeiros 10 números de Fibonacci
(0 a MEM)
(1 b MEM)
(0 count MEM)
((count 10 <) (
  (a b + temp MEM)
  (b a MEM)
  (temp b MEM)
  (count 1 + count MEM)
) WHILE)
(b)
```

### 7.3 Média Aritmética

```
# Média de três números
(10 a MEM)
(20 b MEM)
(30 c MEM)
(a b + c + 3 |)  # (10+20+30)/3 = 20.0
```

### 7.4 Máximo de Dois Números

```
# max(a, b)
(15 a MEM)
(20 b MEM)
((a b >) (a) (b) IF)
# Resultado: 20
```

### 7.5 Verificação de Paridade

```
# Verifica se número é par
(42 num MEM)
((num 2 % 0 ==) (1) (0) IF)  # 1 se par, 0 se ímpar
# Resultado: 1 (42 é par)
```

### 7.6 Cálculo de Área

```
# Área de círculo: πr²
(3.14159 pi MEM)
(5 raio MEM)
(pi raio raio * *)
# Resultado: 78.53975
```

### 7.7 Conversão de Temperatura

```
# Celsius para Fahrenheit: F = C * 9/5 + 32
(25 celsius MEM)
(celsius 9 * 5 | 32 +)
# Resultado: 77.0
```

---

## 8. Casos de Erro Comuns

### 8.1 Erros de Tipo

**Erro 1: Expoente Real**
```
❌ (2 3.5 ^)
✅ (2 3 ^)
```

**Erro 2: Divisão Inteira com Real**
```
❌ (10.5 2 /)
✅ (10 2 /)    # ou
✅ (10.5 2 |)  # divisão real
```

**Erro 3: Módulo com Real**
```
❌ (10.5 3 %)
✅ (10 3 %)
```

### 8.2 Erros de Memória

**Erro 4: Variável Não Declarada**
```
❌ (x 2 *)
✅ (10 x MEM)  # Primeiro declare
   (x 2 *)     # Depois use
```

**Erro 5: Booleano em Memória**
```
❌ (5 3 > resultado MEM)
✅ (5 3 + resultado MEM)  # Armazene valor numérico
```

### 8.3 Erros de Operação

**Erro 6: Divisão por Zero**
```
❌ (10 0 /)
✅ (10 2 /)
```

**Erro 7: RES com Índice Inválido**
```
❌ (-1 RES)
✅ (0 RES)   # Índice não-negativo
```

### 8.4 Erros de Estrutura de Controle

**Erro 8: Condição Não-Booleana em IF**
```
❌ (5 (10) (20) IF)
✅ ((5 3 >) (10) (20) IF)
```

**Erro 9: Condição Não-Booleana em WHILE**
```
❌ (5 (x 1 + x MEM) WHILE)
✅ ((x 5 <) (x 1 + x MEM) WHILE)
```

---

## 📊 Resumo de Padrões

### Padrões Válidos

```
✅ Operações aritméticas básicas
   (a b +) (a b -) (a b *) (a b |)

✅ Divisão e módulo inteiros
   (a b /)  # ambos int
   (a b %)  # ambos int

✅ Potenciação
   (a b ^)  # b deve ser int (pode ser negativo)

✅ Comparações
   (a b >) (a b <) (a b >=) (a b <=) (a b ==) (a b !=)

✅ Memória
   (valor nome MEM)  # valor não pode ser booleano
   (nome)            # nome deve estar declarado

✅ Estruturas
   ((cond) (then) (else) IF)  # cond deve ser booleano
   ((cond) (body) WHILE)      # cond deve ser booleano
   ((init) (cond) (incr) (body) FOR)  # cond deve ser booleano
```

---

## 🎓 Exercícios Propostos

### Nível Iniciante

1. Calcule a soma de 10 e 20
2. Calcule o quadrado de 7
3. Verifique se 15 é maior que 10
4. Armazene o valor 100 em uma variável `total`

### Nível Intermediário

5. Calcule a média de três números: 10, 20, 30
6. Encontre o máximo entre dois números usando IF
7. Calcule o fatorial de 5 iterativamente
8. Conte de 0 a 10 usando WHILE

### Nível Avançado

9. Implemente uma função para verificar se um número é primo
10. Calcule a sequência de Fibonacci até o 15º termo
11. Converta temperaturas de Celsius para Fahrenheit e Kelvin
12. Calcule a potência de 2^n para n de 0 a 10

---

## 📖 Soluções dos Exercícios

### Nível Iniciante

**1. Soma:**
```
(10 20 +)  # 30
```

**2. Quadrado:**
```
(7 7 *)    # 49
```

**3. Comparação:**
```
(15 10 >)  # true
```

**4. Armazenamento:**
```
(100 total MEM)
```

### Nível Intermediário

**5. Média:**
```
(10 20 + 30 + 3 |)  # 20.0
```

**6. Máximo:**
```
(15 a MEM)
(20 b MEM)
((a b >) (a) (b) IF)  # 20
```

### Nível Avançado

Soluções disponíveis na documentação completa do projeto.

---

## 🔗 Recursos Adicionais

- **MANUAL_USUARIO.md**: Guia completo de uso
- **GRAMATICA_ATRIBUTOS.md**: Regras formais
- **REGRAS_DEDUCAO.md**: Exemplos de inferência de tipos
- **DOCUMENTACAO_ESTRUTURAS.md**: Estruturas de controle

---

## 📞 Suporte

Para mais exemplos ou dúvidas:
1. Consulte os arquivos de teste: `teste1.txt`, `teste2.txt`, `teste3.txt`
2. Execute o compilador com os exemplos fornecidos
3. Revise a documentação completa

---

**Compilador:** RPN v3.0  
**Autores:** João Victor Roth, Mariana Trentiny Barbosa  
**Instituição:** PUCPR  
**Ano:** 2025
