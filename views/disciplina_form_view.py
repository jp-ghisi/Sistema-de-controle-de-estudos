import tkinter as tk
from tkinter import ttk, messagebox

from models.disciplina import Disciplina


class DisciplinaFormView(ttk.Frame):
    def __init__(self, parent, controller, disciplina=None):
        super().__init__(parent, padding=30)

        self._controller = controller
        self._disciplina = disciplina

        # Variáveis ligadas aos campos da interface.
        self._nome_var = tk.StringVar()
        self._professor_var = tk.StringVar()
        self._meta_semanal_var = tk.StringVar()

        # Faz a tela ocupar o espaço disponível.
        self.pack(expand=True, fill="both")

        # Cria os elementos visuais.
        self._criar_widgets()

        # Se for alteração, preenche os campos com os dados da disciplina.
        self._preencher_campos()

    def _criar_widgets(self):
        # Configura as colunas para organizar labels e campos.
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Define o título de acordo com a operação.
        if self._disciplina is None:
            texto_titulo = "Cadastrar Disciplina"
        else:
            texto_titulo = "Alterar Disciplina"

        titulo = ttk.Label(self, text=texto_titulo, font=("Arial", 18, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campo nome da disciplina.
        label_nome = ttk.Label(self, text="Nome:")
        label_nome.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        campo_nome = ttk.Entry(self, textvariable=self._nome_var, width=35)
        campo_nome.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Campo professor.
        label_professor = ttk.Label(self, text="Professor:")
        label_professor.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        campo_professor = ttk.Entry(self, textvariable=self._professor_var, width=35)
        campo_professor.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Campo meta semanal.
        label_meta = ttk.Label(self, text="Meta semanal:")
        label_meta.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        campo_meta = ttk.Entry(self, textvariable=self._meta_semanal_var, width=35)
        campo_meta.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Texto explicativo da meta semanal.
        texto_ajuda = ttk.Label(self, text="Informe a meta semanal em minutos.")
        texto_ajuda.grid(row=4, column=0, columnspan=2, pady=(0, 15))

        # Botão salvar.
        botao_salvar = ttk.Button(self, text="Salvar", command=self._salvar)
        botao_salvar.grid(row=5, column=0, pady=10)

        # Botão cancelar.
        botao_cancelar = ttk.Button(self, text="Cancelar", command=self._cancelar)
        botao_cancelar.grid(row=5, column=1, pady=10)

        # Permite apertar Enter no campo de meta para salvar.
        campo_meta.bind("<Return>", lambda event: self._salvar())

        # Coloca o cursor no campo nome.
        campo_nome.focus()

    def _preencher_campos(self):
        # Preenche os campos quando a tela estiver em modo de alteração.
        if self._disciplina is not None:
            self._nome_var.set(self._disciplina.nome)
            self._professor_var.set(self._disciplina.professor)
            self._meta_semanal_var.set(str(self._disciplina.meta_semanal))

    def _salvar(self):
        # Pega os dados digitados pelo usuário.
        nome = self._nome_var.get().strip()
        professor = self._professor_var.get().strip()
        meta_texto = self._meta_semanal_var.get().strip()

        # Valida se o nome foi preenchido.
        if nome == "":
            messagebox.showwarning("Campo obrigatório", "Informe o nome da disciplina.")
            return

        # Valida se a meta semanal foi preenchida.
        if meta_texto == "":
            messagebox.showwarning("Campo obrigatório", "Informe a meta semanal.")
            return

        # Tenta converter a meta semanal para inteiro.
        try:
            meta_semanal = int(meta_texto)
        except ValueError:
            messagebox.showerror(
                "Meta inválida", "A meta semanal deve ser um número inteiro positivo."
            )
            return

        # Se for cadastro, cria uma nova disciplina.
        if self._disciplina is None:
            disciplina = Disciplina(
                nome=nome, professor=professor, meta_semanal=meta_semanal
            )

        # Se for alteração, mantém o ID da disciplina existente.
        else:
            disciplina = Disciplina(
                nome=nome,
                professor=professor,
                meta_semanal=meta_semanal,
                id_disciplina=self._disciplina.id_disciplina,
            )

        # Pede para o controller salvar no banco.
        sucesso = self._controller.salvar_disciplina(disciplina)

        if sucesso:
            messagebox.showinfo("Disciplina salva", "Disciplina salva com sucesso.")

            # Depois de salvar, volta para a tela principal.
            self._controller.mostrar_tela_principal()

        else:
            messagebox.showerror("Erro", "Não foi possível salvar a disciplina.")

    def _cancelar(self):
        # Cancela a operação e volta para a tela principal.
        self._controller.mostrar_tela_principal()
