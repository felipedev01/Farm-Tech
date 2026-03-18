import unicodedata

from calculos import calcular_metricas
from repositorio import (
    adicionar_registro,
    atualizar_registro,
    indice_valido,
    listar_registros,
    remover_registro,
    total_registros,
)


def normalizar_texto(texto: str) -> str:
    try:
        texto = texto.encode("latin1").decode("utf-8")
    except UnicodeError:
        pass

    normalizado = unicodedata.normalize("NFD", texto.strip().lower())
    return "".join(char for char in normalizado if unicodedata.category(char) != "Mn")


def ler_float_positivo(mensagem: str) -> float:
    while True:
        valor_texto = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(valor_texto)
            if valor <= 0:
                print("Erro: o valor deve ser maior que zero.")
                continue
            return valor
        except ValueError:
            print("Erro: digite um numero valido.")


def ler_opcao_menu() -> int:
    while True:
        opcao = input("Escolha uma opcao (1-5): ").strip()
        if opcao in {"1", "2", "3", "4", "5"}:
            return int(opcao)
        print("Erro: opcao invalida. Digite um numero de 1 a 5.")


def ler_cultura() -> str:
    while True:
        print("\nSelecione a cultura:")
        print("1. milho")
        print("2. cafe")
        opcao = input("Escolha uma opcao (1-2): ").strip()

        if opcao == "1":
            return "milho"
        if opcao == "2":
            return "cafe"
        print("Erro: opcao invalida. Digite 1 ou 2.")


def ler_forma() -> str:
    while True:
        print("\nSelecione a forma:")
        print("1. retangulo")
        print("2. circulo")
        opcao = input("Escolha uma opcao (1-2): ").strip()

        if opcao == "1":
            return "retangulo"
        if opcao == "2":
            return "circulo"
        print("Erro: opcao invalida. Digite 1 ou 2.")


def coletar_entrada() -> tuple[str, str, float, float, float, float]:
    cultura = ler_cultura()
    forma = ler_forma()

    if forma == "retangulo":
        dim_a = ler_float_positivo("Digite o comprimento do talhao (m): ")
        dim_b = ler_float_positivo("Digite a largura do talhao (m): ")
    else:
        dim_a = ler_float_positivo("Digite o diametro do talhao (m): ")
        dim_b = 0.0

    largura_rua = ler_float_positivo("Digite a largura da rua (m): ")
    espacamento = ler_float_positivo("Digite o espacamento entre ruas (m): ")
    return cultura, forma, dim_a, dim_b, largura_rua, espacamento


def entrada_dados() -> None:
    cultura, forma, dim_a, dim_b, largura_rua, espacamento = coletar_entrada()
    area_total, qtd_ruas, comp_total_ruas, area_metro_rua = calcular_metricas(
        forma, dim_a, dim_b, largura_rua, espacamento
    )
    adicionar_registro(
        cultura,
        forma,
        dim_a,
        dim_b,
        largura_rua,
        espacamento,
        area_total,
        qtd_ruas,
        comp_total_ruas,
        area_metro_rua,
    )
    print("Registro adicionado com sucesso.")


def exibir_dimensoes(registro: dict) -> str:
    if registro["forma"] == "retangulo":
        return (
            f"comprimento={registro['dimensao_a']:.2f} m, "
            f"largura={registro['dimensao_b']:.2f} m"
        )
    return f"diametro={registro['dimensao_a']:.2f} m"


def exibir_registro(indice: int, registro: dict, unidade_area: str) -> None:
    print(f"\nIndice: {indice}")
    print(f"Cultura: {registro['cultura']}")
    print(f"Forma: {registro['forma']}")
    print(f"Dimensoes: {exibir_dimensoes(registro)}")
    print(f"largura_rua: {registro['largura_rua']:.2f} m")
    print(f"espacamento: {registro['espacamento']:.2f} m")
    print(f"Area total de plantio: {registro['area_total']:.2f} {unidade_area}")
    print(f"Quantidade de ruas: {registro['quantidade_ruas']}")
    print(f"Comprimento total das ruas: {registro['comprimento_total_ruas']:.2f} m")
    print(f"Area por metro de rua: {registro['area_por_metro_rua']:.2f} {unidade_area}/m")


def saida_dados(somente_ultimo: bool = False, pausar_ao_final: bool = False) -> None:
    registros = listar_registros()
    if not registros:
        print("Nenhum registro cadastrado.")
        if pausar_ao_final:
            input("Aperte Enter para continuar...")
        return

    unidade_area = "m\u00b2"
    print("\n=== Registros Cadastrados ===")
    if somente_ultimo:
        indice = len(registros) - 1
        exibir_registro(indice, registros[indice], unidade_area)
    else:
        for indice, registro in enumerate(registros):
            exibir_registro(indice, registro, unidade_area)

    if pausar_ao_final:
        input("Aperte Enter para continuar...")


def ler_indice_valido() -> int | None:
    if total_registros() == 0:
        print("Nenhum registro cadastrado.")
        return None

    while True:
        valor_texto = input("Digite o indice do registro: ").strip()
        if not valor_texto.isdigit():
            print("Erro: informe um indice inteiro valido.")
            continue

        indice = int(valor_texto)
        if indice_valido(indice):
            return indice

        print("Erro: indice fora do intervalo existente.")


def atualizar_dados() -> None:
    indice = ler_indice_valido()
    if indice is None:
        return

    print(f"Atualizando registro no indice {indice}...")
    cultura, forma, dim_a, dim_b, largura_rua, espacamento = coletar_entrada()
    area_total, qtd_ruas, comp_total_ruas, area_metro_rua = calcular_metricas(
        forma, dim_a, dim_b, largura_rua, espacamento
    )
    atualizar_registro(
        indice,
        cultura,
        forma,
        dim_a,
        dim_b,
        largura_rua,
        espacamento,
        area_total,
        qtd_ruas,
        comp_total_ruas,
        area_metro_rua,
    )
    print("Registro atualizado com sucesso.")


def deletar_dados() -> None:
    indice = ler_indice_valido()
    if indice is None:
        return

    remover_registro(indice)
    print("Registro removido com sucesso.")


def exibir_menu() -> None:
    print("\n=== FarmTech - Etapa 1 ===")
    print("1. Calcular Area de Plantio")
    print("2. Saida de dados")
    print("3. Atualizacao de dados")
    print("4. Delecao de dados")
    print("5. Sair")


def loop_menu_principal() -> None:
    while True:
        exibir_menu()
        opcao = ler_opcao_menu()

        if opcao == 1:
            entrada_dados()
            saida_dados(somente_ultimo=True, pausar_ao_final=True)
        elif opcao == 2:
            saida_dados(pausar_ao_final=True)
        elif opcao == 3:
            atualizar_dados()
        elif opcao == 4:
            deletar_dados()
        else:
            print("Encerrando o programa.")
            break
