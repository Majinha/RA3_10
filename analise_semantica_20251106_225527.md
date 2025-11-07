# 📊 Relatório de Análise Semântica

---

## 📋 Informações da Compilação

- **Arquivo fonte**: `teste2.txt`
- **Data**: 06/11/2025 22:55:27
- **Linhas processadas**: 13
- **Erros encontrados**: 3

**Status**: ❌ COMPILAÇÃO COM ERROS

---

## 📚 Tabela de Símbolos

*Nenhuma variável declarada.*

---

## ⚠️ Erros Semânticos

**Total**: 3 erro(s)

### Erro 1

```
Estrutura inválida na linha 6
```

### Erro 2

```
Estrutura inválida na linha 14
```

### Erro 3

```
Estrutura inválida na linha 16
```

---

## 🌳 Árvores Sintáticas Abstratas

**Total**: 13 árvore(s)

### Linha 1: `((10 5 +) (3 2 *) -)`

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

### Linha 2: `((20 4 /) (5 2 +) *)`

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

### Linha 3: `((6 3 *) (12 6 /) +)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 6
    │   ├── OPERANDO [int] = 3
    │   └── OPERADOR = MULT
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 12
    │   ├── OPERANDO [int] = 6
    │   └── OPERADOR = DIV_INT
    └── OPERADOR = PLUS
```

### Linha 4: `((9 3 /) (3 2 ^) -)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 9
    │   ├── OPERANDO [int] = 3
    │   └── OPERADOR = DIV_INT
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 3
    │   ├── OPERANDO [int] = 2
    │   └── OPERADOR = POW
    └── OPERADOR = MINUS
```

### Linha 5: `((5 2 *) (10 3 -) +)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 5
    │   ├── OPERANDO [int] = 2
    │   └── OPERADOR = MULT
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 10
    │   ├── OPERANDO [int] = 3
    │   └── OPERADOR = MINUS
    └── OPERADOR = PLUS
```

### Linha 7: `(10 10 ==)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 10
    ├── OPERANDO [int] = 10
    └── OPERADOR = EQ
```

### Linha 8: `(10 9 !=)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 10
    ├── OPERANDO [int] = 9
    └── OPERADOR = NEQ
```

### Linha 9: `(9 10 <)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 9
    ├── OPERANDO [int] = 10
    └── OPERADOR = LT
```

### Linha 10: `(10 9 >)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 10
    ├── OPERANDO [int] = 9
    └── OPERADOR = GT
```

### Linha 11: `(10 10 >=)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 10
    ├── OPERANDO [int] = 10
    └── OPERADOR = GTE
```

### Linha 12: `(9 10 <=)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 9
    ├── OPERANDO [int] = 10
    └── OPERADOR = LTE
```

### Linha 13: `(999 1 +)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── OPERANDO [int] = 999
    ├── OPERANDO [int] = 1
    └── OPERADOR = PLUS
```

### Linha 15: `(50 51 !=)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 50
    ├── OPERANDO [int] = 51
    └── OPERADOR = NEQ
```

---


*Relatório gerado automaticamente em 06/11/2025 às 22:55:27*
