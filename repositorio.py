import json
import os
from pathlib import Path

VERSAO_ARQUIVO = 1
PASTA_DADOS = Path(__file__).resolve().parent / "data"
ARQUIVO_REGISTROS = PASTA_DADOS / "registros.json"
ARQUIVO_TEMPORARIO = ARQUIVO_REGISTROS.with_suffix(".json.tmp")

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


def _limpar_vetores() -> None:
    culturas.clear()
    formas.clear()
    dimensao_a.clear()
    dimensao_b.clear()
    largura_ruas.clear()
    espacamentos.clear()
    areas_totais.clear()
    quantidade_ruas.clear()
    comprimento_total_ruas.clear()
    area_por_metro_rua.clear()


def _validar_e_hidratar_registros(registros: list[dict]) -> None:
    _limpar_vetores()

    campos_obrigatorios = {
        "cultura",
        "forma",
        "dimensao_a",
        "dimensao_b",
        "largura_rua",
        "espacamento",
        "area_total",
        "quantidade_ruas",
        "comprimento_total_ruas",
        "area_por_metro_rua",
    }

    for item in registros:
        if not isinstance(item, dict):
            raise ValueError("registro com formato invalido")

        if campos_obrigatorios - set(item.keys()):
            raise ValueError("registro com campos ausentes")

        if not isinstance(item["cultura"], str) or not isinstance(item["forma"], str):
            raise ValueError("registro com tipo invalido para cultura ou forma")

        qtd_ruas = item["quantidade_ruas"]
        if isinstance(qtd_ruas, bool) or not isinstance(qtd_ruas, int):
            raise ValueError("registro com tipo invalido para quantidade_ruas")

        culturas.append(item["cultura"])
        formas.append(item["forma"])
        dimensao_a.append(float(item["dimensao_a"]))
        dimensao_b.append(float(item["dimensao_b"]))
        largura_ruas.append(float(item["largura_rua"]))
        espacamentos.append(float(item["espacamento"]))
        areas_totais.append(float(item["area_total"]))
        quantidade_ruas.append(qtd_ruas)
        comprimento_total_ruas.append(float(item["comprimento_total_ruas"]))
        area_por_metro_rua.append(float(item["area_por_metro_rua"]))


def _serializar_registros() -> list[dict]:
    return [obter_registro(i) for i in range(total_registros())]


def _persistir_registros() -> None:
    payload = {"version": VERSAO_ARQUIVO, "registros": _serializar_registros()}
    PASTA_DADOS.mkdir(parents=True, exist_ok=True)
    try:
        with ARQUIVO_TEMPORARIO.open("w", encoding="utf-8") as arquivo:
            json.dump(payload, arquivo, ensure_ascii=False, indent=2)
        os.replace(ARQUIVO_TEMPORARIO, ARQUIVO_REGISTROS)
    except OSError as exc:
        print(f"Aviso: nao foi possivel persistir os dados em disco ({exc}).")
        if ARQUIVO_TEMPORARIO.exists():
            ARQUIVO_TEMPORARIO.unlink(missing_ok=True)


def inicializar_repositorio() -> None:
    _limpar_vetores()
    if not ARQUIVO_REGISTROS.exists():
        return

    try:
        with ARQUIVO_REGISTROS.open("r", encoding="utf-8") as arquivo:
            payload = json.load(arquivo)

        if not isinstance(payload, dict):
            raise ValueError("estrutura raiz invalida")

        if payload.get("version") != VERSAO_ARQUIVO:
            raise ValueError("versao do arquivo nao suportada")

        registros = payload.get("registros")
        if not isinstance(registros, list):
            raise ValueError("lista de registros invalida")

        _validar_e_hidratar_registros(registros)
    except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
        _limpar_vetores()
        print(f"Aviso: arquivo de dados invalido. Iniciando com base vazia ({exc}).")


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
    espacamento: float,
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
    _persistir_registros()


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
    _persistir_registros()


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
    _persistir_registros()
