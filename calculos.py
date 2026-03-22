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


def _insumo(
    nome: str,
    dose_por_m2: float,
    unidade: str,
    area_por_metro_rua: float,
    comprimento_total_ruas: float,
) -> dict:
    dose_por_metro = dose_por_m2 * area_por_metro_rua
    return {
        "nome": nome,
        "dose_por_metro": dose_por_metro,
        "unidade": unidade,
        "consumo_total": dose_por_metro * comprimento_total_ruas,
    }


def calcular_insumos_por_cultura(
    cultura: str, comprimento_total_ruas: float, area_por_metro_rua: float
) -> list[dict]:
    cultura_normalizada = cultura.strip().lower()

    if cultura_normalizada == "milho":
        # Doses-base em m2.
        dose_semente_m2 = 5.5
        dose_npk_m2 = 450.0 / 10000.0
        dose_ureia_m2 = 125.0 / 10000.0
        return [
            _insumo(
                "Semente de milho hibrido",
                dose_semente_m2,
                "sementes",
                area_por_metro_rua,
                comprimento_total_ruas,
            ),
            _insumo(
                "Fertilizante NPK 04-14-08",
                dose_npk_m2,
                "kg",
                area_por_metro_rua,
                comprimento_total_ruas,
            ),
            _insumo(
                "Ureia (cobertura)",
                dose_ureia_m2,
                "kg",
                area_por_metro_rua,
                comprimento_total_ruas,
            ),
        ]

    if cultura_normalizada == "cafe":
        # Doses de referencia por m2 para manejo didatico.
        dose_ureia_m2 = 8.9
        dose_zinco_m2 = 3.0
        dose_manganes_m2 = 5.0
        return [
            _insumo(
                "Ureia (pos-plantio)",
                dose_ureia_m2,
                "g",
                area_por_metro_rua,
                comprimento_total_ruas,
            ),
            _insumo(
                "Sulfato de zinco (foliar)",
                dose_zinco_m2,
                "g",
                area_por_metro_rua,
                comprimento_total_ruas,
            ),
            _insumo(
                "Sulfato de manganes (foliar)",
                dose_manganes_m2,
                "g",
                area_por_metro_rua,
                comprimento_total_ruas,
            ),
        ]

    raise ValueError("cultura nao suportada para calculo de insumos")
