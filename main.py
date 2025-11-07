#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analisador Semântico - Fase 3
Linguagens Formais e Autômatos

Integrantes do grupo (ordem alfabética):
# Gabriel Hess - gabrielhess
# João Victor Roth - joaoroth
# Mariana Trentiny Barbosa - marianabarbosa
# Vitor Hugo B Weber - vitorweber

Nome do grupo no Canvas: RA2-10
"""

import sys
import re
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime


# ============================================================================
# DEFINIÇÕES DE TIPOS
# ============================================================================

class TokenType(Enum):
    """Tipos de tokens reconhecidos"""
    INT_LITERAL = "INT_LITERAL"
    REAL_LITERAL = "REAL_LITERAL"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULT = "MULT"
    DIV_REAL = "DIV_REAL"
    DIV_INT = "DIV_INT"
    MOD = "MOD"
    POW = "POW"
    GT = "GT"
    LT = "LT"
    GTE = "GTE"
    LTE = "LTE"
    EQ = "EQ"
    NEQ = "NEQ"
    MEM = "MEM"
    RES = "RES"
    IF = "IF"
    WHILE = "WHILE"
    FOR = "FOR"
    ID = "ID"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"


@dataclass
class Token:
    """Representa um token"""
    tipo: TokenType
    valor: Any
    linha: int
    coluna: int


@dataclass
class NoAST:
    """Nó da Árvore Sintática Abstrata"""
    tipo_no: str
    valor: Any = None
    tipo_dado: Optional[str] = None
    filhos: List['NoAST'] = None
    linha: int = 0
    contexto: str = ""  # Para armazenar o contexto da expressão
    
    def __post_init__(self):
        if self.filhos is None:
            self.filhos = []
    
    def para_dict(self) -> Dict[str, Any]:
        """Converte para formato JSON"""
        return {
            "tipo_vertice": self.tipo_no,
            "tipo_inferido": self.tipo_dado if self.tipo_dado else "nao_determinado",
            "valor": self.valor,
            "linha": self.linha,
            "filhos": [filho.para_dict() for filho in self.filhos]
        }


# ============================================================================
# FASE 1: ANÁLISE LÉXICA
# ============================================================================

class AnalisadorLexico:
    """Análise Léxica - Tokenização"""
    
    def __init__(self, codigo: str, numero_linha: int = 1):
        self.codigo = codigo
        self.posicao = 0
        self.linha = numero_linha
        self.coluna = 1
        self.tokens = []
    
    def tokenizar(self) -> List[Token]:
        """Realiza análise léxica completa"""
        while self.posicao < len(self.codigo):
            char = self.codigo[self.posicao]
            
            if char.isspace():
                if char == '\n':
                    self.linha += 1
                    self.coluna = 1
                else:
                    self.coluna += 1
                self.posicao += 1
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.linha, self.coluna))
                self.coluna += 1
                self.posicao += 1
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.linha, self.coluna))
                self.coluna += 1
                self.posicao += 1
            elif char in '+-*|/%^':
                self.tokens.append(self.tokenizar_operador(char))
            elif char in '><!=':
                self.tokens.append(self.tokenizar_operador_relacional())
            elif char.isdigit() or (char == '-' and self.posicao + 1 < len(self.codigo) and self.codigo[self.posicao + 1].isdigit()):
                self.tokens.append(self.tokenizar_numero())
            elif char.isalpha():
                self.tokens.append(self.tokenizar_identificador())
            else:
                self.tokens.append(Token(TokenType.UNKNOWN, char, self.linha, self.coluna))
                self.coluna += 1
                self.posicao += 1
        
        self.tokens.append(Token(TokenType.EOF, None, self.linha, self.coluna))
        return self.tokens
    
    def tokenizar_operador(self, char: str) -> Token:
        """Tokeniza operadores aritméticos"""
        tipo_mapa = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULT,
            '|': TokenType.DIV_REAL,
            '/': TokenType.DIV_INT,
            '%': TokenType.MOD,
            '^': TokenType.POW
        }
        token = Token(tipo_mapa[char], char, self.linha, self.coluna)
        self.coluna += 1
        self.posicao += 1
        return token
    
    def tokenizar_operador_relacional(self) -> Token:
        """Tokeniza operadores relacionais"""
        inicio_col = self.coluna
        char = self.codigo[self.posicao]
        
        if self.posicao + 1 < len(self.codigo):
            dois_chars = self.codigo[self.posicao:self.posicao + 2]
            if dois_chars in ['==', '!=', '>=', '<=']:
                self.posicao += 2
                self.coluna += 2
                tipo_mapa = {
                    '==': TokenType.EQ,
                    '!=': TokenType.NEQ,
                    '>=': TokenType.GTE,
                    '<=': TokenType.LTE
                }
                return Token(tipo_mapa[dois_chars], dois_chars, self.linha, inicio_col)
        
        self.posicao += 1
        self.coluna += 1
        tipo_mapa = {
            '>': TokenType.GT,
            '<': TokenType.LT
        }
        return Token(tipo_mapa.get(char, TokenType.UNKNOWN), char, self.linha, inicio_col)
    
    def tokenizar_numero(self) -> Token:
        """Tokeniza números inteiros e reais"""
        inicio = self.posicao
        inicio_col = self.coluna
        tem_ponto = False
        
        # Handle negative numbers
        if self.codigo[self.posicao] == '-':
            self.posicao += 1
            self.coluna += 1
        
        while self.posicao < len(self.codigo):
            char = self.codigo[self.posicao]
            if char.isdigit():
                self.posicao += 1
                self.coluna += 1
            elif char == '.' and not tem_ponto:
                tem_ponto = True
                self.posicao += 1
                self.coluna += 1
            else:
                break
        
        valor_str = self.codigo[inicio:self.posicao]
        if tem_ponto:
            return Token(TokenType.REAL_LITERAL, float(valor_str), self.linha, inicio_col)
        else:
            return Token(TokenType.INT_LITERAL, int(valor_str), self.linha, inicio_col)
    
    def tokenizar_identificador(self) -> Token:
        """Tokeniza identificadores e palavras-chave"""
        inicio = self.posicao
        inicio_col = self.coluna
        
        while self.posicao < len(self.codigo) and (self.codigo[self.posicao].isalnum() or self.codigo[self.posicao] == '_'):
            self.posicao += 1
            self.coluna += 1
        
        valor = self.codigo[inicio:self.posicao]
        
        # Palavras-chave
        palavras_chave = {
            'MEM': TokenType.MEM,
            'RES': TokenType.RES,
            'IF': TokenType.IF,
            'WHILE': TokenType.WHILE,
            'FOR': TokenType.FOR
        }
        
        tipo = palavras_chave.get(valor, TokenType.ID)
        return Token(tipo, valor, self.linha, inicio_col)


# ============================================================================
# FASE 2: ANÁLISE SINTÁTICA
# ============================================================================

class AnalisadorSintatico:
    """Parser LL(1) para a linguagem RPN"""
    
    def __init__(self, tokens: List[Token], codigo_original: str):
        self.tokens = tokens
        self.posicao = 0
        self.codigo_original = codigo_original
    
    def token_atual(self) -> Token:
        """Retorna o token atual"""
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return self.tokens[-1]
    
    def consumir(self, tipo_esperado: TokenType) -> Token:
        """Consome um token do tipo esperado"""
        token = self.token_atual()
        if token.tipo != tipo_esperado:
            raise SyntaxError(f"Esperado {tipo_esperado}, encontrado {token.tipo} na linha {token.linha}")
        self.posicao += 1
        return token
    
    def analisar(self) -> NoAST:
        """Analisa uma expressão completa"""
        self.consumir(TokenType.LPAREN)
        resultado = self.analisar_expressao()
        self.consumir(TokenType.RPAREN)
        return resultado
    
    def obter_contexto(self, inicio_pos: int, fim_pos: int) -> str:
        """Obtém o contexto de código entre duas posições de tokens"""
        if inicio_pos < len(self.tokens) and fim_pos <= len(self.tokens):
            inicio_token = self.tokens[inicio_pos]
            fim_token = self.tokens[min(fim_pos - 1, len(self.tokens) - 1)]
            
            # Encontra as linhas no código original
            linhas = self.codigo_original.split('\n')
            if inicio_token.linha <= len(linhas):
                return linhas[inicio_token.linha - 1].strip()
        return ""
    
    def analisar_expressao(self) -> NoAST:
        """Analisa uma expressão RPN"""
        inicio_pos = self.posicao - 1  # -1 porque já consumimos o '('
        elementos = []
        
        while self.token_atual().tipo != TokenType.RPAREN and self.token_atual().tipo != TokenType.EOF:
            if self.token_atual().tipo == TokenType.LPAREN:
                elementos.append(self.analisar())
            else:
                elementos.append(self.analisar_elemento())
        
        contexto = self.obter_contexto(inicio_pos, self.posicao + 1)
        
        if not elementos:
            raise SyntaxError(f"Expressão vazia na linha {self.token_atual().linha}")
        
        # Comando especial RES
        if len(elementos) == 2 and elementos[1].tipo_no == "OPERADOR" and elementos[1].valor == "RES":
            no = NoAST("COMANDO_RES", linha=elementos[0].linha, contexto=contexto)
            no.filhos = [elementos[0]]
            return no
        
        # Comando especial MEM
        if len(elementos) == 3 and elementos[2].tipo_no == "OPERADOR" and elementos[2].valor == "MEM":
            no = NoAST("COMANDO_MEM", valor=elementos[1].valor, linha=elementos[0].linha, contexto=contexto)
            no.filhos = [elementos[0]]
            return no
        
        # Leitura de memória
        if len(elementos) == 1 and elementos[0].tipo_no == "ID":
            no = NoAST("LEITURA_MEM", linha=elementos[0].linha, contexto=contexto)
            no.filhos = [elementos[0]]
            return no
        
        # Estruturas de controle
        if len(elementos) >= 3:
            ultimo = elementos[-1]
            if ultimo.tipo_no == "OPERADOR":
                if ultimo.valor == "IF" and len(elementos) == 4:
                    no = NoAST("ESTRUTURA_IF", linha=elementos[0].linha, contexto=contexto)
                    no.filhos = elementos[:-1]
                    return no
                elif ultimo.valor == "WHILE" and len(elementos) == 3:
                    no = NoAST("ESTRUTURA_WHILE", linha=elementos[0].linha, contexto=contexto)
                    no.filhos = elementos[:-1]
                    return no
                elif ultimo.valor == "FOR" and len(elementos) == 5:
                    no = NoAST("ESTRUTURA_FOR", linha=elementos[0].linha, contexto=contexto)
                    no.filhos = elementos[:-1]
                    return no
        
        # Expressão aritmética ou relacional
        if len(elementos) == 3 and elementos[2].tipo_no == "OPERADOR":
            no = NoAST("EXPRESSAO", linha=elementos[0].linha, contexto=contexto)
            no.filhos = elementos
            return no
        
        raise SyntaxError(f"Estrutura inválida na linha {self.token_atual().linha}")
    
    def analisar_elemento(self) -> NoAST:
        """Analisa um elemento individual"""
        token = self.token_atual()
        
        if token.tipo == TokenType.INT_LITERAL:
            self.posicao += 1
            return NoAST("OPERANDO", valor=token.valor, tipo_dado="int", linha=token.linha)
        
        elif token.tipo == TokenType.REAL_LITERAL:
            self.posicao += 1
            return NoAST("OPERANDO", valor=token.valor, tipo_dado="real", linha=token.linha)
        
        elif token.tipo == TokenType.ID:
            self.posicao += 1
            return NoAST("ID", valor=token.valor, tipo_dado="id", linha=token.linha)
        
        elif token.tipo in [TokenType.PLUS, TokenType.MINUS, TokenType.MULT, 
                            TokenType.DIV_REAL, TokenType.DIV_INT, TokenType.MOD, 
                            TokenType.POW]:
            self.posicao += 1
            op_mapa = {
                TokenType.PLUS: "PLUS",
                TokenType.MINUS: "MINUS",
                TokenType.MULT: "MULT",
                TokenType.DIV_REAL: "DIV_REAL",
                TokenType.DIV_INT: "DIV_INT",
                TokenType.MOD: "MOD",
                TokenType.POW: "POW"
            }
            return NoAST("OPERADOR", valor=op_mapa[token.tipo], linha=token.linha)
        
        elif token.tipo in [TokenType.GT, TokenType.LT, TokenType.GTE, 
                            TokenType.LTE, TokenType.EQ, TokenType.NEQ]:
            self.posicao += 1
            op_mapa = {
                TokenType.GT: "GT",
                TokenType.LT: "LT",
                TokenType.GTE: "GTE",
                TokenType.LTE: "LTE",
                TokenType.EQ: "EQ",
                TokenType.NEQ: "NEQ"
            }
            return NoAST("OPERADOR", valor=op_mapa[token.tipo], linha=token.linha)
        
        elif token.tipo in [TokenType.MEM, TokenType.RES, TokenType.IF, 
                            TokenType.WHILE, TokenType.FOR]:
            self.posicao += 1
            return NoAST("OPERADOR", valor=token.tipo.value, linha=token.linha)
        
        else:
            raise SyntaxError(f"Token inesperado {token.tipo} na linha {token.linha}")


# ============================================================================
# FASE 3: ANÁLISE SEMÂNTICA - Funções Conforme Especificação
# ============================================================================

# Aluno 1: Gramática de Atributos e Tabela de Símbolos
def definirGramaticaAtributos() -> Dict:
    """
    Define a gramática de atributos com regras semânticas.
    Retorna um dicionário com as regras de tipo e promoção.
    """
    gramatica = {
        "operadores_aritmeticos": ["PLUS", "MINUS", "MULT", "DIV_REAL", "DIV_INT", "MOD", "POW"],
        "operadores_relacionais": ["GT", "LT", "GTE", "LTE", "EQ", "NEQ"],
        
        "regras_promocao": {
            ("int", "int"): "int",
            ("int", "real"): "real",
            ("real", "int"): "real",
            ("real", "real"): "real",
            ("erro", "int"): "erro",
            ("erro", "real"): "erro",
            ("int", "erro"): "erro",
            ("real", "erro"): "erro",
            ("erro", "erro"): "erro",
            ("booleano", "booleano"): "booleano"
        },
        
        "regras_operadores": {
            # Operadores aritméticos
            "PLUS": {"tipos_aceitos": [("int", "int"), ("int", "real"), ("real", "int"), ("real", "real")]},
            "MINUS": {"tipos_aceitos": [("int", "int"), ("int", "real"), ("real", "int"), ("real", "real")]},
            "MULT": {"tipos_aceitos": [("int", "int"), ("int", "real"), ("real", "int"), ("real", "real")]},
            "DIV_REAL": {"tipos_aceitos": [("int", "int"), ("int", "real"), ("real", "int"), ("real", "real")]},
            "DIV_INT": {"tipos_aceitos": [("int", "int")]},  # Apenas inteiros
            "MOD": {"tipos_aceitos": [("int", "int")]},      # Apenas inteiros
            "POW": {"base": ["int", "real"], "expoente": ["int"]},  # Expoente deve ser inteiro positivo
            
            # Operadores relacionais
            "GT": {"tipos_aceitos": [("int", "int"), ("int", "real"), ("real", "int"), ("real", "real")], "retorno": "booleano"},
            "LT": {"tipos_aceitos": [("int", "int"), ("int", "real"), ("real", "int"), ("real", "real")], "retorno": "booleano"},
            "GTE": {"tipos_aceitos": [("int", "int"), ("int", "real"), ("real", "int"), ("real", "real")], "retorno": "booleano"},
            "LTE": {"tipos_aceitos": [("int", "int"), ("int", "real"), ("real", "int"), ("real", "real")], "retorno": "booleano"},
            "EQ": {"tipos_aceitos": [("int", "int"), ("int", "real"), ("real", "int"), ("real", "real")], "retorno": "booleano"},
            "NEQ": {"tipos_aceitos": [("int", "int"), ("int", "real"), ("real", "int"), ("real", "real")], "retorno": "booleano"}
        }
    }
    
    tabela_simbolos = {}
    
    return {
        "gramatica": gramatica,
        "tabela_simbolos": tabela_simbolos
    }


def inicializarTabelaSimbolos() -> Dict:
    """Inicializa a Tabela de Símbolos vazia"""
    return {}


def adicionarSimbolo(tabela: Dict, nome: str, tipo: str, linha: int):
    """
    Adiciona um símbolo à tabela.
    
    Args:
        tabela: Tabela de símbolos
        nome: Nome do símbolo (variável)
        tipo: Tipo do símbolo ('int' ou 'real')
        linha: Linha onde foi declarado
    """
    # Booleano não pode ser armazenado em memória
    if tipo == "booleano":
        raise ValueError(f"ERRO SEMÂNTICO [Linha {linha}]: Tipo booleano não pode ser armazenado em memória")
    
    tabela[nome] = {
        "tipo": tipo,
        "inicializada": True,
        "linha_declaracao": linha
    }


def buscarSimbolo(tabela: Dict, nome: str) -> Optional[Dict]:
    """
    Busca um símbolo na tabela.
    
    Args:
        tabela: Tabela de símbolos
        nome: Nome do símbolo a buscar
    
    Returns:
        Informações do símbolo ou None se não encontrado
    """
    return tabela.get(nome)


# Aluno 2: Análise Semântica Principal
def analisarSemantica(arvoreSintatica: NoAST, gramaticaAtributos: Dict, 
                      tabelaSimbolos: Dict, numero_linha: int, erros: List,
                      resultados_anteriores: List = None) -> NoAST:
    """
    Realiza a análise semântica principal com verificação de tipos.
    
    Args:
        arvoreSintatica: AST gerada na fase 2
        gramaticaAtributos: Regras semânticas
        tabelaSimbolos: Tabela de símbolos
        numero_linha: Número da linha atual
        erros: Lista para acumular erros
        resultados_anteriores: Lista de resultados anteriores para RES
    
    Returns:
        NoAST: Árvore anotada com tipos
    """
    gramatica = gramaticaAtributos["gramatica"]
    
    if arvoreSintatica.tipo_no == "EXPRESSAO":
        return analisarExpressao(arvoreSintatica, gramatica, tabelaSimbolos, 
                                numero_linha, erros)
    
    elif arvoreSintatica.tipo_no == "COMANDO_MEM":
        return analisarComandoMem(arvoreSintatica, tabelaSimbolos, 
                                 numero_linha, erros)
    
    elif arvoreSintatica.tipo_no == "LEITURA_MEM":
        return analisarLeituraMem(arvoreSintatica, tabelaSimbolos, 
                                 numero_linha, erros)
    
    elif arvoreSintatica.tipo_no == "COMANDO_RES":
        return analisarComandoRes(arvoreSintatica, numero_linha, erros, 
                                 resultados_anteriores)
    
    elif arvoreSintatica.tipo_no == "ESTRUTURA_IF":
        return analisarEstruturaIf(arvoreSintatica, gramatica, tabelaSimbolos, 
                                  numero_linha, erros, resultados_anteriores)
    
    elif arvoreSintatica.tipo_no == "ESTRUTURA_WHILE":
        return analisarEstruturaWhile(arvoreSintatica, gramatica, tabelaSimbolos, 
                                     numero_linha, erros, resultados_anteriores)
    
    elif arvoreSintatica.tipo_no == "ESTRUTURA_FOR":
        return analisarEstruturaFor(arvoreSintatica, gramatica, tabelaSimbolos, 
                                   numero_linha, erros, resultados_anteriores)
    
    return arvoreSintatica


def promover_tipo(tipo1: str, tipo2: str, gramatica: Dict) -> str:
    """
    Promove tipos conforme regras da gramática.
    
    Args:
        tipo1: Primeiro tipo
        tipo2: Segundo tipo
        gramatica: Regras da gramática
    
    Returns:
        Tipo promovido
    """
    regras = gramatica["regras_promocao"]
    return regras.get((tipo1, tipo2), "erro")


def analisarExpressao(no: NoAST, gramatica: Dict, tabelaSimbolos: Dict, 
                     numero_linha: int, erros: List) -> NoAST:
    """Analisa expressão aritmética ou relacional"""
    if len(no.filhos) != 3:
        erros.append({
            "linha": numero_linha,
            "tipo": "ERRO_SEMANTICO",
            "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Expressão malformada: esperado 3 filhos, encontrado {len(no.filhos)}",
            "contexto": no.contexto
        })
        no.tipo_dado = "erro"
        return no
    
    operando1 = no.filhos[0]
    operando2 = no.filhos[1]
    operador = no.filhos[2]
    
    # Analisa operando1
    if operando1.tipo_no in ["EXPRESSAO", "ESTRUTURA_IF", "ESTRUTURA_WHILE", "ESTRUTURA_FOR"]:
        operando1 = analisarSemantica(operando1, {"gramatica": gramatica}, 
                                     tabelaSimbolos, numero_linha, erros)
    elif operando1.tipo_no == "LEITURA_MEM":
        operando1 = analisarLeituraMem(operando1, tabelaSimbolos, numero_linha, erros)
    elif operando1.tipo_no == "ID":
        nome_var = operando1.valor
        simbolo = buscarSimbolo(tabelaSimbolos, nome_var)
        if not simbolo:
            erros.append({
                "linha": numero_linha,
                "tipo": "ERRO_SEMANTICO",
                "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Variável '{nome_var}' não declarada",
                "contexto": no.contexto
            })
            operando1.tipo_dado = "erro"
        else:
            operando1.tipo_dado = simbolo["tipo"]
    
    # Analisa operando2
    if operando2.tipo_no in ["EXPRESSAO", "ESTRUTURA_IF", "ESTRUTURA_WHILE", "ESTRUTURA_FOR"]:
        operando2 = analisarSemantica(operando2, {"gramatica": gramatica}, 
                                     tabelaSimbolos, numero_linha, erros)
    elif operando2.tipo_no == "LEITURA_MEM":
        operando2 = analisarLeituraMem(operando2, tabelaSimbolos, numero_linha, erros)
    elif operando2.tipo_no == "ID":
        nome_var = operando2.valor
        simbolo = buscarSimbolo(tabelaSimbolos, nome_var)
        if not simbolo:
            erros.append({
                "linha": numero_linha,
                "tipo": "ERRO_SEMANTICO",
                "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Variável '{nome_var}' não declarada",
                "contexto": no.contexto
            })
            operando2.tipo_dado = "erro"
        else:
            operando2.tipo_dado = simbolo["tipo"]
    
    op_nome = operador.valor
    regras_op = gramatica["regras_operadores"].get(op_nome, {})
    
    # Validações específicas para POW - expoente deve ser inteiro (pode ser negativo)
    if op_nome == "POW":
        # Verifica se o expoente é inteiro
        if operando2.tipo_dado != "int":
            erros.append({
                "linha": numero_linha,
                "tipo": "ERRO_SEMANTICO",
                "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Expoente de potenciação deve ser inteiro, encontrado {operando2.tipo_dado}",
                "contexto": no.contexto
            })
            no.tipo_dado = "erro"
            return no
        # Expoentes negativos são permitidos (2^-3 = 0.125 ou 0 em divisão inteira)
    
    # Validações para DIV_INT e MOD - ambos operandos devem ser inteiros
    if op_nome in ["DIV_INT", "MOD"]:
        if operando1.tipo_dado != "int":
            erros.append({
                "linha": numero_linha,
                "tipo": "ERRO_SEMANTICO",
                "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Operação {op_nome} requer operando1 inteiro, encontrado {operando1.tipo_dado}",
                "contexto": no.contexto
            })
            no.tipo_dado = "erro"
            return no
            
        if operando2.tipo_dado != "int":
            erros.append({
                "linha": numero_linha,
                "tipo": "ERRO_SEMANTICO",
                "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Operação {op_nome} requer operando2 inteiro, encontrado {operando2.tipo_dado}",
                "contexto": no.contexto
            })
            no.tipo_dado = "erro"
            return no
    
    # Verificação de divisão por zero (se for literal)
    if op_nome in ["DIV_REAL", "DIV_INT", "MOD"]:
        if operando2.tipo_no == "OPERANDO" and operando2.valor == 0:
            erros.append({
                "linha": numero_linha,
                "tipo": "ERRO_SEMANTICO",
                "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Divisão por zero detectada",
                "contexto": no.contexto
            })
            no.tipo_dado = "erro"
            return no
    
    # Define tipo do resultado
    if op_nome in gramatica["operadores_relacionais"]:
        no.tipo_dado = "booleano"
    elif op_nome in ["DIV_INT", "MOD"]:
        no.tipo_dado = "int"  # Resultado sempre inteiro
    else:
        no.tipo_dado = promover_tipo(operando1.tipo_dado, operando2.tipo_dado, gramatica)
    
    return no


# Aluno 3: Análise Semântica de Memória e Controle
def analisarSemanticaMemoria(arvoreSintatica: NoAST, tabelaSimbolos: Dict, 
                            numero_linha: int, erros: List):
    """
    Valida uso de memórias (MEM).
    Implementa validações específicas de memória conforme especificação.
    """
    # Esta função é chamada após a análise principal
    # Percorre a árvore verificando uso de memórias
    if arvoreSintatica.tipo_no == "LEITURA_MEM":
        nome_var = arvoreSintatica.filhos[0].valor
        simbolo = buscarSimbolo(tabelaSimbolos, nome_var)
        
        if not simbolo:
            erros.append({
                "linha": numero_linha,
                "tipo": "ERRO_SEMANTICO",
                "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Memória '{nome_var}' não foi inicializada",
                "contexto": arvoreSintatica.contexto
            })
    
    # Percorre filhos recursivamente
    for filho in arvoreSintatica.filhos:
        if hasattr(filho, 'filhos'):
            analisarSemanticaMemoria(filho, tabelaSimbolos, numero_linha, erros)


def analisarSemanticaControle(arvoreSintatica: NoAST, tabelaSimbolos: Dict, 
                             numero_linha: int, erros: List):
    """
    Valida estruturas de controle.
    Verifica que condições em IF, WHILE e FOR são booleanas.
    """
    if arvoreSintatica.tipo_no in ["ESTRUTURA_IF", "ESTRUTURA_WHILE", "ESTRUTURA_FOR"]:
        condicao = arvoreSintatica.filhos[0]
        
        # Para FOR, a condição é o segundo filho
        if arvoreSintatica.tipo_no == "ESTRUTURA_FOR":
            condicao = arvoreSintatica.filhos[1]
        
        if condicao.tipo_dado != "booleano":
            estrutura = arvoreSintatica.tipo_no.replace("ESTRUTURA_", "")
            erros.append({
                "linha": numero_linha,
                "tipo": "ERRO_SEMANTICO",
                "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Condição de {estrutura} deve ser booleana, encontrado {condicao.tipo_dado}",
                "contexto": arvoreSintatica.contexto
            })
    
    # Percorre filhos recursivamente
    for filho in arvoreSintatica.filhos:
        if hasattr(filho, 'filhos'):
            analisarSemanticaControle(filho, tabelaSimbolos, numero_linha, erros)


def analisarComandoMem(no: NoAST, tabelaSimbolos: Dict, numero_linha: int, 
                       erros: List) -> NoAST:
    """
    Analisa comando MEM: (valor ID MEM)
    Booleano não pode ser armazenado em memória.
    """
    valor_no = no.filhos[0]
    nome_var = no.valor
    
    # Determina o tipo do valor
    if valor_no.tipo_no == "OPERANDO":
        tipo_valor = valor_no.tipo_dado
    elif valor_no.tipo_no in ["EXPRESSAO", "ESTRUTURA_IF", "ESTRUTURA_WHILE", "ESTRUTURA_FOR"]:
        tipo_valor = valor_no.tipo_dado if valor_no.tipo_dado else "int"
    elif valor_no.tipo_no == "LEITURA_MEM":
        simbolo = buscarSimbolo(tabelaSimbolos, valor_no.filhos[0].valor)
        tipo_valor = simbolo["tipo"] if simbolo else "erro"
    else:
        tipo_valor = "int"
    
    # Verifica se não é booleano
    if tipo_valor == "booleano":
        erros.append({
            "linha": numero_linha,
            "tipo": "ERRO_SEMANTICO",
            "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Tipo booleano não pode ser armazenado em memória",
            "contexto": no.contexto
        })
        no.tipo_dado = "erro"
        return no
    
    # Adiciona à tabela de símbolos
    try:
        adicionarSimbolo(tabelaSimbolos, nome_var, tipo_valor, numero_linha)
        no.tipo_dado = tipo_valor
    except ValueError as e:
        erros.append({
            "linha": numero_linha,
            "tipo": "ERRO_SEMANTICO",
            "mensagem": str(e),
            "contexto": no.contexto
        })
        no.tipo_dado = "erro"
    
    return no


def analisarLeituraMem(no: NoAST, tabelaSimbolos: Dict, numero_linha: int, 
                       erros: List) -> NoAST:
    """Analisa leitura de memória: (ID)"""
    nome_var = no.filhos[0].valor
    simbolo = buscarSimbolo(tabelaSimbolos, nome_var)
    
    if not simbolo:
        erros.append({
            "linha": numero_linha,
            "tipo": "ERRO_SEMANTICO",
            "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Memória '{nome_var}' não foi inicializada",
            "contexto": no.contexto
        })
        no.tipo_dado = "erro"
        return no
    
    no.tipo_dado = simbolo["tipo"]
    return no


def analisarComandoRes(no: NoAST, numero_linha: int, erros: List, 
                       resultados_anteriores: List = None) -> NoAST:
    """
    Analisa comando RES.
    RES só funciona para inteiros positivos.
    """
    operando = no.filhos[0]
    
    # RES só aceita inteiros não negativos
    if operando.tipo_dado != "int":
        erros.append({
            "linha": numero_linha,
            "tipo": "ERRO_SEMANTICO",
            "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: RES requer índice inteiro, encontrado {operando.tipo_dado}",
            "contexto": no.contexto
        })
        no.tipo_dado = "erro"
        return no
    
    # Se temos o valor literal, verificamos se é não negativo
    if operando.tipo_no == "OPERANDO" and isinstance(operando.valor, int):
        n = operando.valor
        
        if n < 0:
            erros.append({
                "linha": numero_linha,
                "tipo": "ERRO_SEMANTICO",
                "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Índice de RES deve ser inteiro não-negativo, encontrado {n}",
                "contexto": no.contexto
            })
            no.tipo_dado = "erro"
            return no
        
        # Verifica se o índice é válido
        if resultados_anteriores is not None:
            if n >= len(resultados_anteriores):
                erros.append({
                    "linha": numero_linha,
                    "tipo": "ERRO_SEMANTICO",
                    "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: RES referencia expressão inexistente: índice {n} mas só existem {len(resultados_anteriores)} expressões anteriores",
                    "contexto": no.contexto
                })
                no.tipo_dado = "erro"
                return no
            
            # Define o tipo como o tipo da expressão referenciada
            if n < len(resultados_anteriores):
                no.tipo_dado = resultados_anteriores[-(n+1)].get("tipo", "int")
            else:
                no.tipo_dado = "int"
        else:
            no.tipo_dado = "int"
    else:
        # Não podemos verificar em tempo de compilação
        no.tipo_dado = "int"
    
    return no


def analisarEstruturaIf(no: NoAST, gramatica: Dict, tabelaSimbolos: Dict, 
                        numero_linha: int, erros: List, 
                        resultados_anteriores: List = None) -> NoAST:
    """Analisa estrutura IF"""
    condicao = no.filhos[0]
    bloco_true = no.filhos[1]
    bloco_false = no.filhos[2]
    
    # Analisa condição
    condicao_analisada = analisarSemantica(condicao, {"gramatica": gramatica}, 
                                          tabelaSimbolos, numero_linha, erros, 
                                          resultados_anteriores)
    
    if condicao_analisada.tipo_dado != "booleano":
        erros.append({
            "linha": numero_linha,
            "tipo": "ERRO_SEMANTICO",
            "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Condição do IF deve ser booleana, encontrado {condicao_analisada.tipo_dado}",
            "contexto": no.contexto
        })
        no.tipo_dado = "erro"
        return no
    
    # Analisa blocos
    bloco_true_analisado = analisarSemantica(bloco_true, {"gramatica": gramatica}, 
                                            tabelaSimbolos, numero_linha, erros, 
                                            resultados_anteriores)
    bloco_false_analisado = analisarSemantica(bloco_false, {"gramatica": gramatica}, 
                                             tabelaSimbolos, numero_linha, erros, 
                                             resultados_anteriores)
    
    # Define tipo resultante
    if bloco_true_analisado.tipo_dado == bloco_false_analisado.tipo_dado:
        no.tipo_dado = bloco_true_analisado.tipo_dado
    else:
        no.tipo_dado = promover_tipo(bloco_true_analisado.tipo_dado, 
                                    bloco_false_analisado.tipo_dado, gramatica)
    
    no.filhos = [condicao_analisada, bloco_true_analisado, bloco_false_analisado]
    return no


def analisarEstruturaWhile(no: NoAST, gramatica: Dict, tabelaSimbolos: Dict, 
                           numero_linha: int, erros: List, 
                           resultados_anteriores: List = None) -> NoAST:
    """Analisa estrutura WHILE"""
    condicao = no.filhos[0]
    bloco = no.filhos[1]
    
    # Analisa condição
    condicao_analisada = analisarSemantica(condicao, {"gramatica": gramatica}, 
                                          tabelaSimbolos, numero_linha, erros, 
                                          resultados_anteriores)
    
    if condicao_analisada.tipo_dado != "booleano":
        erros.append({
            "linha": numero_linha,
            "tipo": "ERRO_SEMANTICO",
            "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Condição do WHILE deve ser booleana, encontrado {condicao_analisada.tipo_dado}",
            "contexto": no.contexto
        })
        no.tipo_dado = "erro"
        return no
    
    # Analisa bloco
    bloco_analisado = analisarSemantica(bloco, {"gramatica": gramatica}, 
                                       tabelaSimbolos, numero_linha, erros, 
                                       resultados_anteriores)
    
    no.tipo_dado = bloco_analisado.tipo_dado
    no.filhos = [condicao_analisada, bloco_analisado]
    return no


def analisarEstruturaFor(no: NoAST, gramatica: Dict, tabelaSimbolos: Dict, 
                        numero_linha: int, erros: List, 
                        resultados_anteriores: List = None) -> NoAST:
    """Analisa estrutura FOR"""
    inicio = no.filhos[0]
    condicao = no.filhos[1]
    incremento = no.filhos[2]
    bloco = no.filhos[3]
    
    # Analisa cada parte
    inicio_analisado = analisarSemantica(inicio, {"gramatica": gramatica}, 
                                        tabelaSimbolos, numero_linha, erros, 
                                        resultados_anteriores)
    condicao_analisada = analisarSemantica(condicao, {"gramatica": gramatica}, 
                                          tabelaSimbolos, numero_linha, erros, 
                                          resultados_anteriores)
    
    if condicao_analisada.tipo_dado != "booleano":
        erros.append({
            "linha": numero_linha,
            "tipo": "ERRO_SEMANTICO",
            "mensagem": f"ERRO SEMÂNTICO [Linha {numero_linha}]: Condição do FOR deve ser booleana, encontrado {condicao_analisada.tipo_dado}",
            "contexto": no.contexto
        })
        no.tipo_dado = "erro"
        return no
    
    incremento_analisado = analisarSemantica(incremento, {"gramatica": gramatica}, 
                                            tabelaSimbolos, numero_linha, erros, 
                                            resultados_anteriores)
    bloco_analisado = analisarSemantica(bloco, {"gramatica": gramatica}, 
                                       tabelaSimbolos, numero_linha, erros, 
                                       resultados_anteriores)
    
    no.tipo_dado = bloco_analisado.tipo_dado
    no.filhos = [inicio_analisado, condicao_analisada, incremento_analisado, bloco_analisado]
    return no


# Aluno 4: Geração da Árvore Atribuída e Integração
def gerarArvoreAtribuida(arvoreAnotada: NoAST) -> Dict:
    """
    Gera a árvore sintática abstrata atribuída final.
    
    Args:
        arvoreAnotada: Árvore com anotações de tipo
    
    Returns:
        Dicionário com a árvore atribuída em formato JSON
    """
    return arvoreAnotada.para_dict()


def main():
    """
    Função principal que gerencia a execução sequencial dos analisadores.
    """
    # Lê o arquivo de entrada
    if len(sys.argv) != 2:
        print("Uso: python compilador.py <arquivo_entrada>")
        sys.exit(1)
    
    nome_arquivo = sys.argv[1]
    
    try:
        with open(nome_arquivo, 'r') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado")
        sys.exit(1)
    
    # Processa linha por linha
    linhas = codigo.strip().split('\n')
    resultados = []
    resultados_anteriores = []
    erros_totais = []
    
    # Inicializa gramática e tabela de símbolos globais
    gramatica_atributos = definirGramaticaAtributos()
    tabela_simbolos_global = inicializarTabelaSimbolos()
    
    for numero_linha, linha in enumerate(linhas, 1):
        linha = linha.strip()
        if not linha or linha.startswith('#'):
            continue
        
        print(f"\n{'='*60}")
        print(f"Processando linha {numero_linha}: {linha}")
        print(f"{'='*60}")
        
        try:
            # Fase 1: Análise Léxica
            lexer = AnalisadorLexico(linha, numero_linha)
            tokens = lexer.tokenizar()
            
            # Fase 2: Análise Sintática
            parser = AnalisadorSintatico(tokens, linha)
            arvore_sintatica = parser.analisar()
            
            # Fase 3: Análise Semântica
            erros_linha = []
            
            # Análise semântica principal
            arvore_anotada = analisarSemantica(
                arvore_sintatica, 
                gramatica_atributos, 
                tabela_simbolos_global, 
                numero_linha, 
                erros_linha,
                resultados_anteriores
            )
            
            # Análise de memória
            analisarSemanticaMemoria(
                arvore_anotada,
                tabela_simbolos_global,
                numero_linha,
                erros_linha
            )
            
            # Análise de controle
            analisarSemanticaControle(
                arvore_anotada,
                tabela_simbolos_global,
                numero_linha,
                erros_linha
            )
            
            # Gera árvore atribuída
            arvore_atribuida = gerarArvoreAtribuida(arvore_anotada)
            
            # Armazena resultado
            resultado = {
                "linha": numero_linha,
                "codigo": linha,
                "arvore": arvore_atribuida,
                "tipo": arvore_anotada.tipo_dado,
                "erros": erros_linha
            }
            
            resultados.append(resultado)
            resultados_anteriores.append({"tipo": arvore_anotada.tipo_dado, "linha": numero_linha})
            erros_totais.extend(erros_linha)
            
            # Exibe resultado
            if erros_linha:
                print("\n" + "="*60)
                print("❌ ERROS SEMÂNTICOS DETECTADOS")
                print("="*60)
                for i, erro in enumerate(erros_linha, 1):
                    print(f"\n🔴 Erro #{i}:")
                    print(f"   Tipo: {erro.get('tipo', 'ERRO_SEMANTICO')}")
                    print(f"   {erro['mensagem']}")
                    if 'contexto' in erro and erro['contexto']:
                        print(f"   📍 Contexto: {erro['contexto']}")
                    print()
                print("="*60)
            else:
                print(f"\n✅ Análise bem-sucedida")
                print(f"   Tipo inferido: {arvore_anotada.tipo_dado}")
                if arvore_anotada.valor is not None:
                    print(f"   Valor: {arvore_anotada.valor}")
            
        except Exception as e:
            print(f"\n❌ Erro ao processar linha {numero_linha}: {str(e)}")
            erros_totais.append({
                "linha": numero_linha,
                "tipo": "ERRO",
                "mensagem": str(e)
            })
    
    # Relatório final
    print(f"\n{'='*60}")
    print("RELATÓRIO FINAL")
    print(f"{'='*60}")
    print(f"Total de linhas processadas: {len(resultados)}")
    print(f"Total de erros: {len(erros_totais)}")
    
    if erros_totais:
        print("\n" + "="*60)
        print("📋 RESUMO DETALHADO DE ERROS")
        print("="*60)
        for i, erro in enumerate(erros_totais, 1):
            print(f"\n{i}. [Linha {erro.get('linha', '?')}]")
            print(f"   {erro['mensagem']}")
            if 'contexto' in erro and erro['contexto']:
                print(f"   📍 {erro['contexto']}")
        print("\n" + "="*60)
    
    # Salva resultados em JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_json = f"analise_semantica_{timestamp}.json"
    nome_md = f"analise_semantica_{timestamp}.md"
    
    # Estrutura completa do relatório
    relatorio_completo = {
        "metadata": {
            "arquivo_fonte": nome_arquivo,
            "data_compilacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "total_linhas": len(resultados),
            "total_erros": len(erros_totais)
        },
        "tabela_simbolos": tabela_simbolos_global,
        "erros_semanticos": erros_totais,
        "arvores_sintaticas": [
            {
                "linha": r["linha"],
                "codigo": r["codigo"],
                "ast": r["arvore"],
                "tipo": r["tipo"]
            }
            for r in resultados
        ]
    }
    
    with open(nome_json, 'w', encoding='utf-8') as f:
        json.dump(relatorio_completo, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Resultados salvos em: {nome_json}")
    
    # Gera automaticamente o Markdown
    print(f"📝 Gerando relatório em Markdown...")
    try:
        gerar_markdown_inline(relatorio_completo, nome_md)
        print(f"✅ Relatório Markdown gerado: {nome_md}")
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível gerar Markdown: {e}")
    
    # Tabela de símbolos final
    if tabela_simbolos_global:
        print(f"\n📊 TABELA DE SÍMBOLOS FINAL:")
        for nome, info in tabela_simbolos_global.items():
            print(f"  • {nome}: {info['tipo']} (linha {info['linha_declaracao']})")
    
    # Retorna código de erro se houver erros
    sys.exit(1 if erros_totais else 0)


def gerar_markdown_inline(dados: Dict, nome_arquivo: str):
    """Gera relatório Markdown a partir dos dados da análise"""
    linhas = []
    
    # Cabeçalho
    linhas.append("# 📊 Relatório de Análise Semântica\n")
    linhas.append("---\n")
    
    # Metadados
    meta = dados["metadata"]
    linhas.append("## 📋 Informações da Compilação\n")
    linhas.append(f"- **Arquivo fonte**: `{meta['arquivo_fonte']}`")
    linhas.append(f"- **Data**: {meta['data_compilacao']}")
    linhas.append(f"- **Linhas processadas**: {meta['total_linhas']}")
    linhas.append(f"- **Erros encontrados**: {meta['total_erros']}\n")
    
    # Status
    if meta['total_erros'] == 0:
        linhas.append("**Status**: ✅ COMPILAÇÃO BEM-SUCEDIDA\n")
    else:
        linhas.append("**Status**: ❌ COMPILAÇÃO COM ERROS\n")
    
    linhas.append("---\n")
    
    # Tabela de Símbolos
    tabela = dados.get("tabela_simbolos", {})
    linhas.append("## 📚 Tabela de Símbolos\n")
    if tabela:
        linhas.append("| Variável | Tipo | Inicializada | Linha Declaração |")
        linhas.append("|----------|------|--------------|------------------|")
        for nome, info in tabela.items():
            linhas.append(f"| `{nome}` | `{info['tipo']}` | ✅ | {info['linha_declaracao']} |")
    else:
        linhas.append("*Nenhuma variável declarada.*")
    
    linhas.append("\n---\n")
    
    # Erros
    erros = dados.get("erros_semanticos", [])
    linhas.append("## ⚠️ Erros Semânticos\n")
    if erros:
        linhas.append(f"**Total**: {len(erros)} erro(s)\n")
        for i, erro in enumerate(erros, 1):
            linhas.append(f"### Erro {i}\n")
            linhas.append(f"```")
            linhas.append(f"{erro['mensagem']}")
            if 'contexto' in erro and erro['contexto']:
                linhas.append(f"Contexto: {erro['contexto']}")
            linhas.append(f"```\n")
    else:
        linhas.append("✅ **Nenhum erro semântico detectado!**\n")
    
    linhas.append("---\n")
    
    # Árvores Sintáticas
    arvores = dados.get("arvores_sintaticas", [])
    linhas.append("## 🌳 Árvores Sintáticas Abstratas\n")
    linhas.append(f"**Total**: {len(arvores)} árvore(s)\n")
    
    for arvore_info in arvores:
        linha_num = arvore_info['linha']
        codigo = arvore_info['codigo']
        tipo = arvore_info['tipo']
        
        linhas.append(f"### Linha {linha_num}: `{codigo}`\n")
        linhas.append(f"**Tipo inferido**: `{tipo}`\n")
        
        # AST em formato de árvore textual
        ast = arvore_info['ast']
        linhas.append("```")
        linhas.append(desenhar_arvore_simples(ast))
        linhas.append("```\n")
    
    linhas.append("---\n")
    linhas.append(f"\n*Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}*\n")
    
    # Salva
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas))


def desenhar_arvore_simples(no: Dict, prefixo: str = "", eh_ultimo: bool = True) -> str:
    """Desenha árvore em formato textual simples"""
    linhas = []
    
    # Conectores
    conector = "└── " if eh_ultimo else "├── "
    
    # Informação do nó
    tipo = no.get("tipo_vertice", "?")
    tipo_inf = no.get("tipo_inferido", "?")
    valor = no.get("valor")
    
    info = f"{tipo}"
    if tipo_inf and tipo_inf != "nao_determinado":
        info += f" [{tipo_inf}]"
    if valor is not None:
        info += f" = {valor}"
    
    linhas.append(prefixo + conector + info)
    
    # Filhos
    filhos = no.get("filhos", [])
    for i, filho in enumerate(filhos):
        eh_ultimo_filho = (i == len(filhos) - 1)
        extensao = "    " if eh_ultimo else "│   "
        linhas.append(desenhar_arvore_simples(filho, prefixo + extensao, eh_ultimo_filho))
    
    return '\n'.join(linhas)


if __name__ == "__main__":
    main()
