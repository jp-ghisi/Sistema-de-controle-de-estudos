import tkinter as tk
from tkinter import ttk, messagebox

from models.usuario import Usuario


class CadastroView(ttk.Frame):
    def __init__(self, parent, controller):
        # Inicializa o Frame da tela de cadastro.
        # parent = janela principal.
        # controller = classe App, responsável por trocar telas e cadastrar usuários.
        super().__init__(parent, padding=30)

        self._controller = controller

        # Variáveis que armazenam os valores digitados nos campos.
        self._nome_var = tk.StringVar()
        self._email_var = tk.StringVar()
        self._senha_var = tk.StringVar()
        self._confirmar_senha_var = tk.StringVar()

        # Faz a tela ocupar o espaço disponível.
        self.pack(expand=True, fill="both")

        # Cria os elementos visuais da tela.
        self._criar_widgets()

    def _criar_widgets(self):
        # Configura duas colunas para organizar os labels e campos.
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Título da tela.
        titulo = ttk.Label(self, text="Cadastro de Usuário", font=("Arial", 18, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campo de nome.
        label_nome = ttk.Label(self, text="Nome:")
        label_nome.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        campo_nome = ttk.Entry(self, textvariable=self._nome_var, width=30)
        campo_nome.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Campo de email.
        label_email = ttk.Label(self, text="Email:")
        label_email.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        campo_email = ttk.Entry(self, textvariable=self._email_var, width=30)
        campo_email.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Campo de senha.
        label_senha = ttk.Label(self, text="Senha:")
        label_senha.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        campo_senha = ttk.Entry(self, textvariable=self._senha_var, width=30, show="*")
        campo_senha.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Campo de confirmação de senha.
        label_confirmar = ttk.Label(self, text="Confirmar senha:")
        label_confirmar.grid(row=4, column=0, sticky="e", padx=5, pady=5)

        campo_confirmar = ttk.Entry(
            self, textvariable=self._confirmar_senha_var, width=30, show="*"
        )
        campo_confirmar.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Botão para cadastrar.
        botao_cadastrar = ttk.Button(self, text="Cadastrar", command=self._cadastrar)
        botao_cadastrar.grid(row=5, column=0, columnspan=2, pady=(15, 5))

        # Botão para voltar para a tela de login.
        botao_voltar = ttk.Button(
            self, text="Voltar para Login", command=self._voltar_login
        )
        botao_voltar.grid(row=6, column=0, columnspan=2, pady=5)

        # Permite apertar Enter no último campo para cadastrar.
        campo_confirmar.bind("<Return>", lambda event: self._cadastrar())

        # Coloca o cursor inicialmente no campo de nome.
        campo_nome.focus()

    def _cadastrar(self):
        # Pega os valores digitados pelo usuário.
        nome = self._nome_var.get().strip()
        email = self._email_var.get().strip()
        senha = self._senha_var.get().strip()
        confirmar_senha = self._confirmar_senha_var.get().strip()

        # Verifica se todos os campos foram preenchidos.
        if nome == "" or email == "" or senha == "" or confirmar_senha == "":
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        # Valida o formato do email usando o método da classe Usuario.
        if not Usuario.validar_email(email):
            messagebox.showerror("Email inválido", "O email deve conter '@' e '.com'.")
            return

        # Verifica se a senha e a confirmação são iguais.
        if senha != confirmar_senha:
            messagebox.showerror(
                "Senhas diferentes",
                "A senha e a confirmação de senha devem ser iguais.",
            )
            return

        # Valida se a senha é forte usando o método da classe Usuario.
        if not Usuario.validar_senha_forte(senha):
            messagebox.showerror(
                "Senha fraca",
                "A senha deve ter pelo menos 8 caracteres, uma letra maiúscula, "
                "uma letra minúscula, um número e um caractere especial.",
            )
            return

        # Solicita ao controller o cadastro do usuário.
        # Depois, o controller vai gerar o hash da senha e salvar no banco.
        cadastro_realizado = self._controller.cadastrar_usuario(nome, email, senha)

        if cadastro_realizado:
            messagebox.showinfo("Cadastro realizado", "Usuário cadastrado com sucesso.")

            # Após cadastrar, volta para a tela de login.
            self._controller.mostrar_login()
        else:
            messagebox.showerror(
                "Erro no cadastro", "Não foi possível cadastrar o usuário."
            )

    def _voltar_login(self):
        # Volta para a tela de login sem cadastrar.
        self._controller.mostrar_login()

    def limpar_campos(self):
        # Limpa todos os campos da tela de cadastro.
        self._nome_var.set("")
        self._email_var.set("")
        self._senha_var.set("")
        self._confirmar_senha_var.set("")
