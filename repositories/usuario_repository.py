import sqlite3

from database.conexao import conectar
from models.usuario import Usuario


class UsuarioRepository:
    def inserir(self, usuario):
        # Abre conexão com o banco.
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            # Insere o usuário no banco.
            cursor.execute(
                """
                INSERT INTO usuarios (nome, email, senha_hash)
                VALUES (?, ?, ?)
            """,
                (usuario.nome, usuario.email, usuario.senha_hash),
            )

            # Confirma a inserção.
            conexao.commit()

            # Pega o ID gerado automaticamente pelo banco.
            usuario.id_usuario = cursor.lastrowid

            return True

        except sqlite3.IntegrityError:
            # Esse erro pode acontecer se o email já estiver cadastrado,
            # porque a coluna email foi criada com UNIQUE.
            return False

        finally:
            # Fecha a conexão de qualquer forma.
            conexao.close()

    def buscar_por_email(self, email):
        # Abre conexão com o banco.
        conexao = conectar()
        cursor = conexao.cursor()

        # Busca um usuário pelo email.
        cursor.execute(
            """
            SELECT id_usuario, nome, email, senha_hash
            FROM usuarios
            WHERE email = ?
        """,
            (email,),
        )

        resultado = cursor.fetchone()

        # Fecha a conexão.
        conexao.close()

        # Se não encontrou nenhum usuário, retorna None.
        if resultado is None:
            return None

        # Se encontrou, transforma o resultado do banco em objeto Usuario.
        id_usuario, nome, email, senha_hash = resultado

        return Usuario(
            nome=nome, email=email, senha_hash=senha_hash, id_usuario=id_usuario
        )
