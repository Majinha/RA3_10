# 📊 Relatório de Análise Semântica

---

## 📋 Informações da Compilação

- **Arquivo fonte**: `teste1.txt`
- **Data**: 06/11/2025 22:55:01
- **Linhas processadas**: 17
- **Erros encontrados**: 5

**Status**: ❌ COMPILAÇÃO COM ERROS

---

## 📚 Tabela de Símbolos

| Variável | Tipo | Inicializada | Linha Declaração |
|----------|------|--------------|------------------|
| `X` | `int` | ✅ | 10 |

---

## ⚠️ Erros Semânticos

**Total**: 5 erro(s)

### Erro 1

```
Estrutura inválida na linha 4
```

### Erro 2

```
Estrutura inválida na linha 7
```

### Erro 3

```
ERRO SEMÂNTICO [Linha 11]: RES requer índice inteiro, encontrado real
```

### Erro 4

```
ERRO SEMÂNTICO [Linha 14]: Operação DIV_INT requer operando1 inteiro, encontrado real
```

### Erro 5

```
ERRO SEMÂNTICO [Linha 19]: Expoente de potenciação deve ser inteiro, encontrado real
```

---

## 🌳 Árvores Sintáticas Abstratas

**Total**: 17 árvore(s)

### Linha 1: `(((10 5 +) (3 2 *) +) ((8 4 /) (2 3 +) -) *)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── EXPRESSAO [int]
    │   ├── EXPRESSAO [int]
    │   │   ├── OPERANDO [int] = 10
    │   │   ├── OPERANDO [int] = 5
    │   │   └── OPERADOR = PLUS
    │   ├── EXPRESSAO [int]
    │   │   ├── OPERANDO [int] = 3
    │   │   ├── OPERANDO [int] = 2
    │   │   └── OPERADOR = MULT
    │   └── OPERADOR = PLUS
    ├── EXPRESSAO [int]
    │   ├── EXPRESSAO [int]
    │   │   ├── OPERANDO [int] = 8
    │   │   ├── OPERANDO [int] = 4
    │   │   └── OPERADOR = DIV_INT
    │   ├── EXPRESSAO [int]
    │   │   ├── OPERANDO [int] = 2
    │   │   ├── OPERANDO [int] = 3
    │   │   └── OPERADOR = PLUS
    │   └── OPERADOR = MINUS
    └── OPERADOR = MULT
```

### Linha 2: `((100 50 -) (25 5 /) +)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 100
    │   ├── OPERANDO [int] = 50
    │   └── OPERADOR = MINUS
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 25
    │   ├── OPERANDO [int] = 5
    │   └── OPERADOR = DIV_INT
    └── OPERADOR = PLUS
```

### Linha 3: `((10 2 ^) (9 3 %) +)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 10
    │   ├── OPERANDO [int] = 2
    │   └── OPERADOR = POW
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 9
    │   ├── OPERANDO [int] = 3
    │   └── OPERADOR = MOD
    └── OPERADOR = PLUS
```

### Linha 5: `((20 10 >) ((10 5 <) (3 3 ==) (10 5 *) IF) ((50 25 !=) (10 2 ^) (5 5 +) IF) IF)`

**Tipo inferido**: `erro`

```
└── ESTRUTURA_IF [erro]
    ├── EXPRESSAO [booleano]
    │   ├── OPERANDO [int] = 20
    │   ├── OPERANDO [int] = 10
    │   └── OPERADOR = GT
    ├── ESTRUTURA_IF [erro]
    │   ├── EXPRESSAO [booleano]
    │   │   ├── OPERANDO [int] = 10
    │   │   ├── OPERANDO [int] = 5
    │   │   └── OPERADOR = LT
    │   ├── EXPRESSAO [booleano]
    │   │   ├── OPERANDO [int] = 3
    │   │   ├── OPERANDO [int] = 3
    │   │   └── OPERADOR = EQ
    │   └── EXPRESSAO [int]
    │       ├── OPERANDO [int] = 10
    │       ├── OPERANDO [int] = 5
    │       └── OPERADOR = MULT
    └── ESTRUTURA_IF [int]
        ├── EXPRESSAO [booleano]
        │   ├── OPERANDO [int] = 50
        │   ├── OPERANDO [int] = 25
        │   └── OPERADOR = NEQ
        ├── EXPRESSAO [int]
        │   ├── OPERANDO [int] = 10
        │   ├── OPERANDO [int] = 2
        │   └── OPERADOR = POW
        └── EXPRESSAO [int]
            ├── OPERANDO [int] = 5
            ├── OPERANDO [int] = 5
            └── OPERADOR = PLUS
