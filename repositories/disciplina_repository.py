from database.conexao import conectar
from models.disciplina import Disciplina


class DisciplinaRepository:
    def inserir(self, disciplina):
        # Salva uma nova disciplina no banco
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO disciplinas (nome, professor, meta_semanal)
            VALUES (?, ?, ?)
        """,
            (disciplina.nome, disciplina.professor, disciplina.meta_semanal),
        )

        conexao.commit()

        # Guarda no objeto o ID gerado pelo banco
        disciplina.id_disciplina = cursor.lastrowid

        conexao.close()

        return True

    def listar_todas(self):
        # Lista todas as disciplinas cadastradas
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id_disciplina, nome, professor, meta_semanal
            FROM disciplinas
            ORDER BY nome
        """)

        resultados = cursor.fetchall()
        conexao.close()

        disciplinas = []

        for linha in resultados:
            id_disciplina, nome, professor, meta_semanal = linha

            disciplina = Disciplina(
                nome=nome,
                professor=professor,
                meta_semanal=meta_semanal,
                id_disciplina=id_disciplina,
            )

            disciplinas.append(disciplina)

        return disciplinas

    def buscar_por_id(self, id_disciplina):
        # Busca uma disciplina específica pelo ID
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT id_disciplina, nome, professor, meta_semanal
            FROM disciplinas
            WHERE id_disciplina = ?
        """,
            (id_disciplina,),
        )

        resultado = cursor.fetchone()
        conexao.close()

        if resultado is None:
            return None

        id_disciplina, nome, professor, meta_semanal = resultado

        return Disciplina(
            nome=nome,
            professor=professor,
            meta_semanal=meta_semanal,
            id_disciplina=id_disciplina,
        )

    def alterar(self, disciplina):
        # Atualiza os dados de uma disciplina já existente
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE disciplinas
            SET nome = ?, professor = ?, meta_semanal = ?
            WHERE id_disciplina = ?
        """,
            (
                disciplina.nome,
                disciplina.professor,
                disciplina.meta_semanal,
                disciplina.id_disciplina,
            ),
        )

        conexao.commit()
        linhas_afetadas = cursor.rowcount

        conexao.close()

        return linhas_afetadas > 0

    def excluir(self, id_disciplina):
        # Exclui uma disciplina pelo ID
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            DELETE FROM disciplinas
            WHERE id_disciplina = ?
        """,
            (id_disciplina,),
        )

        conexao.commit()
        linhas_afetadas = cursor.rowcount

        conexao.close()

        return linhas_afetadas > 0
