import tkinter as tk
from tkinter import ttk, messagebox


class TelaPrincipalView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=30)

        self._controller = controller

        # Variáveis do timer.
        self._tempo_segundos = 0
        self._timer_rodando = False
        self._timer_id = None

        # Listas que serão carregadas do banco depois.
        self._disciplinas = []
        self._atividades = []

        # Variáveis ligadas aos selects da interface.
        self._disciplina_var = tk.StringVar()
        self._atividade_var = tk.StringVar()

        # Faz a tela ocupar o espaço disponível.
        self.pack(expand=True, fill="both")

        # Cria os elementos visuais.
        self._criar_widgets()

        # Carrega as disciplinas no select.
        self._carregar_disciplinas()

    def _criar_widgets(self):
        # Configuração geral das colunas.
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Título da tela.
        titulo = ttk.Label(self, text="Controle de Estudos", font=("Arial", 18, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Label do timer.
        self._label_timer = ttk.Label(self, text="00:00:00", font=("Arial", 28, "bold"))
        self._label_timer.grid(row=1, column=0, columnspan=3, pady=10)

        # Botões do timer.
        self._botao_iniciar = ttk.Button(
            self, text="Iniciar", command=self._iniciar_timer
        )
        self._botao_iniciar.grid(row=2, column=0, pady=10)

        self._botao_pausar = ttk.Button(self, text="Pausar", command=self._pausar_timer)
        self._botao_pausar.grid(row=2, column=1, pady=10)

        self._botao_finalizar = ttk.Button(
            self, text="Finalizar Sessão", command=self._finalizar_sessao
        )
        self._botao_finalizar.grid(row=2, column=2, pady=10)

        # Select de disciplina.
        label_disciplina = ttk.Label(self, text="Disciplina:")
        label_disciplina.grid(row=3, column=0, sticky="e", padx=5, pady=10)

        self._combo_disciplina = ttk.Combobox(
            self, textvariable=self._disciplina_var, state="readonly", width=30
        )
        self._combo_disciplina.grid(row=3, column=1, sticky="w", padx=5, pady=10)

        # Quando o usuário escolher uma disciplina, atualiza as atividades.
        self._combo_disciplina.bind(
            "<<ComboboxSelected>>", lambda event: self._carregar_atividades()
        )

        # Select de atividade.
        label_atividade = ttk.Label(self, text="Atividade:")
        label_atividade.grid(row=4, column=0, sticky="e", padx=5, pady=10)

        self._combo_atividade = ttk.Combobox(
            self, textvariable=self._atividade_var, state="readonly", width=30
        )
        self._combo_atividade.grid(row=4, column=1, sticky="w", padx=5, pady=10)

        # Separador visual.
        separador = ttk.Separator(self, orient="horizontal")
        separador.grid(row=5, column=0, columnspan=3, sticky="ew", pady=20)

        # Botões de CRUD.
        botao_criar_disciplina = ttk.Button(
            self, text="Criar Disciplina", command=self._criar_disciplina
        )
        botao_criar_disciplina.grid(row=6, column=0, padx=5, pady=5)

        botao_criar_atividade = ttk.Button(
            self, text="Criar Atividade", command=self._criar_atividade
        )
        botao_criar_atividade.grid(row=6, column=1, padx=5, pady=5)

        botao_alterar = ttk.Button(self, text="Alterar", command=self._alterar)
        botao_alterar.grid(row=6, column=2, padx=5, pady=5)

        botao_excluir = ttk.Button(self, text="Excluir", command=self._excluir)
        botao_excluir.grid(row=7, column=0, padx=5, pady=5)

        botao_relatorio = ttk.Button(
            self, text="Relatório", command=self._abrir_relatorio
        )
        botao_relatorio.grid(row=7, column=1, padx=5, pady=5)

        botao_sair = ttk.Button(self, text="Sair", command=self._sair)
        botao_sair.grid(row=7, column=2, padx=5, pady=5)

    def _formatar_tempo(self):
        # Converte o tempo em segundos para o formato HH:MM:SS.
        horas = self._tempo_segundos // 3600
        minutos = (self._tempo_segundos % 3600) // 60
        segundos = self._tempo_segundos % 60

        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    def _atualizar_timer(self):
        # Atualiza o timer a cada segundo enquanto ele estiver rodando.
        if self._timer_rodando:
            self._tempo_segundos += 1
            self._label_timer.config(text=self._formatar_tempo())

            # Chama este mesmo método novamente depois de 1000 ms.
            self._timer_id = self.after(1000, self._atualizar_timer)

    def _iniciar_timer(self):
        # Inicia o timer somente se ele ainda não estiver rodando.
        if not self._timer_rodando:
            self._timer_rodando = True
            self._atualizar_timer()

    def _pausar_timer(self):
        # Pausa o timer.
        self._timer_rodando = False

        # Cancela a próxima chamada agendada do timer, se existir.
        if self._timer_id is not None:
            self.after_cancel(self._timer_id)
            self._timer_id = None

    def _zerar_timer(self):
        # Zera o timer visualmente e internamente.
        self._tempo_segundos = 0
        self._label_timer.config(text="00:00:00")

    def _finalizar_sessao(self):
        # Finaliza a sessão de estudo e envia os dados para o controller salvar.
        self._pausar_timer()

        if self._tempo_segundos == 0:
            messagebox.showwarning("Sessão inválida", "O timer ainda está zerado.")
            return

        disciplina = self._obter_disciplina_selecionada()
        atividade = self._obter_atividade_selecionada()

        if disciplina is None:
            messagebox.showwarning(
                "Disciplina obrigatória",
                "Selecione uma disciplina antes de finalizar a sessão.",
            )
            return

        # Converte segundos para minutos.
        # O banco vai armazenar o tempo em minutos.
        tempo_minutos = self._tempo_segundos // 60

        # Se o tempo for menor que 1 minuto, registra como 1 minuto.
        if tempo_minutos == 0:
            tempo_minutos = 1

        sucesso = self._controller.registrar_sessao_estudo(
            disciplina, atividade, tempo_minutos
        )

        if sucesso:
            messagebox.showinfo(
                "Sessão registrada", "Sessão de estudo registrada com sucesso."
            )
            self._zerar_timer()
        else:
            messagebox.showerror(
                "Erro", "Não foi possível registrar a sessão de estudo."
            )

    def _carregar_disciplinas(self):
        # Busca as disciplinas no controller.
        # Depois o controller buscará essas informações no banco.
        self._disciplinas = self._controller.listar_disciplinas()

        # Mostra apenas os nomes das disciplinas no Combobox.
        nomes = [disciplina.nome for disciplina in self._disciplinas]

        self._combo_disciplina["values"] = nomes

        # Se existir pelo menos uma disciplina, seleciona a primeira.
        if len(nomes) > 0:
            self._combo_disciplina.current(0)
            self._carregar_atividades()

        else:
            self._disciplina_var.set("")
            self._atividade_var.set("")

            self._atividades = []

            self._combo_atividade["values"] = []

    def _carregar_atividades(self):
        # Busca a disciplina selecionada.
        disciplina = self._obter_disciplina_selecionada()

        if disciplina is None:
            self._atividades = []
            self._combo_atividade["values"] = ["Nenhuma"]
            self._combo_atividade.current(0)
            return

        # Busca as atividades relacionadas à disciplina.
        self._atividades = self._controller.listar_atividades_por_disciplina(disciplina)

        # A atividade é opcional, então adicionamos "Nenhuma".
        titulos = ["Nenhuma"] + [atividade.titulo for atividade in self._atividades]

        self._combo_atividade["values"] = titulos
        self._combo_atividade.current(0)

    def _obter_disciplina_selecionada(self):
        # Retorna o objeto Disciplina selecionado no Combobox.
        indice = self._combo_disciplina.current()

        if indice < 0 or indice >= len(self._disciplinas):
            return None

        return self._disciplinas[indice]

    def _obter_atividade_selecionada(self):
        # Retorna o objeto Atividade selecionado no Combobox.
        # Se estiver em "Nenhuma", retorna None.
        indice = self._combo_atividade.current()

        if indice <= 0:
            return None

        indice_real = indice - 1

        if indice_real >= len(self._atividades):
            return None

        return self._atividades[indice_real]

    def _criar_disciplina(self):
        # Solicita ao controller a abertura da tela de criação de disciplina.
        self._controller.mostrar_form_disciplina()

    def _criar_atividade(self):
        # Solicita ao controller a abertura da tela de criação de atividade.
        self._controller.mostrar_form_atividade()

    def _alterar(self):
        # Primeiro tenta alterar a atividade selecionada.
        atividade = self._obter_atividade_selecionada()

        if atividade is not None:
            self._controller.mostrar_form_atividade(atividade)
            return

        # Se nenhuma atividade foi selecionada, altera a disciplina.
        disciplina = self._obter_disciplina_selecionada()

        if disciplina is not None:
            self._controller.mostrar_form_disciplina(disciplina)
            return

        messagebox.showwarning(
            "Nenhum item selecionado",
            "Selecione uma disciplina ou atividade para alterar.",
        )

    def _excluir(self):
        # Primeiro tenta excluir a atividade selecionada.
        atividade = self._obter_atividade_selecionada()

        if atividade is not None:
            resposta = messagebox.askyesno(
                "Confirmar exclusão",
                f"Deseja excluir a atividade '{atividade.titulo}'?",
            )

            if resposta:
                self._controller.excluir_atividade(atividade)
                self._carregar_atividades()

            return

        # Se nenhuma atividade foi selecionada, tenta excluir a disciplina.
        disciplina = self._obter_disciplina_selecionada()

        if disciplina is not None:
            resposta = messagebox.askyesno(
                "Confirmar exclusão",
                f"Deseja excluir a disciplina '{disciplina.nome}'?",
            )

            if resposta:
                self._controller.excluir_disciplina(disciplina)
                self._carregar_disciplinas()

            return

        messagebox.showwarning(
            "Nenhum item selecionado",
            "Selecione uma disciplina ou atividade para excluir.",
        )

    def _abrir_relatorio(self):
        # Solicita ao controller a abertura da tela de relatório.
        self._controller.mostrar_relatorio()

    def _sair(self):
        # Para o timer e volta para a tela de login.
        self._pausar_timer()
        self._controller.mostrar_login()
