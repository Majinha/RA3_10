# Manual do Usuário - Compilador RPN

## 📖 Guia Completo de Uso

---

## 🎯 Visão Geral

Este manual descreve como usar o **Compilador RPN** (Reverse Polish Notation) com análise semântica completa. O compilador processa código em notação polonesa reversa, valida tipos, gerencia memória e estruturas de controle.

---

## 🚀 Começando

### Instalação

**Requisitos:**
- Python 3.8 ou superior
- Nenhuma biblioteca externa necessária

**Download:**
```bash
git clone [URL_DO_REPOSITORIO]
cd compilador-rpn
```

### Verificação da Instalação

```bash
python compilador_final_corrigido.py --help
```

---

## 📝 Sintaxe da Linguagem

### Notação Polonesa Reversa (RPN)

Na RPN, os operadores vêm **após** os operandos:

| Notação Infixa | Notação RPN | Significado |
|----------------|-------------|-------------|
| `5 + 3` | `5 3 +` | Soma |
| `10 - 2` | `10 2 -` | Subtração |
| `7 * 3` | `7 3 *` | Multiplicação |
| `(5 + 3) * 2` | `5 3 + 2 *` | Precedência |

### Tipos de Dados

1. **int** (Inteiro)
   - Números sem ponto decimal
   - Exemplos: `5`, `-3`, `42`, `0`

2. **real** (Real/Float)
   - Números com ponto decimal
   - Exemplos: `3.14`, `-0.5`, `2.0`

3. **booleano**
   - Resultado de comparações
   - Valores lógicos: verdadeiro/falso

---

## 🔧 Operadores

### Aritméticos

| Operador | Símbolo | Exemplo RPN | Resultado | Restrições |
|----------|---------|-------------|-----------|------------|
| Adição | `+` | `5 3 +` | 8 | Promove tipos |
| Subtração | `-` | `10 2 -` | 8 | Promove tipos |
| Multiplicação | `*` | `7 3 *` | 21 | Promove tipos |
| Divisão real | `\|` | `10 3 \|` | 3.333... | Promove tipos |
| Divisão inteira | `/` | `10 3 /` | 3 | Apenas int |
| Módulo | `%` | `10 3 %` | 1 | Apenas int |
| Potenciação | `^` | `2 3 ^` | 8 | Expoente int (pode ser negativo) |

### Relacionais

| Operador | Símbolo | Exemplo RPN | Resultado | Tipo Retorno |
|----------|---------|-------------|-----------|--------------|
| Maior que | `>` | `5 3 >` | verdadeiro | booleano |
| Menor que | `<` | `5 3 <` | falso | booleano |
| Maior ou igual | `>=` | `5 5 >=` | verdadeiro | booleano |
| Menor ou igual | `<=` | `3 5 <=` | verdadeiro | booleano |
| Igual | `==` | `5 5 ==` | verdadeiro | booleano |
| Diferente | `!=` | `5 3 !=` | verdadeiro | booleano |

---

## 💾 Gerenciamento de Memória

### Comando MEM (Armazenar)

**Sintaxe:** `<valor> <nome_variavel> MEM`

**Exemplo:**
```
42 x MEM        # x = 42
3.14 pi MEM     # pi = 3.14
```

**Restrições:**
- ❌ Não pode armazenar valores booleanos
- ✅ Aceita int e real

**Erro comum:**
```
5 3 > resultado MEM    # ❌ ERRO: booleano não pode ser armazenado
```

### Leitura de Variável

**Sintaxe:** `<nome_variavel>`

**Exemplo:**
```
42 x MEM        # Declara x = 42
x 2 *           # Usa x: x * 2 = 84
```

**Validações:**
- ✅ Variável deve estar declarada antes do uso
- ✅ Variável deve estar inicializada

### Comando RES (Recuperar Resultado)

**Sintaxe:** `<indice> RES`

Recupera o resultado de uma linha anterior (índice começa em 0).

**Exemplo:**
```
# Linha 0
5 3 +           # Resultado: 8

# Linha 1
0 RES 2 *       # Recupera linha 0: 8 * 2 = 16
```

**Restrições:**
- Índice deve ser **inteiro**
- Índice deve ser **não-negativo**
- Índice deve ser **válido** (< número de linhas anteriores)

---

## 🎛️ Estruturas de Controle

### IF (Condicional)

**Sintaxe:** `(<condicao>) (<ramo_then>) (<ramo_else>) IF`

**Exemplo:**
```
5 3 > (10) (20) IF
# Se 5 > 3 então 10, senão 20
# Resultado: 10
```

**Com Expressões:**
```
x 0 > (x 2 *) (x 2 /) IF
# Se x > 0 então x*2, senão x/2
```

**Validações:**
- Condição **deve ser booleana**
- Ramos podem ter tipos diferentes (haverá promoção)

### WHILE (Loop Condicional)

**Sintaxe:** `(<condicao>) (<corpo>) WHILE`

**Exemplo:**
```
0 i MEM
(i 10 <) (i 1 + i MEM) WHILE
# while (i < 10) { i = i + 1 }
```

