import requests
from datetime import date


class FeriadoService:
    # URL base da API de feriados nacionais da BrasilAPI
    BASE_URL = "https://brasilapi.com.br/api/feriados/v1"

    @staticmethod
    def buscar_feriados_por_ano(ano):
        # Busca na API todos os feriados nacionais de um determinado ano.
        try:
            resposta = requests.get(
                f"{FeriadoService.BASE_URL}/{ano}",
                timeout=5
            )

            if resposta.status_code == 200:
                return resposta.json()

            return []

        except requests.RequestException:
            # Se der erro de internet/API, retorna lista vazia
            return []

    @staticmethod
    def buscar_feriado_por_data(data_consulta=None):
        # Verifica se uma data específica é feriado.
        # Se nenhuma data for passada, usa a data atual.
        if data_consulta is None:
            data_consulta = date.today()

        ano = data_consulta.year
        data_texto = data_consulta.isoformat()

        feriados = FeriadoService.buscar_feriados_por_ano(ano)

        for feriado in feriados:
            if feriado.get("date") == data_texto:
                return feriado

        return None

    @staticmethod
    def classificar_data(data_consulta=None):
        # Classifica uma data como:
        # "feriado", "fim de semana" ou "dia útil".
        if data_consulta is None:
            data_consulta = date.today()

        feriado = FeriadoService.buscar_feriado_por_data(data_consulta)

        if feriado is not None:
            return {
                "tipo_dia": "feriado",
                "nome_feriado": feriado.get("name")
            }

        # weekday():
        # 0 = segunda, 1 = terça, ..., 5 = sábado, 6 = domingo
        if data_consulta.weekday() >= 5:
            return {
                "tipo_dia": "fim de semana",
                "nome_feriado": None
            }

        return {
            "tipo_dia": "dia útil",
            "nome_feriado": None
        }