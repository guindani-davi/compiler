"""
Script principal para executar o analisador léxico
Processa arquivos .sp (Pascal Simplificado)
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from lexer import lexer, print_tokens


def analisar_arquivo(caminho_arquivo):
    """
    Analisa um arquivo .sp e imprime os tokens encontrados
    """
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return False

    # Verifica a extensão do arquivo
    if not caminho_arquivo.endswith(".sp"):
        print(f"Aviso: O arquivo '{caminho_arquivo}' não possui extensão .sp")

    # Lê o conteúdo do arquivo
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            codigo = arquivo.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return False

    # Imprime informações do arquivo
    print("=" * 70)
    print(f"Análise Léxica do arquivo: {caminho_arquivo}")
    print("=" * 70)
    print()

    # Executa a análise léxica
    print_tokens(codigo)

    print()
    print("=" * 70)
    print("Análise concluída!")
    print("=" * 70)

    return True


def main():
    """
    Função principal
    """
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.sp>")
        print()
        print("Exemplos disponíveis:")
        examples_dir = Path("examples")
        if examples_dir.exists():
            for arquivo in examples_dir.glob("*.sp"):
                print(f"  - {arquivo}")
        sys.exit(1)

    arquivo = sys.argv[1]
    analisar_arquivo(arquivo)


if __name__ == "__main__":
    main()
