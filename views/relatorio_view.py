import tkinter as tk
from tkinter import ttk


class RelatorioView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)

        self._controller = controller

        # Busca os dados do relatório no banco por meio do controller.
        self._sessoes = self._controller.listar_sessoes_usuario()
        self._total_por_disciplina = self._controller.total_estudado_por_disciplina()
        self._total_por_tipo_dia = self._controller.total_estudado_por_tipo_dia()

        # Faz a tela ocupar o espaço disponível.
        self.pack(expand=True, fill="both")

        # Cria os elementos visuais da tela.
        self._criar_widgets()

    def _criar_widgets(self):
        # Configura a tela para expandir corretamente.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Título da tela.
        titulo = ttk.Label(
            self, text="Relatório de Estudos", font=("Arial", 18, "bold")
        )
        titulo.grid(row=0, column=0, pady=(0, 15))

        # Cria o resumo geral.
        self._criar_resumo_geral()

        # Cria a tabela com as sessões de estudo.
        self._criar_tabela_sessoes()

        # Cria as tabelas de totais.
        self._criar_tabelas_totais()

        # Botão para voltar para a tela principal.
        botao_voltar = ttk.Button(self, text="Voltar", command=self._voltar)
        botao_voltar.grid(row=4, column=0, pady=15)

    def _criar_resumo_geral(self):
        # Frame para organizar os dados principais do relatório.
        frame_resumo = ttk.LabelFrame(self, text="Resumo Geral", padding=10)
        frame_resumo.grid(row=1, column=0, sticky="ew", pady=10)

        frame_resumo.columnconfigure(0, weight=1)
        frame_resumo.columnconfigure(1, weight=1)
        frame_resumo.columnconfigure(2, weight=1)

        # Calcula o tempo total estudado somando todas as sessões.
        total_minutos = 0

        for sessao in self._sessoes:
            total_minutos += sessao["tempo_minutos"]

        quantidade_sessoes = len(self._sessoes)

        # Exibe quantidade de sessões.
        label_sessoes = ttk.Label(
            frame_resumo, text=f"Sessões registradas: {quantidade_sessoes}"
        )
        label_sessoes.grid(row=0, column=0, padx=10, pady=5)

        # Exibe tempo total estudado.
        label_tempo = ttk.Label(
            frame_resumo, text=f"Tempo total: {self._formatar_minutos(total_minutos)}"
        )
        label_tempo.grid(row=0, column=1, padx=10, pady=5)

        # Exibe quantidade de disciplinas estudadas.
        label_disciplinas = ttk.Label(
            frame_resumo,
            text=f"Disciplinas estudadas: {len(self._total_por_disciplina)}",
        )
        label_disciplinas.grid(row=0, column=2, padx=10, pady=5)

    def _criar_tabela_sessoes(self):
        # Frame para a tabela principal de sessões.
        frame_sessoes = ttk.LabelFrame(self, text="Sessões de Estudo", padding=10)
        frame_sessoes.grid(row=2, column=0, sticky="nsew", pady=10)

        frame_sessoes.columnconfigure(0, weight=1)
        frame_sessoes.rowconfigure(0, weight=1)

        # Colunas da tabela.
        colunas = ("data", "disciplina", "atividade", "tempo", "tipo_dia", "feriado")

        self._tree_sessoes = ttk.Treeview(
            frame_sessoes, columns=colunas, show="headings", height=8
        )

        # Define os títulos das colunas.
        self._tree_sessoes.heading("data", text="Data")
        self._tree_sessoes.heading("disciplina", text="Disciplina")
        self._tree_sessoes.heading("atividade", text="Atividade")
        self._tree_sessoes.heading("tempo", text="Tempo")
        self._tree_sessoes.heading("tipo_dia", text="Tipo do dia")
        self._tree_sessoes.heading("feriado", text="Feriado")

        # Define larguras das colunas.
        self._tree_sessoes.column("data", width=90, anchor="center")
        self._tree_sessoes.column("disciplina", width=150)
        self._tree_sessoes.column("atividade", width=150)
        self._tree_sessoes.column("tempo", width=80, anchor="center")
        self._tree_sessoes.column("tipo_dia", width=100, anchor="center")
        self._tree_sessoes.column("feriado", width=120)

        # Barra de rolagem vertical.
        scrollbar = ttk.Scrollbar(
            frame_sessoes, orient="vertical", command=self._tree_sessoes.yview
        )

        self._tree_sessoes.configure(yscrollcommand=scrollbar.set)

        self._tree_sessoes.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Preenche a tabela com os dados vindos do banco.
        self._preencher_tabela_sessoes()

    def _preencher_tabela_sessoes(self):
        # Caso não existam sessões registradas, mostra uma linha informativa.
        if len(self._sessoes) == 0:
            self._tree_sessoes.insert(
                "", "end", values=("—", "Nenhuma sessão registrada", "—", "—", "—", "—")
            )
            return

        for sessao in self._sessoes:
            atividade = sessao["atividade"]

            if atividade is None:
                atividade = "Nenhuma"

            nome_feriado = sessao["nome_feriado"]

            if nome_feriado is None:
                nome_feriado = "—"

            self._tree_sessoes.insert(
                "",
                "end",
                values=(
                    sessao["data_estudo"],
                    sessao["disciplina"],
                    atividade,
                    self._formatar_minutos(sessao["tempo_minutos"]),
                    sessao["tipo_dia"],
                    nome_feriado,
                ),
            )

    def _criar_tabelas_totais(self):
        # Frame geral para colocar os totais lado a lado.
        frame_totais = ttk.Frame(self)
        frame_totais.grid(row=3, column=0, sticky="ew", pady=10)

        frame_totais.columnconfigure(0, weight=1)
        frame_totais.columnconfigure(1, weight=1)

        self._criar_total_por_disciplina(frame_totais)
        self._criar_total_por_tipo_dia(frame_totais)

    def _criar_total_por_disciplina(self, parent):
        # Frame do total por disciplina.
        frame = ttk.LabelFrame(parent, text="Tempo por Disciplina", padding=10)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        colunas = ("disciplina", "tempo")

        tree = ttk.Treeview(frame, columns=colunas, show="headings", height=5)

        tree.heading("disciplina", text="Disciplina")
        tree.heading("tempo", text="Tempo")

        tree.column("disciplina", width=180)
        tree.column("tempo", width=100, anchor="center")

        tree.pack(expand=True, fill="both")

        if len(self._total_por_disciplina) == 0:
            tree.insert("", "end", values=("Nenhuma disciplina", "—"))
            return

        for nome_disciplina, total_minutos in self._total_por_disciplina:
            tree.insert(
                "",
                "end",
                values=(nome_disciplina, self._formatar_minutos(total_minutos)),
            )

    def _criar_total_por_tipo_dia(self, parent):
        # Frame do total por tipo de dia.
        frame = ttk.LabelFrame(parent, text="Tempo por Tipo de Dia", padding=10)
        frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        colunas = ("tipo_dia", "tempo")

        tree = ttk.Treeview(frame, columns=colunas, show="headings", height=5)

        tree.heading("tipo_dia", text="Tipo do dia")
        tree.heading("tempo", text="Tempo")

        tree.column("tipo_dia", width=180)
        tree.column("tempo", width=100, anchor="center")

        tree.pack(expand=True, fill="both")

        if len(self._total_por_tipo_dia) == 0:
            tree.insert("", "end", values=("Nenhum registro", "—"))
            return

        for tipo_dia, total_minutos in self._total_por_tipo_dia:
            tree.insert(
                "", "end", values=(tipo_dia, self._formatar_minutos(total_minutos))
            )

    def _formatar_minutos(self, minutos):
        # Converte minutos para um texto mais legível.
        if minutos < 60:
            return f"{minutos}min"

        horas = minutos // 60
        minutos_restantes = minutos % 60

        if minutos_restantes == 0:
            return f"{horas}h"

        return f"{horas}h{minutos_restantes}min"

    def _voltar(self):
        # Volta para a tela principal.
        self._controller.mostrar_tela_principal()
