from database.conexao import conectar


def criar_tabelas():
    # Abre a conexão com o banco de dados
    conexao = conectar()
    cursor = conexao.cursor()

    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        )
    """)

    # Tabela de disciplinas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id_disciplina INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            professor TEXT,
            meta_semanal INTEGER NOT NULL
        )
    """)

    # Tabela de atividades
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL,
            id_disciplina INTEGER NOT NULL,

            FOREIGN KEY (id_disciplina)
            REFERENCES disciplinas (id_disciplina)
            ON DELETE CASCADE
        )
    """)

    # Tabela de sessões de estudo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessoes_estudo (
            id_sessao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_disciplina INTEGER NOT NULL,
            id_atividade INTEGER,
            tempo_minutos INTEGER NOT NULL,
            data_estudo TEXT NOT NULL,
            tipo_dia TEXT NOT NULL,
            nome_feriado TEXT,

            FOREIGN KEY (id_usuario)
            REFERENCES usuarios (id_usuario)
            ON DELETE CASCADE,

            FOREIGN KEY (id_disciplina)
            REFERENCES disciplinas (id_disciplina)
            ON DELETE CASCADE,

            FOREIGN KEY (id_atividade)
            REFERENCES atividades (id_atividade)
            ON DELETE SET NULL
        )
    """)

    # Salva as alterações
    conexao.commit()

    # Fecha a conexão
    conexao.close()
