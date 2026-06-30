import sqlite3
import os

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), "controle_estudos.db")


def conectar():
    # Cria conexão com o banco SQLite
    conexao = sqlite3.connect(CAMINHO_BANCO)

    # Ativa o uso de chaves estrangeiras no SQLite
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao
