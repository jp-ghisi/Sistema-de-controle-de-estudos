import hashlib
import os


class AuthService:
    @staticmethod
    def gerar_hash_senha(senha):
        # Gera um salt aleatório.
        # O salt impede que senhas iguais gerem exatamente o mesmo hash.
        salt = os.urandom(16)

        # Gera o hash da senha usando PBKDF2 com SHA-256.
        hash_senha = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, 100000)

        # Converte salt e hash para hexadecimal para salvar no banco como texto.
        salt_hex = salt.hex()
        hash_hex = hash_senha.hex()

        # Salva tudo em uma única string.
        # Formato: salt$hash
        return f"{salt_hex}${hash_hex}"

    @staticmethod
    def verificar_senha(senha_digitada, senha_hash_salva):
        # Separa o salt e o hash que estavam salvos no banco.
        salt_hex, hash_salvo_hex = senha_hash_salva.split("$")

        # Converte o salt de hexadecimal para bytes.
        salt = bytes.fromhex(salt_hex)

        # Gera novamente o hash usando a senha digitada e o mesmo salt.
        hash_teste = hashlib.pbkdf2_hmac(
            "sha256", senha_digitada.encode("utf-8"), salt, 100000
        )

        # Compara o hash gerado agora com o hash salvo no banco.
        return hash_teste.hex() == hash_salvo_hex
