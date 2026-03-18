culturas: list[str] = []
formas: list[str] = []
dimensao_a: list[float] = []
dimensao_b: list[float] = []
largura_ruas: list[float] = []
espacamentos: list[float] = []

areas_totais: list[float] = []
quantidade_ruas: list[int] = []
comprimento_total_ruas: list[float] = []
area_por_metro_rua: list[float] = []


def total_registros() -> int:
    return len(culturas)


def indice_valido(indice: int) -> bool:
    return 0 <= indice < total_registros()


def adicionar_registro(
    cultura: str,
    forma: str,
    dim_a: float,
    dim_b: float,
    largura_rua: float,
    espacamento:float,
    area_total: float,
    qtd_ruas: int,
    comp_total_ruas: float,
    area_metro_rua: float,
) -> None:
    culturas.append(cultura)
    formas.append(forma)
    dimensao_a.append(dim_a)
    dimensao_b.append(dim_b)
    largura_ruas.append(largura_rua)
    espacamentos.append(espacamento)
    areas_totais.append(area_total)
    quantidade_ruas.append(qtd_ruas)
    comprimento_total_ruas.append(comp_total_ruas)
    area_por_metro_rua.append(area_metro_rua)


def obter_registro(indice: int) -> dict:
    if not indice_valido(indice):
        raise IndexError("indice fora do intervalo existente")

    return {
        "cultura": culturas[indice],
        "forma": formas[indice],
        "dimensao_a": dimensao_a[indice],
        "dimensao_b": dimensao_b[indice],
        "largura_rua": largura_ruas[indice],
        "espacamento": espacamentos[indice],
        "area_total": areas_totais[indice],
        "quantidade_ruas": quantidade_ruas[indice],
        "comprimento_total_ruas": comprimento_total_ruas[indice],
        "area_por_metro_rua": area_por_metro_rua[indice],
    }


def listar_registros() -> list[dict]:
    return [obter_registro(i) for i in range(total_registros())]


def atualizar_registro(
    indice: int,
    cultura: str,
    forma: str,
    dim_a: float,
    dim_b: float,
    largura_rua: float,
    espacamento: float,
    area_total: float,
    qtd_ruas: int,
    comp_total_ruas: float,
    area_metro_rua: float,
) -> None:
    if not indice_valido(indice):
        raise IndexError("indice fora do intervalo existente")

    culturas[indice] = cultura
    formas[indice] = forma
    dimensao_a[indice] = dim_a
    dimensao_b[indice] = dim_b
    largura_ruas[indice] = largura_rua
    espacamentos[indice] = espacamento
    areas_totais[indice] = area_total
    quantidade_ruas[indice] = qtd_ruas
    comprimento_total_ruas[indice] = comp_total_ruas
    area_por_metro_rua[indice] = area_metro_rua


def remover_registro(indice: int) -> None:
    if not indice_valido(indice):
        raise IndexError("indice fora do intervalo existente")

    culturas.pop(indice)
    formas.pop(indice)
    dimensao_a.pop(indice)
    dimensao_b.pop(indice)
    largura_ruas.pop(indice)
    espacamentos.pop(indice)
    areas_totais.pop(indice)
    quantidade_ruas.pop(indice)
    comprimento_total_ruas.pop(indice)
    area_por_metro_rua.pop(indice)
