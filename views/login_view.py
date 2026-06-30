import tkinter as tk
from tkinter import ttk, messagebox


class LoginView(ttk.Frame):
    def __init__(self, parent, controller):
        # Inicializa o Frame da tela de login.
        # parent = janela principal onde essa tela será exibida.
        # controller = classe principal do app, responsável por trocar telas.
        super().__init__(parent, padding=30)

        self._controller = controller

        # Variáveis ligadas aos campos da interface.
        self._email_var = tk.StringVar()
        self._senha_var = tk.StringVar()

        # Faz a tela ocupar o espaço disponível.
        self.pack(expand=True, fill="both")

        # Cria os elementos visuais da tela.
        self._criar_widgets()

    def _criar_widgets(self):
        # Configura as colunas para centralizar melhor os elementos.
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Título da tela.
        titulo = ttk.Label(self, text="Controle de Estudos", font=("Arial", 18, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campo de email.
        label_email = ttk.Label(self, text="Email:")
        label_email.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        campo_email = ttk.Entry(self, textvariable=self._email_var, width=30)
        campo_email.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Campo de senha.
        label_senha = ttk.Label(self, text="Senha:")
        label_senha.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        campo_senha = ttk.Entry(self, textvariable=self._senha_var, width=30, show="*")
        campo_senha.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Botão para realizar login.
        botao_entrar = ttk.Button(self, text="Entrar", command=self._fazer_login)
        botao_entrar.grid(row=3, column=0, columnspan=2, pady=(15, 5))

        # Botão para abrir a tela de cadastro.
        botao_cadastro = ttk.Button(
            self, text="Criar conta", command=self._abrir_cadastro
        )
        botao_cadastro.grid(row=4, column=0, columnspan=2, pady=5)

        # Permite apertar Enter para fazer login.
        campo_senha.bind("<Return>", lambda event: self._fazer_login())

        # Coloca o cursor inicialmente no campo de email.
        campo_email.focus()

    def _fazer_login(self):
        # Pega os valores digitados pelo usuário.
        email = self._email_var.get().strip()
        senha = self._senha_var.get().strip()

        # Validação simples para impedir campos vazios.
        if email == "" or senha == "":
            messagebox.showwarning("Campos obrigatórios", "Preencha o email e a senha.")
            return

        # Chama o controller para verificar o login.
        # Essa função será criada depois na classe principal do app.
        login_valido = self._controller.autenticar_usuario(email, senha)

        if login_valido:
            messagebox.showinfo("Login realizado", "Login realizado com sucesso.")

            # Após login correto, abre a tela principal.
            self._controller.mostrar_tela_principal()
        else:
            messagebox.showerror("Erro no login", "Email ou senha incorretos.")

    def _abrir_cadastro(self):
        # Solicita ao controller a troca para a tela de cadastro.
        self._controller.mostrar_cadastro()

    def limpar_campos(self):
        # Limpa os campos da tela de login.
        self._email_var.set("")
        self._senha_var.set("")
