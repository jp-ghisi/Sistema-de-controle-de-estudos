from database.conexao import conectar
from models.atividade import Atividade
from models.disciplina import Disciplina


class AtividadeRepository:
    def inserir(self, atividade):
        # Salva uma nova atividade no banco
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO atividades (titulo, descricao, status, id_disciplina)
            VALUES (?, ?, ?, ?)
        """,
            (
                atividade.titulo,
                atividade.descricao,
                atividade.status,
                atividade.disciplina.id_disciplina,
            ),
        )

        conexao.commit()

        # Guarda no objeto o ID gerado pelo banco
        atividade.id_atividade = cursor.lastrowid

        conexao.close()

        return True

    def listar_todas(self):
        # Lista todas as atividades com suas respectivas disciplinas
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT 
                a.id_atividade,
                a.titulo,
                a.descricao,
                a.status,
                d.id_disciplina,
                d.nome,
                d.professor,
                d.meta_semanal
            FROM atividades a
            INNER JOIN disciplinas d
                ON a.id_disciplina = d.id_disciplina
            ORDER BY a.titulo
        """)

        resultados = cursor.fetchall()
        conexao.close()

        atividades = []

        for linha in resultados:
            (
                id_atividade,
                titulo,
                descricao,
                status,
                id_disciplina,
                nome_disciplina,
                professor,
                meta_semanal,
            ) = linha

            disciplina = Disciplina(
                nome=nome_disciplina,
                professor=professor,
                meta_semanal=meta_semanal,
                id_disciplina=id_disciplina,
            )

            atividade = Atividade(
                titulo=titulo,
                descricao=descricao,
                status=status,
                disciplina=disciplina,
                id_atividade=id_atividade,
            )

            atividades.append(atividade)

        return atividades

    def listar_por_disciplina(self, disciplina):
        # Lista somente as atividades de uma disciplina específica
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT id_atividade, titulo, descricao, status
            FROM atividades
            WHERE id_disciplina = ?
            ORDER BY titulo
        """,
            (disciplina.id_disciplina,),
        )

        resultados = cursor.fetchall()
        conexao.close()

        atividades = []

        for linha in resultados:
            id_atividade, titulo, descricao, status = linha

            atividade = Atividade(
                titulo=titulo,
                descricao=descricao,
                status=status,
                disciplina=disciplina,
                id_atividade=id_atividade,
            )

            atividades.append(atividade)

        return atividades

    def buscar_por_id(self, id_atividade):
        # Busca uma atividade pelo ID
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT 
                a.id_atividade,
                a.titulo,
                a.descricao,
                a.status,
                d.id_disciplina,
                d.nome,
                d.professor,
                d.meta_semanal
            FROM atividades a
            INNER JOIN disciplinas d
                ON a.id_disciplina = d.id_disciplina
            WHERE a.id_atividade = ?
        """,
            (id_atividade,),
        )

        resultado = cursor.fetchone()
        conexao.close()

        if resultado is None:
            return None

        (
            id_atividade,
            titulo,
            descricao,
            status,
            id_disciplina,
            nome_disciplina,
            professor,
            meta_semanal,
        ) = resultado

        disciplina = Disciplina(
            nome=nome_disciplina,
            professor=professor,
            meta_semanal=meta_semanal,
            id_disciplina=id_disciplina,
        )

        return Atividade(
            titulo=titulo,
            descricao=descricao,
            status=status,
            disciplina=disciplina,
            id_atividade=id_atividade,
        )

    def alterar(self, atividade):
        # Atualiza uma atividade já existente
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE atividades
            SET titulo = ?, descricao = ?, status = ?, id_disciplina = ?
            WHERE id_atividade = ?
        """,
            (
                atividade.titulo,
                atividade.descricao,
                atividade.status,
                atividade.disciplina.id_disciplina,
                atividade.id_atividade,
            ),
        )

        conexao.commit()
        linhas_afetadas = cursor.rowcount

        conexao.close()

        return linhas_afetadas > 0

    def excluir(self, id_atividade):
        # Exclui uma atividade pelo ID
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            DELETE FROM atividades
            WHERE id_atividade = ?
        """,
            (id_atividade,),
        )

        conexao.commit()
        linhas_afetadas = cursor.rowcount

        conexao.close()

        return linhas_afetadas > 0