**Validações:**
- Condição **deve ser booleana**
- Corpo é executado enquanto condição for verdadeira

### FOR (Loop Iterativo)

**Sintaxe:** `(<init>) (<condicao>) (<incremento>) (<corpo>) FOR`

**Exemplo:**
```
(0 i MEM) (i 10 <) (i 1 + i MEM) (i i *) FOR
# for(i=0; i<10; i++) { return i*i }
```

**Validações:**
- Condição **deve ser booleana**
- Todas as partes são expressões válidas

---

## 📊 Promoção de Tipos

### Regras Automáticas

| Operação | Tipo Resultado |
|----------|---------------|
| `int + int` | int |
| `int + real` | real |
| `real + int` | real |
| `real + real` | real |

**Exemplo:**
```
5 3 +      # int + int = int → 8
5 3.0 +    # int + real = real → 8.0
5.5 2.5 +  # real + real = real → 8.0
```

---

## 💻 Uso do Compilador

### Execução Básica

```bash
python compilador_final_corrigido.py <arquivo.txt>
```

### Exemplo Completo

**1. Criar arquivo de teste (`meu_codigo.txt`):**
```
# Operações básicas
5 3 +
10 2 -
7 3 *

# Uso de memória
42 x MEM
x 2 *

# Estrutura condicional
5 3 > (100) (200) IF
```

**2. Executar:**
```bash
python compilador_final_corrigido.py meu_codigo.txt
```

**3. Saída esperada:**
```
============================================================
Processando linha 1: 5 3 +
============================================================

✅ Análise bem-sucedida
   Tipo inferido: int

============================================================
Processando linha 2: 10 2 -
============================================================

✅ Análise bem-sucedida
   Tipo inferido: int

...

============================================================
RELATÓRIO FINAL
============================================================
Total de linhas processadas: 6
Total de erros: 0

📊 TABELA DE SÍMBOLOS FINAL:
  • x: int (linha 4)

📁 Resultados salvos em: analise_semantica_20250106_143000.json
📝 Gerando relatório em Markdown...
✅ Relatório Markdown gerado: analise_semantica_20250106_143000.md
```

---

## 📁 Arquivos Gerados

### JSON (`analise_semantica_TIMESTAMP.json`)

Contém análise completa estruturada:
```json
{
  "metadata": {
    "arquivo_fonte": "meu_codigo.txt",
    "data_compilacao": "06/01/2025 14:30:00",
    "total_linhas": 6,
    "total_erros": 0
  },
  "tabela_simbolos": {
    "x": {
      "tipo": "int",
      "inicializada": true,
      "linha_declaracao": 4
    }
  },
  "erros_semanticos": [],
  "arvores_sintaticas": [...]
}
```

### Markdown (`analise_semantica_TIMESTAMP.md`)

Relatório visual legível com:
- Tabela de símbolos formatada
- Erros com contexto
- Árvores sintáticas visualizadas
- Estatísticas

---

## ⚠️ Erros Comuns e Soluções

### Erro 1: Expoente Não-Inteiro

**Código:**
```
2 3.5 ^
```

**Erro:**
```
ERRO SEMÂNTICO [Linha 1]: Expoente de potenciação deve ser inteiro, encontrado real
```

**Solução:** Use expoente inteiro
```
2 3 ^     # ✅ Correto
```

**Nota:** Expoentes negativos são permitidos!
```
2 -3 ^    # ✅ Correto (resultado: 0 em divisão inteira)
```

### Erro 2: Divisão Inteira com Real

**Código:**
```
10.5 2 /
```

**Erro:**
```
ERRO SEMÂNTICO [Linha 1]: Divisão inteira requer operando1 inteiro, encontrado real
```

**Solução:** Use divisão real (`|`) ou converta para int
```
10.5 2 |    # ✅ Divisão real
10 2 /      # ✅ Divisão inteira
```

### Erro 3: Variável Não Declarada

**Código:**
```
x 2 *
```

**Erro:**
```
ERRO SEMÂNTICO [Linha 1]: Variável 'x' não declarada
```

**Solução:** Declare a variável primeiro
```
42 x MEM    # Declara x
x 2 *       # ✅ Agora pode usar
```

### Erro 4: Condição Não-Booleana

**Código:**
```
5 (10) (20) IF
```

**Erro:**
```
ERRO SEMÂNTICO [Linha 1]: Condição de IF deve ser booleana, encontrado int
```

**Solução:** Use operador relacional
```
5 3 > (10) (20) IF    # ✅ Correto
```

### Erro 5: Booleano em Memória

**Código:**
```
5 3 > resultado MEM
```

**Erro:**
```
ERRO SEMÂNTICO [Linha 1]: Tipo booleano não pode ser armazenado em memória
```

**Solução:** Armazene apenas int ou real
```
5 3 + resultado MEM    # ✅ Correto (int)
```

### Erro 6: Divisão por Zero

**Código:**
```
10 0 /
```

**Erro:**
```
ERRO SEMÂNTICO [Linha 1]: Divisão por zero detectada
```

