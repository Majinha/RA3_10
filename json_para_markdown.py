#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Conversor JSON → Markdown
Transforma o JSON da AST em Markdown legível com árvore visualizada
"""

import json
import sys
from datetime import datetime


def desenhar_arvore(no, prefixo="", eh_ultimo=True):
    """
    Desenha a árvore AST em formato ASCII art
    
    Args:
        no: Nó da árvore (dict)
        prefixo: Prefixo para indentação
        eh_ultimo: Se é o último filho do pai
    
    Returns:
        String com a árvore formatada
    """
    resultado = []
    
    # Conectores ASCII
    conector = "└── " if eh_ultimo else "├── "
    
    # Informações do nó
    tipo = no.get("tipo_vertice", "?")
    tipo_inf = no.get("tipo_inferido", "?")
    valor = no.get("valor")
    linha = no.get("linha", "?")
    
    # Formata a linha do nó
    info_no = f"{tipo}"
    if tipo_inf and tipo_inf != "nao_determinado":
        info_no += f" [{tipo_inf}]"
    if valor is not None:
        info_no += f" = {valor}"
    info_no += f" (L{linha})"
    
    resultado.append(prefixo + conector + info_no)
    
    # Processa filhos
    filhos = no.get("filhos", [])
    for i, filho in enumerate(filhos):
        eh_ultimo_filho = (i == len(filhos) - 1)
        
        # Extensão do prefixo
        if eh_ultimo:
            novo_prefixo = prefixo + "    "
        else:
            novo_prefixo = prefixo + "│   "
        
        resultado.append(desenhar_arvore(filho, novo_prefixo, eh_ultimo_filho))
    
    return "\n".join(resultado)


def gerar_markdown(json_data, nome_saida="analise_compilacao.md"):
    """
    Gera arquivo Markdown a partir do JSON
    
    Args:
        json_data: Dados do JSON (dict)
        nome_saida: Nome do arquivo Markdown de saída
    """
    
    md_linhas = []
    
    # Cabeçalho
    md_linhas.append("# 📊 Análise de Compilação - Relatório Completo")
    md_linhas.append("")
    md_linhas.append("---")
    md_linhas.append("")
    
    # Metadados
    metadata = json_data.get("metadata", {})
    md_linhas.append("## 📋 Informações da Compilação")
    md_linhas.append("")
    md_linhas.append(f"- **Arquivo fonte**: `{metadata.get('arquivo_fonte', 'N/A')}`")
    md_linhas.append(f"- **Data da compilação**: {metadata.get('data_compilacao', 'N/A')}")
    md_linhas.append(f"- **Total de linhas**: {metadata.get('total_linhas', 0)}")
    md_linhas.append(f"- **Total de erros**: {metadata.get('total_erros', 0)}")
    md_linhas.append("")
    md_linhas.append("---")
    md_linhas.append("")
    
    # Tabela de Símbolos
    tabela_simbolos = json_data.get("tabela_simbolos", {})
    md_linhas.append("## 📚 Tabela de Símbolos")
    md_linhas.append("")
    
    if tabela_simbolos:
        md_linhas.append("| Símbolo | Tipo | Inicializada | Linha Declaração |")
        md_linhas.append("|---------|------|--------------|------------------|")
        
        for nome, info in tabela_simbolos.items():
            tipo = info.get("tipo", "?")
            inicializada = "✅" if info.get("inicializada", False) else "❌"
            linha_decl = info.get("linha_declaracao", "?")
            md_linhas.append(f"| `{nome}` | `{tipo}` | {inicializada} | {linha_decl} |")
    else:
        md_linhas.append("*Nenhum símbolo declarado.*")
    
    md_linhas.append("")
    md_linhas.append("---")
    md_linhas.append("")
    
    # Erros Semânticos
    erros = json_data.get("erros_semanticos", [])
    md_linhas.append("## ⚠️ Erros Semânticos")
    md_linhas.append("")
    
    if erros:
        md_linhas.append(f"**Total de erros encontrados**: {len(erros)}")
        md_linhas.append("")
        
        for i, erro in enumerate(erros, 1):
            md_linhas.append(f"### Erro {i}")
            md_linhas.append("")
            md_linhas.append(f"- **Linha**: {erro.get('linha', '?')}")
            md_linhas.append(f"- **Tipo**: `{erro.get('tipo', '?')}`")
            md_linhas.append(f"- **Mensagem**: {erro.get('mensagem', '?')}")
            
            if 'contexto' in erro:
                md_linhas.append(f"- **Contexto**: `{erro.get('contexto')}`")
            
            md_linhas.append("")
    else:
        md_linhas.append("✅ **Nenhum erro semântico encontrado!**")
    
    md_linhas.append("")
    md_linhas.append("---")
    md_linhas.append("")
    
    # Árvores Sintáticas
    arvores = json_data.get("arvores_sintaticas", [])
    md_linhas.append("## 🌳 Árvores Sintáticas Abstratas (AST)")
    md_linhas.append("")
    md_linhas.append(f"**Total de árvores**: {len(arvores)}")
    md_linhas.append("")
    
    for arvore_info in arvores:
        linha_num = arvore_info.get("linha", "?")
        ast = arvore_info.get("ast", {})
        
        md_linhas.append(f"### Linha {linha_num}")
        md_linhas.append("")
        
        # Informações resumidas
        tipo_raiz = ast.get("tipo_vertice", "?")
        tipo_inf_raiz = ast.get("tipo_inferido", "?")
        
        md_linhas.append(f"**Tipo da raiz**: `{tipo_raiz}`")
        md_linhas.append(f"**Tipo inferido**: `{tipo_inf_raiz}`")
        md_linhas.append("")
        
        # Árvore ASCII
        md_linhas.append("#### Visualização da Árvore:")
        md_linhas.append("```")
        md_linhas.append("Raiz")
        md_linhas.append(desenhar_arvore(ast, "", True))
        md_linhas.append("```")
        md_linhas.append("")
        
        # JSON colapsado
        md_linhas.append("<details>")
        md_linhas.append("<summary>📄 Ver JSON completo</summary>")
        md_linhas.append("")
        md_linhas.append("```json")
        md_linhas.append(json.dumps(ast, indent=2, ensure_ascii=False))
        md_linhas.append("```")
        md_linhas.append("")
        md_linhas.append("</details>")
        md_linhas.append("")
        md_linhas.append("---")
        md_linhas.append("")
    
    # Estatísticas
    md_linhas.append("## 📈 Estatísticas da Compilação")
    md_linhas.append("")
    
    # Conta tipos de nós
    tipos_nos = {}
    for arvore_info in arvores:
        ast = arvore_info.get("ast", {})
        contar_tipos_nos(ast, tipos_nos)
    
    if tipos_nos:
        md_linhas.append("### Distribuição de Nós da AST")
        md_linhas.append("")
        md_linhas.append("| Tipo de Nó | Quantidade |")
        md_linhas.append("|------------|------------|")
        
        for tipo, qtd in sorted(tipos_nos.items(), key=lambda x: x[1], reverse=True):
            md_linhas.append(f"| `{tipo}` | {qtd} |")
    
    md_linhas.append("")
    
    # Conta tipos inferidos
    tipos_inferidos = {}
    for arvore_info in arvores:
        ast = arvore_info.get("ast", {})
        contar_tipos_inferidos(ast, tipos_inferidos)
    
    if tipos_inferidos:
        md_linhas.append("### Distribuição de Tipos Inferidos")
        md_linhas.append("")
        md_linhas.append("| Tipo | Quantidade |")
        md_linhas.append("|------|------------|")
        
        for tipo, qtd in sorted(tipos_inferidos.items(), key=lambda x: x[1], reverse=True):
            md_linhas.append(f"| `{tipo}` | {qtd} |")
    
    md_linhas.append("")
    md_linhas.append("---")
    md_linhas.append("")
    
    # Rodapé
    md_linhas.append("## ℹ️ Informações")
    md_linhas.append("")
    md_linhas.append("Este relatório foi gerado automaticamente pelo compilador.")
    md_linhas.append("")
    md_linhas.append(f"**Gerado em**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    md_linhas.append("")
    
    # Salva o arquivo
    with open(nome_saida, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_linhas))
    
    print(f"✅ Markdown gerado: {nome_saida}")


def contar_tipos_nos(no, contador):
    """Conta recursivamente os tipos de nós"""
    tipo = no.get("tipo_vertice")
    if tipo:
        contador[tipo] = contador.get(tipo, 0) + 1
    
    for filho in no.get("filhos", []):
        contar_tipos_nos(filho, contador)


def contar_tipos_inferidos(no, contador):
    """Conta recursivamente os tipos inferidos"""
    tipo = no.get("tipo_inferido")
    if tipo and tipo != "nao_determinado":
        contador[tipo] = contador.get(tipo, 0) + 1
    
    for filho in no.get("filhos", []):
        contar_tipos_inferidos(filho, contador)


def main():
    """Função principal"""
    print("\n" + "="*70)
    print("CONVERSOR JSON → MARKDOWN")
    print("Visualização de Árvores Sintáticas")
    print("="*70)
    
    if len(sys.argv) < 2:
        print("\nUSO: python json_para_markdown.py <arquivo.json> [saida.md]")
        print("\nExemplo:")
        print("  python json_para_markdown.py arvore_sintatica_atribuida.json")
        print("  python json_para_markdown.py arvore_sintatica_atribuida.json relatorio.md")
        sys.exit(1)
    
    arquivo_json = sys.argv[1]
    arquivo_saida = sys.argv[2] if len(sys.argv) > 2 else "analise_compilacao.md"
    
    try:
        # Carrega o JSON
        print(f"\n📂 Carregando: {arquivo_json}")
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Gera o Markdown
        print(f"🔄 Convertendo para Markdown...")
        gerar_markdown(dados, arquivo_saida)
        
        print(f"\n✅ Conversão concluída com sucesso!")
        print(f"📄 Arquivo gerado: {arquivo_saida}")
        
    except FileNotFoundError:
        print(f"\n❌ ERRO: Arquivo '{arquivo_json}' não encontrado")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\n❌ ERRO: JSON inválido - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
