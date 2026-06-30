from datetime import date


class SessaoEstudo:
    def __init__(
        self,
        usuario,
        disciplina,
        id_sessao=None,
        atividade=None,
        tempo_minutos=0,
        data_estudo=None,
        tipo_dia="dia útil",
        nome_feriado=None,
    ):
        # ID único da sessão de estudo no banco de dados.
        self._id_sessao = id_sessao

        # Usuário dono da sessão de estudo.
        # Aqui temos uma associação entre SessaoEstudo e Usuario.
        self._usuario = usuario

        # Disciplina estudada na sessão.
        # Aqui temos uma associação entre SessaoEstudo e Disciplina.
        self._disciplina = disciplina

        # Atividade relacionada à sessão.
        # Pode ser None, pois o usuário pode estudar sem escolher uma atividade específica.
        self._atividade = atividade

        # Tempo total estudado em minutos.
        self._tempo_minutos = tempo_minutos

        # Data da sessão de estudo.
        # Se nenhuma data for passada, usa a data atual.
        self._data_estudo = data_estudo if data_estudo is not None else date.today()

        # Tipo do dia: "dia útil", "fim de semana" ou "feriado".
        self._tipo_dia = tipo_dia

        # Nome do feriado, caso a sessão tenha ocorrido em um feriado.
        # Em dias normais, esse valor pode ser None.
        self._nome_feriado = nome_feriado

    @property
    def id_sessao(self):
        return self._id_sessao

    @id_sessao.setter
    def id_sessao(self, id_sessao):
        self._id_sessao = id_sessao

    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, usuario):
        self._usuario = usuario

    @property
    def disciplina(self):
        return self._disciplina

    @disciplina.setter
    def disciplina(self, disciplina):
        self._disciplina = disciplina

    @property
    def atividade(self):
        return self._atividade

    @atividade.setter
    def atividade(self, atividade):
        self._atividade = atividade

    @property
    def tempo_minutos(self):
        return self._tempo_minutos

    @tempo_minutos.setter
    def tempo_minutos(self, tempo_minutos):
        self._tempo_minutos = tempo_minutos

    @property
    def data_estudo(self):
        return self._data_estudo

    @data_estudo.setter
    def data_estudo(self, data_estudo):
        self._data_estudo = data_estudo

    @property
    def tipo_dia(self):
        return self._tipo_dia

    @tipo_dia.setter
    def tipo_dia(self, tipo_dia):
        self._tipo_dia = tipo_dia

    @property
    def nome_feriado(self):
        return self._nome_feriado

    @nome_feriado.setter
    def nome_feriado(self, nome_feriado):
        self._nome_feriado = nome_feriado