```

### Linha 6: `(((10 5 +) (2 3 ^) >) ((20 4 /) (5 2 +) *) ((15 5 -) (10 2 *) +) IF)`

**Tipo inferido**: `int`

```
└── ESTRUTURA_IF [int]
    ├── EXPRESSAO [booleano]
    │   ├── EXPRESSAO [int]
    │   │   ├── OPERANDO [int] = 10
    │   │   ├── OPERANDO [int] = 5
    │   │   └── OPERADOR = PLUS
    │   ├── EXPRESSAO [int]
    │   │   ├── OPERANDO [int] = 2
    │   │   ├── OPERANDO [int] = 3
    │   │   └── OPERADOR = POW
    │   └── OPERADOR = GT
    ├── EXPRESSAO [int]
    │   ├── EXPRESSAO [int]
    │   │   ├── OPERANDO [int] = 20
    │   │   ├── OPERANDO [int] = 4
    │   │   └── OPERADOR = DIV_INT
    │   ├── EXPRESSAO [int]
    │   │   ├── OPERANDO [int] = 5
    │   │   ├── OPERANDO [int] = 2
    │   │   └── OPERADOR = PLUS
    │   └── OPERADOR = MULT
    └── EXPRESSAO [int]
        ├── EXPRESSAO [int]
        │   ├── OPERANDO [int] = 15
        │   ├── OPERANDO [int] = 5
        │   └── OPERADOR = MINUS
        ├── EXPRESSAO [int]
        │   ├── OPERANDO [int] = 10
        │   ├── OPERANDO [int] = 2
        │   └── OPERADOR = MULT
        └── OPERADOR = PLUS
```

### Linha 8: `((999 1 +) (10 2 /) +)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 999
    │   ├── OPERANDO [int] = 1
    │   └── OPERADOR = PLUS
    ├── EXPRESSAO [int]
    │   ├── OPERANDO [int] = 10
    │   ├── OPERANDO [int] = 2
    │   └── OPERADOR = DIV_INT
    └── OPERADOR = PLUS
```

### Linha 9: `(50 50 ==)`

**Tipo inferido**: `booleano`

```
└── EXPRESSAO [booleano]
    ├── OPERANDO [int] = 50
    ├── OPERANDO [int] = 50
    └── OPERADOR = EQ
```

### Linha 10: `(100 X MEM)`

**Tipo inferido**: `int`

```
└── COMANDO_MEM [int] = X
    └── OPERANDO [int] = 100
```

### Linha 11: `(1.22 RES)`

**Tipo inferido**: `erro`

```
└── COMANDO_RES [erro]
    └── OPERANDO [real] = 1.22
```

### Linha 12: `(5 RES)`

**Tipo inferido**: `erro`

```
└── COMANDO_RES [erro]
    └── OPERANDO [int] = 5
```

### Linha 13: `(5.5 4.5 +)`

**Tipo inferido**: `real`

```
└── EXPRESSAO [real]
    ├── OPERANDO [real] = 5.5
    ├── OPERANDO [real] = 4.5
    └── OPERADOR = PLUS
```

### Linha 14: `(7.2 3.6 /)`

**Tipo inferido**: `erro`

```
└── EXPRESSAO [erro]
    ├── OPERANDO [real] = 7.2
    ├── OPERANDO [real] = 3.6
    └── OPERADOR = DIV_INT
```

### Linha 15: `(100 25 -)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── OPERANDO [int] = 100
    ├── OPERANDO [int] = 25
    └── OPERADOR = MINUS
```

### Linha 16: `(10 2 ^)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── OPERANDO [int] = 10
    ├── OPERANDO [int] = 2
    └── OPERADOR = POW
```

### Linha 17: `(15 X *)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── OPERANDO [int] = 15
    ├── ID [int] = X
    └── OPERADOR = MULT
```

### Linha 18: `(90 45 /)`

**Tipo inferido**: `int`

```
└── EXPRESSAO [int]
    ├── OPERANDO [int] = 90
    ├── OPERANDO [int] = 45
    └── OPERADOR = DIV_INT
```

### Linha 19: `(2 3.5 ^)`

**Tipo inferido**: `erro`

```
└── EXPRESSAO [erro]
    ├── OPERANDO [int] = 2
    ├── OPERANDO [real] = 3.5
    └── OPERADOR = POW
```

---


*Relatório gerado automaticamente em 06/11/2025 às 22:55:01*
