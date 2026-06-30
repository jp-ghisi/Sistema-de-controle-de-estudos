from database.conexao import conectar


class SessaoEstudoRepository:
    def inserir(self, sessao):
        # Salva uma sessão de estudo no banco
        conexao = conectar()
        cursor = conexao.cursor()

        # A atividade é opcional.
        # Se não houver atividade, salvamos None no banco.
        id_atividade = None

        if sessao.atividade is not None:
            id_atividade = sessao.atividade.id_atividade

        cursor.execute(
            """
            INSERT INTO sessoes_estudo (
                id_usuario,
                id_disciplina,
                id_atividade,
                tempo_minutos,
                data_estudo,
                tipo_dia,
                nome_feriado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                sessao.usuario.id_usuario,
                sessao.disciplina.id_disciplina,
                id_atividade,
                sessao.tempo_minutos,
                str(sessao.data_estudo),
                sessao.tipo_dia,
                sessao.nome_feriado,
            ),
        )

        conexao.commit()

        # Guarda no objeto o ID gerado pelo banco
        sessao.id_sessao = cursor.lastrowid

        conexao.close()

        return True

    def listar_por_usuario(self, id_usuario):
        # Lista as sessões de estudo de um usuário.
        # Retorna dicionários porque isso facilita a criação do relatório depois.
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT
                s.id_sessao,
                s.tempo_minutos,
                s.data_estudo,
                s.tipo_dia,
                s.nome_feriado,
                d.nome AS nome_disciplina,
                a.titulo AS titulo_atividade
            FROM sessoes_estudo s
            INNER JOIN disciplinas d
                ON s.id_disciplina = d.id_disciplina
            LEFT JOIN atividades a
                ON s.id_atividade = a.id_atividade
            WHERE s.id_usuario = ?
            ORDER BY s.data_estudo DESC
        """,
            (id_usuario,),
        )

        resultados = cursor.fetchall()
        conexao.close()

        sessoes = []

        for linha in resultados:
            (
                id_sessao,
                tempo_minutos,
                data_estudo,
                tipo_dia,
                nome_feriado,
                nome_disciplina,
                titulo_atividade,
            ) = linha

            sessoes.append(
                {
                    "id_sessao": id_sessao,
                    "tempo_minutos": tempo_minutos,
                    "data_estudo": data_estudo,
                    "tipo_dia": tipo_dia,
                    "nome_feriado": nome_feriado,
                    "disciplina": nome_disciplina,
                    "atividade": titulo_atividade,
                }
            )

        return sessoes

    def total_por_disciplina(self, id_usuario):
        # Calcula o tempo total estudado por disciplina
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT
                d.nome,
                SUM(s.tempo_minutos) AS total_minutos
            FROM sessoes_estudo s
            INNER JOIN disciplinas d
                ON s.id_disciplina = d.id_disciplina
            WHERE s.id_usuario = ?
            GROUP BY d.nome
            ORDER BY total_minutos DESC
        """,
            (id_usuario,),
        )

        resultados = cursor.fetchall()
        conexao.close()

        return resultados

    def total_por_tipo_dia(self, id_usuario):
        # Calcula o tempo total estudado em dia útil, fim de semana e feriado
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT
                tipo_dia,
                SUM(tempo_minutos) AS total_minutos
            FROM sessoes_estudo
            WHERE id_usuario = ?
            GROUP BY tipo_dia
            ORDER BY total_minutos DESC
        """,
            (id_usuario,),
        )

        resultados = cursor.fetchall()
        conexao.close()

        return resultados

    def excluir(self, id_sessao):
        # Exclui uma sessão de estudo pelo ID
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            DELETE FROM sessoes_estudo
            WHERE id_sessao = ?
        """,
            (id_sessao,),
        )

        conexao.commit()
        linhas_afetadas = cursor.rowcount

        conexao.close()

        return linhas_afetadas > 0