**Solução:** Use divisor diferente de zero
```
10 2 /    # ✅ Correto
```

---

## 🎓 Exemplos Práticos

### Exemplo 1: Calculadora Simples

```
# calculadora.txt
5 3 +        # 8
10 2 -       # 8
7 3 *        # 21
15 3 |       # 5.0
10 3 /       # 3
10 3 %       # 1
2 3 ^        # 8
```

### Exemplo 2: Gestão de Variáveis

```
# variaveis.txt
10 a MEM
20 b MEM
a b +        # 30
a b *        # 200
```

### Exemplo 3: Fibonacci Simplificado

```
# fibonacci.txt
1 fib1 MEM
1 fib2 MEM
fib1 fib2 +        # Próximo fibonacci
```

### Exemplo 4: Condicional Complexa

```
# condicional.txt
100 score MEM
score 90 >= (A) (
    score 80 >= (B) (
        score 70 >= (C) (D) IF
    ) IF
) IF
```

### Exemplo 5: Loop Contador

```
# contador.txt
0 count MEM
(count 5 <) (
    count 1 + count MEM
) WHILE
count    # Resultado final: 5
```

---

## 🔍 Depuração

### Modo Verboso

O compilador já exibe informações detalhadas por padrão:
- Linha sendo processada
- Tipo inferido
- Erros com contexto completo

### Análise de Erros

Cada erro exibe:
```
🔴 Erro #1:
   Tipo: ERRO_SEMANTICO
   ERRO SEMÂNTICO [Linha 5]: Descrição do erro
   📍 Contexto: (código relevante)
```

### Inspeção do JSON

```python
import json

with open('analise_semantica_20250106_143000.json', 'r') as f:
    dados = json.load(f)

# Ver metadados
print(dados['metadata'])

# Ver erros
for erro in dados['erros_semanticos']:
    print(erro['mensagem'])

# Ver tabela de símbolos
for var, info in dados['tabela_simbolos'].items():
    print(f"{var}: {info['tipo']}")
```

---

## 📚 Recursos Adicionais

### Documentação Completa

- `README.md` - Visão geral do projeto
- `GRAMATICA_ATRIBUTOS.md` - Gramática formal
- `REGRAS_DEDUCAO.md` - Regras de inferência de tipos
- `DOCUMENTACAO_ESTRUTURAS.md` - Estruturas de controle
- `EXEMPLOS_USO.md` - Mais exemplos práticos

### Arquivos de Teste

- `teste1.txt` - Casos básicos válidos
- `teste2.txt` - Casos de erro
- `teste3.txt` - Casos complexos

---

## 💡 Dicas e Boas Práticas

### 1. Comentários

Use `#` para comentários:
```
# Este é um comentário
5 3 +    # Soma de 5 e 3
```

### 2. Formatação

Mantenha uma operação por linha para facilitar leitura:
```
# Bom ✅
5 3 +
10 2 -

# Evite (múltiplas operações confusas)
```

### 3. Nomes de Variáveis

Use nomes descritivos:
```
100 score MEM       # ✅ Claro
100 s MEM           # ❌ Confuso
```

### 4. Estruturas Complexas

Use parênteses para clareza:
```
(x 0 >) (
    (x 10 <) (1) (0) IF
) (
    -1
) IF
```

### 5. Teste Incremental

Teste seu código linha por linha:
```
# Linha 1
5 3 +

# Adicione linha 2 após validar linha 1
10 2 -
```

---

## 🆘 Suporte

### Problemas Comuns

1. **Arquivo não encontrado**
   ```bash
   python compilador_final_corrigido.py arquivo_inexistente.txt
   # Erro: Arquivo 'arquivo_inexistente.txt' não encontrado
   ```
   Solução: Verifique o nome e caminho do arquivo

2. **Sintaxe inválida**
   - Verifique se operadores vêm após operandos (RPN)
   - Confirme uso correto de parênteses
   - Valide estrutura das estruturas de controle

3. **Erros de tipo**
   - Revise tabela de promoção de tipos
   - Verifique restrições de operadores (/, %, ^)
   - Confirme tipos de condições (devem ser booleanos)

---

## ✅ Checklist de Uso

Antes de executar:
- [ ] Arquivo de código existe
- [ ] Sintaxe RPN correta
- [ ] Variáveis declaradas antes do uso
- [ ] Condições são booleanas
- [ ] Operadores usados corretamente

Após execução:
- [ ] Verificar erros no terminal
- [ ] Consultar relatório JSON
- [ ] Revisar relatório Markdown
- [ ] Validar tabela de símbolos

---

## 📞 Contato e Contribuições

Para dúvidas, sugestões ou relato de bugs:
1. Consulte a documentação completa
2. Revise os exemplos fornecidos
3. Execute os casos de teste incluídos

---

**Versão:** 3.0 - Análise Semântica Completa  
**Última Atualização:** Janeiro 2025  
**Autores:** João Victor Roth, Mariana Trentiny Barbosa  
**Instituição:** PUCPR - Pontifícia Universidade Católica do Paraná
