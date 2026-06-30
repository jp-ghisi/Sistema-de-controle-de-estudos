import tkinter as tk
from tkinter import ttk, messagebox

from models.atividade import Atividade


class AtividadeFormView(ttk.Frame):
    def __init__(self, parent, controller, atividade=None):
        super().__init__(parent, padding=30)

        self._controller = controller
        self._atividade = atividade

        # Lista de disciplinas cadastradas no banco.
        # A atividade precisa estar associada a uma disciplina.
        self._disciplinas = self._controller.listar_disciplinas()

        # Variáveis ligadas aos campos da interface.
        self._titulo_var = tk.StringVar()
        self._descricao_var = tk.StringVar()
        self._status_var = tk.StringVar()
        self._disciplina_var = tk.StringVar()

        # Faz a tela ocupar o espaço disponível.
        self.pack(expand=True, fill="both")

        # Cria os elementos visuais.
        self._criar_widgets()

        # Se for alteração, preenche os campos com os dados da atividade.
        self._preencher_campos()

    def _criar_widgets(self):
        # Configura as colunas para organizar labels e campos.
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Define o título de acordo com a operação.
        if self._atividade is None:
            texto_titulo = "Cadastrar Atividade"
        else:
            texto_titulo = "Alterar Atividade"

        titulo = ttk.Label(self, text=texto_titulo, font=("Arial", 18, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Campo título.
        label_titulo = ttk.Label(self, text="Título:")
        label_titulo.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        campo_titulo = ttk.Entry(self, textvariable=self._titulo_var, width=35)
        campo_titulo.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Campo descrição.
        label_descricao = ttk.Label(self, text="Descrição:")
        label_descricao.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        campo_descricao = ttk.Entry(self, textvariable=self._descricao_var, width=35)
        campo_descricao.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Select de status.
        label_status = ttk.Label(self, text="Status:")
        label_status.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self._combo_status = ttk.Combobox(
            self, textvariable=self._status_var, state="readonly", width=32
        )
        self._combo_status["values"] = ["pendente", "em andamento", "concluída"]
        self._combo_status.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self._combo_status.current(0)

        # Select de disciplina.
        label_disciplina = ttk.Label(self, text="Disciplina:")
        label_disciplina.grid(row=4, column=0, sticky="e", padx=5, pady=5)

        self._combo_disciplina = ttk.Combobox(
            self, textvariable=self._disciplina_var, state="readonly", width=32
        )

        # Mostra no combobox apenas os nomes das disciplinas.
        nomes_disciplinas = [disciplina.nome for disciplina in self._disciplinas]

        self._combo_disciplina["values"] = nomes_disciplinas
        self._combo_disciplina.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Se houver disciplinas cadastradas, seleciona a primeira.
        if len(nomes_disciplinas) > 0:
            self._combo_disciplina.current(0)

        # Texto de aviso.
        texto_ajuda = ttk.Label(
            self, text="A atividade deve estar associada a uma disciplina."
        )
        texto_ajuda.grid(row=5, column=0, columnspan=2, pady=(0, 15))

        # Botão salvar.
        botao_salvar = ttk.Button(self, text="Salvar", command=self._salvar)
        botao_salvar.grid(row=6, column=0, pady=10)

        # Botão cancelar.
        botao_cancelar = ttk.Button(self, text="Cancelar", command=self._cancelar)
        botao_cancelar.grid(row=6, column=1, pady=10)

        # Permite apertar Enter no campo de descrição para salvar.
        campo_descricao.bind("<Return>", lambda event: self._salvar())

        # Coloca o cursor no campo título.
        campo_titulo.focus()

    def _preencher_campos(self):
        # Preenche os campos quando a tela estiver em modo de alteração.
        if self._atividade is not None:
            self._titulo_var.set(self._atividade.titulo)
            self._descricao_var.set(self._atividade.descricao)
            self._status_var.set(self._atividade.status)

            # Seleciona no combobox a disciplina da atividade.
            for indice, disciplina in enumerate(self._disciplinas):
                if disciplina.id_disciplina == self._atividade.disciplina.id_disciplina:
                    self._combo_disciplina.current(indice)
                    break

    def _obter_disciplina_selecionada(self):
        # Retorna o objeto Disciplina selecionado no combobox.
        indice = self._combo_disciplina.current()

        if indice < 0 or indice >= len(self._disciplinas):
            return None

        return self._disciplinas[indice]

    def _salvar(self):
        # Pega os dados digitados pelo usuário.
        titulo = self._titulo_var.get().strip()
        descricao = self._descricao_var.get().strip()
        status = self._status_var.get().strip()
        disciplina = self._obter_disciplina_selecionada()

        # Valida se o título foi preenchido.
        if titulo == "":
            messagebox.showwarning(
                "Campo obrigatório", "Informe o título da atividade."
            )
            return

        # Valida se existe uma disciplina selecionada.
        if disciplina is None:
            messagebox.showwarning(
                "Disciplina obrigatória",
                "Cadastre e selecione uma disciplina antes de salvar a atividade.",
            )
            return

        # Valida se o status foi selecionado.
        if status == "":
            messagebox.showwarning(
                "Status obrigatório", "Selecione o status da atividade."
            )
            return

        # Se for cadastro, cria uma nova atividade.
        if self._atividade is None:
            atividade = Atividade(
                titulo=titulo, descricao=descricao, status=status, disciplina=disciplina
            )

        # Se for alteração, mantém o ID da atividade existente.
        else:
            atividade = Atividade(
                titulo=titulo,
                descricao=descricao,
                status=status,
                disciplina=disciplina,
                id_atividade=self._atividade.id_atividade,
            )

        # Pede para o controller salvar no banco.
        sucesso = self._controller.salvar_atividade(atividade)

        if sucesso:
            messagebox.showinfo("Atividade salva", "Atividade salva com sucesso.")

            # Depois de salvar, volta para a tela principal.
            self._controller.mostrar_tela_principal()

        else:
            messagebox.showerror("Erro", "Não foi possível salvar a atividade.")

    def _cancelar(self):
        # Cancela a operação e volta para a tela principal.
        self._controller.mostrar_tela_principal()
