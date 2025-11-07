# 📊 Relatório de Análise Semântica

---

## 📋 Informações da Compilação

- **Arquivo fonte**: `teste_semantica.txt`
- **Data**: 07/11/2025 00:33:37
- **Linhas processadas**: 12
- **Erros encontrados**: 9

**Status**: ❌ COMPILAÇÃO COM ERROS

---

## 📚 Tabela de Símbolos

| Variável | Tipo | Inicializada | Linha Declaração |
|----------|------|--------------|------------------|
| `x` | `int` | ✅ | 22 |

---

## ⚠️ Erros Semânticos

**Total**: 9 erro(s)

### Erro 1

```
ERRO SEMÂNTICO [Linha 10]: Expoente de potenciação deve ser inteiro, encontrado real
```

### Erro 2

```
ERRO SEMÂNTICO [Linha 13]: Operação DIV_INT requer operando1 inteiro, encontrado real
```

### Erro 3

```
ERRO SEMÂNTICO [Linha 16]: Divisão por zero detectada
```

### Erro 4

```
Estrutura inválida na linha 19
```

### Erro 5

```
ERRO SEMÂNTICO [Linha 28]: Variável 'y' não declarada
```

### Erro 6

```
Estrutura inválida na linha 32
```

### Erro 7

```
Estrutura inválida na linha 38
```

### Erro 8

```
Estrutura inválida na linha 41
```

### Erro 9

```
ERRO SEMÂNTICO [Linha 47]: Operação MOD requer operando1 inteiro, encontrado real
```

---

## 🌳 Árvores Sintáticas Abstratas

**Total**: 12 árvore(s)

### Linha 4: `(5 3 +)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── OPERANDO [int] = 5
    ├── OPERANDO [int] = 3
    └── OPERADOR = PLUS
```

### Linha 7: `(5 3.5 +)`

**Tipo inferido**: `real`

```
└── EXPRESSAO [real]
    ├── OPERANDO [int] = 5
    ├── OPERANDO [real] = 3.5
    └── OPERADOR = PLUS
```

### Linha 10: `(2 3.5 ^)`

**Tipo inferido**: `erro`

```
└── EXPRESSAO [erro]
    ├── OPERANDO [int] = 2
    ├── OPERANDO [real] = 3.5
    └── OPERADOR = POW
```

### Linha 13: `(10.5 2 /)`

**Tipo inferido**: `erro`

```
└── EXPRESSAO [erro]
    ├── OPERANDO [real] = 10.5
    ├── OPERANDO [int] = 2
    └── OPERADOR = DIV_INT
```

### Linha 16: `(10 0 /)`

**Tipo inferido**: `erro`

```
└── EXPRESSAO [erro]
    ├── OPERANDO [int] = 10
    ├── OPERANDO [int] = 0
    └── OPERADOR = DIV_INT
```

### Linha 22: `(42 x MEM)`

**Tipo inferido**: `int`

```
└── COMANDO_MEM [int] = x
    └── OPERANDO [int] = 42
```

### Linha 25: `(x 2 *)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── ID [int] = x
    ├── OPERANDO [int] = 2
    └── OPERADOR = MULT
```

### Linha 28: `(y 3 +)`

**Tipo inferido**: `erro`

```
└── EXPRESSAO [erro]
    ├── ID [erro] = y
    ├── OPERANDO [int] = 3
    └── OPERADOR = PLUS
```

### Linha 31: `(5 3 >)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 5
    ├── OPERANDO [int] = 3
    └── OPERADOR = GT
```

### Linha 35: `(10 5 >)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 10
    ├── OPERANDO [int] = 5
    └── OPERADOR = GT
```

### Linha 44: `(10 3 %)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── OPERANDO [int] = 10
    ├── OPERANDO [int] = 3
    └── OPERADOR = MOD
```

### Linha 47: `(10.5 3 %)`

**Tipo inferido**: `erro`

```
└── EXPRESSAO [erro]
    ├── OPERANDO [real] = 10.5
    ├── OPERANDO [int] = 3
    └── OPERADOR = MOD
```

---


*Relatório gerado automaticamente em 07/11/2025 às 00:33:37*
