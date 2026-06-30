import tkinter as tk
from tkinter import ttk

from database.criar_tabelas import criar_tabelas

from models.usuario import Usuario
from models.sessao_estudo import SessaoEstudo

from repositories.usuario_repository import UsuarioRepository
from repositories.disciplina_repository import DisciplinaRepository
from repositories.atividade_repository import AtividadeRepository
from repositories.sessao_estudo_repository import SessaoEstudoRepository

from services.auth_service import AuthService
from services.feriado_service import FeriadoService

from views.login_view import LoginView
from views.cadastro_view import CadastroView
from views.tela_principal_view import TelaPrincipalView
from views.disciplina_form_view import DisciplinaFormView
from views.atividade_form_view import AtividadeFormView
from views.relatorio_view import RelatorioView


class App:
    def __init__(self):
        # Cria a janela principal do sistema.
        self._janela = tk.Tk()

        # Define o título da janela.
        self._janela.title("Controle de Estudos")

        # Define o tamanho inicial da janela.
        self._janela.geometry("600x400")

        # Impede que a janela comece muito pequena.
        self._janela.minsize(500, 350)

        # Guarda qual tela está sendo exibida no momento.
        self._tela_atual = None

        # Cria as tabelas do banco caso ainda não existam.
        criar_tabelas()

        # Repositórios usados para acessar o banco de dados
        self._usuario_repository = UsuarioRepository()
        self._disciplina_repository = DisciplinaRepository()
        self._atividade_repository = AtividadeRepository()
        self._sessao_repository = SessaoEstudoRepository()

        # Usuário atualmente logado no sistema
        self._usuario_logado = None

        # Mostra a tela de login ao iniciar o sistema.
        self.mostrar_login()

        # Mantém a janela aberta.
        self._janela.mainloop()

    def _limpar_tela(self):
        # Remove a tela atual antes de abrir outra.
        if self._tela_atual is not None:
            self._tela_atual.destroy()

    def mostrar_login(self):
        # Exibe a tela de login.
        self._limpar_tela()
        self._tela_atual = LoginView(self._janela, self)

    def mostrar_cadastro(self):
        # Exibe a tela de cadastro.
        self._limpar_tela()
        self._tela_atual = CadastroView(self._janela, self)

    def mostrar_tela_principal(self):
        # Exibe a tela principal do sistema.
        self._limpar_tela()
        self._tela_atual = TelaPrincipalView(self._janela, self)

    def cadastrar_usuario(self, nome, email, senha):
        # Gera o hash da senha.
        senha_hash = AuthService.gerar_hash_senha(senha)

        # Cria o objeto Usuario.
        usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)

        # Salva o usuário no banco.
        return self._usuario_repository.inserir(usuario)

    def autenticar_usuario(self, email, senha):
        # Busca o usuário no banco pelo email.
        usuario = self._usuario_repository.buscar_por_email(email)

        # Se não encontrou usuário com esse email, login falha.
        if usuario is None:
            return False

        # Verifica se a senha digitada corresponde ao hash salvo.
        senha_correta = AuthService.verificar_senha(senha, usuario.senha_hash)

        if senha_correta:
            # Guarda o usuário logado para usar depois nas sessões de estudo
            self._usuario_logado = usuario
            return True

        return False

    def listar_disciplinas(self):
        # Retorna todas as disciplinas salvas no banco
        return self._disciplina_repository.listar_todas()

    def listar_atividades_por_disciplina(self, disciplina):
        # Retorna as atividades associadas à disciplina selecionada
        return self._atividade_repository.listar_por_disciplina(disciplina)

    def registrar_sessao_estudo(self, disciplina, atividade, tempo_minutos):
        classificacao = FeriadoService.classificar_data()

        tipo_dia = classificacao["tipo_dia"]
        nome_feriado = classificacao["nome_feriado"]

        # Cria o objeto SessaoEstudo
        sessao = SessaoEstudo(
            usuario=self._usuario_logado,
            disciplina=disciplina,
            atividade=atividade,
            tempo_minutos=tempo_minutos,
            tipo_dia=tipo_dia,
            nome_feriado=nome_feriado,
        )

        # Salva a sessão no banco
        return self._sessao_repository.inserir(sessao)

    def mostrar_form_disciplina(self, disciplina=None):
        # Exibe a tela de cadastro ou alteração de disciplina.
        self._limpar_tela()
        self._tela_atual = DisciplinaFormView(self._janela, self, disciplina)

    def salvar_disciplina(self, disciplina):
        # Se a disciplina ainda não tem ID, é um novo cadastro.
        if disciplina.id_disciplina is None:
            return self._disciplina_repository.inserir(disciplina)

        # Se já tem ID, é uma alteração.
        return self._disciplina_repository.alterar(disciplina)

    def mostrar_form_atividade(self, atividade=None):
        # Exibe a tela de cadastro ou alteração de atividade.
        self._limpar_tela()
        self._tela_atual = AtividadeFormView(self._janela, self, atividade)

    def salvar_atividade(self, atividade):
        # Se a atividade ainda não tem ID, é um novo cadastro.
        if atividade.id_atividade is None:
            return self._atividade_repository.inserir(atividade)

        # Se já tem ID, é uma alteração.
        return self._atividade_repository.alterar(atividade)

    def excluir_disciplina(self, disciplina):
        # Exclui a disciplina selecionada
        return self._disciplina_repository.excluir(disciplina.id_disciplina)

    def excluir_atividade(self, atividade):
        # Exclui a atividade selecionada
        return self._atividade_repository.excluir(atividade.id_atividade)

    def mostrar_relatorio(self):
        # Exibe a tela de relatório.
        self._limpar_tela()
        self._tela_atual = RelatorioView(self._janela, self)

    def listar_sessoes_usuario(self):
        # Lista as sessões de estudo do usuário logado.
        return self._sessao_repository.listar_por_usuario(
            self._usuario_logado.id_usuario
        )

    def total_estudado_por_disciplina(self):
        # Retorna o total de minutos estudados agrupado por disciplina.
        return self._sessao_repository.total_por_disciplina(
            self._usuario_logado.id_usuario
        )

    def total_estudado_por_tipo_dia(self):
        # Retorna o total de minutos estudados agrupado por tipo de dia.
        return self._sessao_repository.total_por_tipo_dia(
            self._usuario_logado.id_usuario
        )

if __name__ == "__main__":
    App()
