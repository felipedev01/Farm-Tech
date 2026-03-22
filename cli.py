import unicodedata

from calculos import calcular_insumos_por_cultura, calcular_metricas
from repositorio import (
    adicionar_registro,
    atualizar_registro,
    indice_valido,
    listar_registros,
    remover_registro,
    setar_insumos_registro,
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


def ler_opcao_fluxo_insumos() -> int:
    while True:
        print("\nDeseja calcular o consumo de insumos deste registro?")
        print("1. Calcular consumo de insumos")
        print("2. Finalizar e voltar ao menu principal")
        opcao = input("Escolha uma opcao (1-2): ").strip()
        if opcao in {"1", "2"}:
            return int(opcao)
        print("Erro: opcao invalida. Digite 1 ou 2.")


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


def entrada_dados() -> int:
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
    return total_registros() - 1


def formatar_float_ptbr(valor: float) -> str:
    texto = f"{valor:,.2f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def formatar_int_ptbr(valor: int) -> str:
    texto = f"{valor:,d}"
    return texto.replace(",", ".")


def exibir_dimensoes(registro: dict) -> str:
    if registro["forma"] == "retangulo":
        return (
            f"{formatar_float_ptbr(registro['dimensao_a'])} m x "
            f"{formatar_float_ptbr(registro['dimensao_b'])} m"
        )
    return f"diametro {formatar_float_ptbr(registro['dimensao_a'])} m"


def linha_campo(rotulo: str, valor: str, largura_rotulo: int = 28) -> str:
    return f"  {rotulo.ljust(largura_rotulo, '.')} {valor}"


def formatar_dose_por_metro(dose: float, unidade: str) -> str:
    return f"{formatar_float_ptbr(dose)} {unidade}/m"


def formatar_consumo_total(consumo: float, unidade: str) -> str:
    return f"{formatar_float_ptbr(consumo)} {unidade}"


def exibir_insumos(registro: dict) -> None:
    insumos = registro.get("insumos", [])
    print("Insumos")
    print()
    if not insumos:
        print("  Insumos: nao calculados")
        print()
        return

    for insumo in insumos:
        nome = insumo["nome"]
        dose = formatar_dose_por_metro(insumo["dose_por_metro"], insumo["unidade"])
        consumo = formatar_consumo_total(insumo["consumo_total"], insumo["unidade"])
        print(linha_campo(nome, f"dose {dose} | total {consumo}", largura_rotulo=36))
    print()


def exibir_registro(indice: int, registro: dict, unidade_area: str) -> None:
    print("\n----------------------------------------")
    print(f"Registro #{indice}")
    print("----------------------------------------")
    print("Dados de Entrada")
    print(linha_campo("Cultura", registro["cultura"]))
    print(linha_campo("Forma", registro["forma"]))
    print(linha_campo("Dimensoes", exibir_dimensoes(registro)))
    print(
        linha_campo(
            "Largura da rua", f"{formatar_float_ptbr(registro['largura_rua'])} m"
        )
    )
    print(
        linha_campo(
            "Espacamento entre ruas",
            f"{formatar_float_ptbr(registro['espacamento'])} m",
        )
    )
    print()
    print("Metricas de Plantio")
    print()
    print(
        linha_campo(
            "Area total de plantio",
            f"{formatar_float_ptbr(registro['area_total'])} {unidade_area}",
        )
    )
    print(
        linha_campo(
            "Quantidade de ruas", formatar_int_ptbr(registro["quantidade_ruas"])
        )
    )
    print(
        linha_campo(
            "Comprimento total das ruas",
            f"{formatar_float_ptbr(registro['comprimento_total_ruas'])} m",
        )
    )
    print(
        linha_campo(
            "Area por metro de rua",
            f"{formatar_float_ptbr(registro['area_por_metro_rua'])} {unidade_area}/m",
        )
    )
    print()
    exibir_insumos(registro)


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


def saida_insumos_por_indice(
    indice_registro: int, pausar_ao_final: bool = False
) -> None:
    registros = listar_registros()
    if not (0 <= indice_registro < len(registros)):
        print("Erro: registro nao encontrado para exibicao de insumos.")
        if pausar_ao_final:
            input("Aperte Enter para continuar...")
        return

    print("\n=== Insumos Calculados ===")
    print(f"Registro #{indice_registro}")
    exibir_insumos(registros[indice_registro])

    if pausar_ao_final:
        input("Aperte Enter para continuar...")


def calcular_e_salvar_insumos(indice_registro: int) -> None:
    registros = listar_registros()
    if not (0 <= indice_registro < len(registros)):
        print("Erro: registro nao encontrado para calculo de insumos.")
        return

    registro = registros[indice_registro]
    insumos = calcular_insumos_por_cultura(
        registro["cultura"],
        registro["comprimento_total_ruas"],
        registro["area_por_metro_rua"],
    )
    setar_insumos_registro(indice_registro, insumos)
    print("Insumos calculados e salvos com sucesso.")


def fluxo_pos_calculo(indice_registro: int) -> None:
    opcao = ler_opcao_fluxo_insumos()
    if opcao == 1:
        calcular_e_salvar_insumos(indice_registro)
        saida_insumos_por_indice(indice_registro, pausar_ao_final=True)


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
            indice_novo = entrada_dados()
            saida_dados(somente_ultimo=True, pausar_ao_final=False)
            fluxo_pos_calculo(indice_novo)
        elif opcao == 2:
            saida_dados(pausar_ao_final=True)
        elif opcao == 3:
            atualizar_dados()
        elif opcao == 4:
            deletar_dados()
        else:
            print("Encerrando o programa.")
            break
