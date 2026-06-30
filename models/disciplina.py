class Disciplina:
    def __init__(self, nome, professor="", meta_semanal=0, id_disciplina=None):
        # ID único da disciplina no banco de dados.
        self._id_disciplina = id_disciplina

        # Nome da disciplina, por exemplo: "POO II".
        self._nome = nome

        # Nome do professor da disciplina.
        # Pode ficar vazio caso o usuário não queira informar.
        self._professor = professor

        # Meta semanal de estudo em minutos.
        self._meta_semanal = meta_semanal

    def formatar_meta_semanal(self):
        # Converte a meta semanal de minutos para um texto mais legível.
        # Exemplo: 120 vira "2h", 90 vira "1h30min".

        if self._meta_semanal < 60:
            return f"{self._meta_semanal}min"

        horas = self._meta_semanal // 60
        minutos = self._meta_semanal % 60

        if minutos == 0:
            return f"{horas}h"

        return f"{horas}h{minutos}min"

    @property
    def id_disciplina(self):
        return self._id_disciplina

    @id_disciplina.setter
    def id_disciplina(self, id_disciplina):
        self._id_disciplina = id_disciplina

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def professor(self):
        return self._professor

    @professor.setter
    def professor(self, professor):
        self._professor = professor

    @property
    def meta_semanal(self):
        return self._meta_semanal

    @meta_semanal.setter
    def meta_semanal(self, meta_semanal):
        # Só permite alterar a meta semanal se ela for um inteiro positivo
        if not Disciplina.validar_meta_semanal(meta_semanal):
            raise ValueError(
                "Meta semanal inválida. A meta deve ser um número inteiro positivo."
            )
        self._meta_semanal = meta_semanal
