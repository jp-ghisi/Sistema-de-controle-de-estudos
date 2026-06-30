class Atividade:
    def __init__(
        self,  titulo, id_atividade=None, descricao="", status="pendente", disciplina=None
    ):
        # ID único da atividade no banco de dados.
        self._id_atividade = id_atividade

        # Título da atividade.
        # Exemplo: "Estudar herança em Python".
        self._titulo = titulo

        # Descrição mais detalhada da atividade.
        self._descricao = descricao

        # Status da atividade.
        # Pode ser "pendente", "em andamento" ou "concluída".
        self._status = status

        # Disciplina associada à atividade.
        self._disciplina = disciplina

    @property
    def id_atividade(self):
        return self._id_atividade

    @id_atividade.setter
    def id_atividade(self, id_atividade):
        self._id_atividade = id_atividade

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, titulo):
        self._titulo = titulo

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def disciplina(self):
        return self._disciplina

    @disciplina.setter
    def disciplina(self, disciplina):
        self._disciplina = disciplina
