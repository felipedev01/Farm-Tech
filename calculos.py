import math


def calcular_qtd_ruas(largura_util: float, espacamento: float, largura_rua: float) -> int:
    faixa_ocupada_por_rua = espacamento + largura_rua
    return math.floor((largura_util + espacamento) / faixa_ocupada_por_rua)


def calcular_metricas(
    forma: str, dim_a: float, dim_b: float, largura_rua: float, espacamento: float
) -> tuple[float, int, float, float]:
    if forma == "retangulo":
        comprimento = dim_a
        largura = dim_b
        area_talhao = comprimento * largura
        largura_util = largura
        comprimento_rua = comprimento
    else:
        diametro = dim_a
        area_talhao = math.pi * (diametro / 2) ** 2
        largura_util = diametro
        comprimento_rua = diametro

    qtd_ruas = calcular_qtd_ruas(largura_util, espacamento, largura_rua)
    comp_total_ruas = qtd_ruas * comprimento_rua
    area_metro_rua = largura_rua * 1.0

    # area de plantio = area do talhao - area ocupada apenas pelos espacamentos
    area_ocupada = max(qtd_ruas - 1, 0) * espacamento * comprimento_rua
    area_total_plantio = max(area_talhao - area_ocupada, 0.0)

    return area_total_plantio, qtd_ruas, comp_total_ruas, area_metro_rua
