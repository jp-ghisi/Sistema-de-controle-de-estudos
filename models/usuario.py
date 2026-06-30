class Usuario:
    def __init__(self, nome, email, senha_hash, id_usuario=None):
        # Nome do usuário.
        self._nome = nome

        # Email usado para login.
        if not Usuario.validar_email(email):
            raise ValueError("Email inválido. O email deve conter '@' e '.com'.")
        self._email = email

        # Senha criptografada com hash.

        self._senha_hash = senha_hash

        # ID único do usuário no banco de dados.
        # Quando o usuário ainda não foi salvo no banco, pode ser None.
        self._id_usuario = id_usuario

    # Método estático porque não depende de um usuário já criado.
    # Ele serve para verificar se uma senha digitada é forte.
    @staticmethod
    def validar_senha_forte(senha):
        # Verifica se a senha tem pelo menos 8 caracteres
        if len(senha) < 8:
            return False

        # Verifica se existe pelo menos uma letra maiúscula
        tem_maiuscula = any(caractere.isupper() for caractere in senha)

        # Verifica se existe pelo menos uma letra minúscula
        tem_minuscula = any(caractere.islower() for caractere in senha)

        # Verifica se existe pelo menos um número
        tem_numero = any(caractere.isdigit() for caractere in senha)

        # Verifica se existe pelo menos um caractere especial
        tem_especial = any(not caractere.isalnum() for caractere in senha)

        return tem_maiuscula and tem_minuscula and tem_numero and tem_especial

    @staticmethod
    def validar_email(email):
        # Verifica se o email possui "@" e ".com"
        return "@" in email and ".com" in email

    @property
    def id_usuario(self):
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, id_usuario):
        self._id_usuario = id_usuario

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        # Só permite alterar o email se ele for válido
        if not Usuario.validar_email(email):
            raise ValueError("Email inválido. O email deve conter '@' e '.com'.")
        self._email = email

    @property
    def senha_hash(self):
        return self._senha_hash

    @senha_hash.setter
    def senha_hash(self, senha_hash):
        self._senha_hash = senha_hash
