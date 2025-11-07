# 📊 Relatório de Análise Semântica

---

## 📋 Informações da Compilação

- **Arquivo fonte**: `teste3.txt`
- **Data**: 06/11/2025 22:55:35
- **Linhas processadas**: 12
- **Erros encontrados**: 4

**Status**: ❌ COMPILAÇÃO COM ERROS

---

## 📚 Tabela de Símbolos

| Variável | Tipo | Inicializada | Linha Declaração |
|----------|------|--------------|------------------|
| `X` | `int` | ✅ | 10 |

---

## ⚠️ Erros Semânticos

**Total**: 4 erro(s)

### Erro 1

```
Estrutura inválida na linha 4
```

### Erro 2

```
ERRO SEMÂNTICO [Linha 11]: Divisão por zero detectada
```

### Erro 3

```
Estrutura inválida na linha 12
```

### Erro 4

```
ERRO SEMÂNTICO [Linha 13]: Operação MOD requer operando1 inteiro, encontrado real
```

---

## 🌳 Árvores Sintáticas Abstratas

**Total**: 12 árvore(s)

### Linha 1: `((10 5 >) (50 25 +) WHILE)`

**Tipo inferido**: `int`

```
└── ESTRUTURA_WHILE [int]
    ├── EXPRESSAO [booleano]
    │   ├── OPERANDO [int] = 10
    │   ├── OPERANDO [int] = 5
    │   └── OPERADOR = GT
    └── EXPRESSAO [int]
        ├── OPERANDO [int] = 50
        ├── OPERANDO [int] = 25
        └── OPERADOR = PLUS
```

### Linha 2: `((5 3 >) (10 8 >) (5 2 +) (100 50 -) FOR)`

**Tipo inferido**: `int`

```
└── ESTRUTURA_FOR [int]
    ├── EXPRESSAO [booleano]
    │   ├── OPERANDO [int] = 5
    │   ├── OPERANDO [int] = 3
    │   └── OPERADOR = GT
    ├── EXPRESSAO [booleano]
    │   ├── OPERANDO [int] = 10
    │   ├── OPERANDO [int] = 8
    │   └── OPERADOR = GT
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 5
    │   ├── OPERANDO [int] = 2
    │   └── OPERADOR = PLUS
    └── EXPRESSAO [int]
        ├── OPERANDO [int] = 100
        ├── OPERANDO [int] = 50
        └── OPERADOR = MINUS
```

### Linha 3: `((2 1 >) (100 50 <) (10 5 +) (20 10 *) FOR)`

**Tipo inferido**: `int`

```
└── ESTRUTURA_FOR [int]
    ├── EXPRESSAO [booleano]
    │   ├── OPERANDO [int] = 2
    │   ├── OPERANDO [int] = 1
    │   └── OPERADOR = GT
    ├── EXPRESSAO [booleano]
    │   ├── OPERANDO [int] = 100
    │   ├── OPERANDO [int] = 50
    │   └── OPERADOR = LT
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 10
    │   ├── OPERANDO [int] = 5
    │   └── OPERADOR = PLUS
    └── EXPRESSAO [int]
        ├── OPERANDO [int] = 20
        ├── OPERANDO [int] = 10
        └── OPERADOR = MULT
```

### Linha 5: `((10 5 ==) (100 50 /) (25 5 +) IF)`

**Tipo inferido**: `int`

```
└── ESTRUTURA_IF [int]
    ├── EXPRESSAO [booleano]
    │   ├── OPERANDO [int] = 10
    │   ├── OPERANDO [int] = 5
    │   └── OPERADOR = EQ
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 100
    │   ├── OPERANDO [int] = 50
    │   └── OPERADOR = DIV_INT
    └── EXPRESSAO [int]
        ├── OPERANDO [int] = 25
        ├── OPERANDO [int] = 5
        └── OPERADOR = PLUS
```

### Linha 6: `((20 4 /) (5 2 +) *)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 20
    │   ├── OPERANDO [int] = 4
    │   └── OPERADOR = DIV_INT
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 5
    │   ├── OPERANDO [int] = 2
    │   └── OPERADOR = PLUS
    └── OPERADOR = MULT
```

### Linha 7: `((10 5 +) (3 2 *) -)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 10
    │   ├── OPERANDO [int] = 5
    │   └── OPERADOR = PLUS
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 3
    │   ├── OPERANDO [int] = 2
    │   └── OPERADOR = MULT
    └── OPERADOR = MINUS
```

### Linha 8: `(100 100 ==)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 100
    ├── OPERANDO [int] = 100
    └── OPERADOR = EQ
```

### Linha 9: `(4 RES)`

**Tipo inferido**: `int`

```
└── COMANDO_RES [int]
    └── OPERANDO [int] = 4
```

### Linha 10: `(60 X MEM)`

**Tipo inferido**: `int`

```
└── COMANDO_MEM [int] = X
    └── OPERANDO [int] = 60
```

### Linha 11: `(10 0 /)`

**Tipo inferido**: `erro`

```
└── EXPRESSAO [erro]
    ├── OPERANDO [int] = 10
    ├── OPERANDO [int] = 0
    └── OPERADOR = DIV_INT
```

### Linha 13: `(10.5 3 %)`

**Tipo inferido**: `erro`

```
└── EXPRESSAO [erro]
    ├── OPERANDO [real] = 10.5
    ├── OPERANDO [int] = 3
    └── OPERADOR = MOD
```

### Linha 14: `(X X +)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── ID [int] = X
    ├── ID [int] = X
    └── OPERADOR = PLUS
```

---


*Relatório gerado automaticamente em 06/11/2025 às 22:55:35*
