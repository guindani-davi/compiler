"""
Script principal para executar análises léxica e sintática
Processa arquivos .sp (Pascal Simplificado)
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from lexer import lexer, print_tokens
from parser import parse_file
from semantic import analisar_semantica


def analisar_arquivo(caminho_arquivo, modo="completo"):
    """
    Analisa um arquivo .sp

    Args:
        caminho_arquivo: Caminho para o arquivo .sp
        modo: 'lexico' para análise léxica, 'sintatico' para sintática,
              'semantico' para semântica, 'completo' para todas
    """
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"✗ Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return False

    # Verifica a extensão do arquivo
    if not caminho_arquivo.endswith(".sp"):
        print(f"⚠ Aviso: O arquivo '{caminho_arquivo}' não possui extensão .sp")

    # Lê o conteúdo do arquivo
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            codigo = arquivo.read()
    except Exception as e:
        print(f"✗ Erro ao ler o arquivo: {e}")
        return False

    sucesso = True
    ast = None

    # Análise Léxica
    if modo in ["lexico", "completo"]:
        print("=" * 70)
        print(f"ANÁLISE LÉXICA: {caminho_arquivo}")
        print("=" * 70)
        print()

        print_tokens(codigo)

        print()
        print("=" * 70)
        print("Análise léxica concluída!")
        print("=" * 70)
        print()

    # Análise Sintática
    if modo in ["sintatico", "semantico", "completo"]:
        ast = parse_file(caminho_arquivo)
        sucesso = ast is not None

        if not sucesso:
            print(
                "\n✗ Análise sintática falhou. Não é possível prosseguir para análise semântica."
            )
            return False

    # Análise Semântica
    if modo in ["semantico", "completo"] and ast:
        print("\n" + "=" * 70)
        print(f"ANÁLISE SEMÂNTICA: {caminho_arquivo}")
        print("=" * 70)
        print()

        sucesso_semantico, analisador = analisar_semantica(ast, verbose=True)
        sucesso = sucesso and sucesso_semantico

        print()
        print("=" * 70)
        if sucesso_semantico:
            print("✓ Análise semântica concluída com sucesso!")
        else:
            print("✗ Análise semântica falhou!")
        print("=" * 70)
        print()

    return sucesso


def main():
    """
    Função principal
    """
    # Parse de argumentos
    modo = "completo"
    arquivo = None

    if len(sys.argv) < 2:
        print("Uso: python main.py [opções] <arquivo.sp>")
        print()
        print("Opções:")
        print("  -l, --lexico     Apenas análise léxica")
        print("  -s, --sintatico  Apenas análise sintática")
        print("  -sem, --semantico Análise sintática e semântica")
        print("  -c, --completo   Análise léxica, sintática e semântica (padrão)")
        print()
        print("Exemplos disponíveis:")
        examples_dir = Path("examples")
        if examples_dir.exists():
            for arq in sorted(examples_dir.glob("*.sp")):
                print(f"  - {arq}")
        sys.exit(1)

    # Processa argumentos
    for arg in sys.argv[1:]:
        if arg in ["-l", "--lexico"]:
            modo = "lexico"
        elif arg in ["-s", "--sintatico"]:
            modo = "sintatico"
        elif arg in ["-sem", "--semantico"]:
            modo = "semantico"
        elif arg in ["-c", "--completo"]:
            modo = "completo"
        elif not arg.startswith("-"):
            arquivo = arg

    if not arquivo:
        print("✗ Erro: Nenhum arquivo especificado")
        sys.exit(1)

    analisar_arquivo(arquivo, modo)


if __name__ == "__main__":
    main()
