source("r/io_dados.R")
source("r/estatisticas.R")

verificar_dependencias <- function() {
  pacotes <- c("jsonlite", "dplyr")
  faltantes <- pacotes[!vapply(pacotes, requireNamespace, logical(1), quietly = TRUE)]

  if (length(faltantes) > 0) {
    cat("Dependencias ausentes detectadas.\n")
    for (pkg in faltantes) {
      cat(sprintf("- %s\n", pkg))
    }
    cat("\nInstale antes de executar:\n")
    for (pkg in faltantes) {
      cat(sprintf('install.packages("%s")\n', pkg))
    }
    quit(save = "no", status = 1)
  }
}

ler_opcao_menu <- function() {
  while (TRUE) {
    entrada <- trimws(readline("Escolha uma opcao (1-7): "))
    if (entrada == "" && !isatty(stdin())) {
      stop(
        paste(
          "Entrada interativa indisponivel (stdin sem terminal).",
          "Execute no terminal com:",
          "'Rscript r/main.R'"
        )
      )
    }
    if (entrada %in% as.character(1:7)) {
      return(as.integer(entrada))
    }
    cat("Erro: opcao invalida. Digite um numero de 1 a 7.\n")
  }
}

aguardar_volta_menu <- function() {
  while (TRUE) {
    entrada <- trimws(readline("\nDigite 1 para voltar ao menu: "))
    if (entrada == "1") {
      return(invisible(NULL))
    }
    cat("Opcao invalida. Digite 1 para voltar ao menu.\n")
  }
}

exibir_menu <- function() {
  cat("\n=== FarmTech Estatisticas (R) ===\n")
  cat("1. Carregar dados\n")
  cat("2. Exibir estatistica de plantio (geral)\n")
  cat("3. Exibir estatistica de plantio (por cultura)\n")
  cat("4. Exibir estatistica de insumos (por cultura)\n")
  cat("5. Salvar execucao no historico\n")
  cat("6. Visualizar ultimas execucoes do historico\n")
  cat("7. Sair\n")
}

main <- function() {
  verificar_dependencias()

  if (!isatty(stdin())) {
    stop(
      paste(
        "Este script precisa de entrada interativa.",
        "Abra um terminal e rode: 'Rscript r/main.R'"
      )
    )
  }

  caminho_entrada <- "data/registros.json"
  caminho_historico <- "outputs/historico_estatisticas.json"
  dados <- NULL

  while (TRUE) {
    exibir_menu()
    opcao <- ler_opcao_menu()

    if (opcao == 1) {
      dados <- tryCatch(
        carregar_registros(caminho_entrada),
        error = function(e) {
          cat(sprintf("Erro ao carregar dados: %s\n", conditionMessage(e)))
          NULL
        }
      )

      if (!is.null(dados)) {
        cat(
          sprintf(
            "Dados carregados com sucesso. Registros de plantio: %d | linhas de insumos: %d\n",
            nrow(dados$plantio_df),
            nrow(dados$insumos_df)
          )
        )
        if (nrow(dados$plantio_df) == 0) {
          cat("Aviso: base vazia.\n")
        }
      }
    } else if (opcao == 2) {
      if (is.null(dados)) {
        cat("Nenhum dado carregado. Use a opcao 1 primeiro.\n")
        next
      }
      resumo_geral <- calcular_resumo_geral(dados$plantio_df)
      exibir_resumo_geral(resumo_geral)
      aguardar_volta_menu()
    } else if (opcao == 3) {
      if (is.null(dados)) {
        cat("Nenhum dado carregado. Use a opcao 1 primeiro.\n")
        next
      }
      resumo_por_cultura <- calcular_resumo_por_cultura(dados$plantio_df)
      exibir_resumo_por_cultura(resumo_por_cultura)
      aguardar_volta_menu()
    } else if (opcao == 4) {
      if (is.null(dados)) {
        cat("Nenhum dado carregado. Use a opcao 1 primeiro.\n")
        next
      }
      resumo_insumos_por_cultura <- calcular_resumo_insumos_por_cultura(dados$insumos_df)
      exibir_resumo_insumos_por_cultura(resumo_insumos_por_cultura)
      aguardar_volta_menu()
    } else if (opcao == 5) {
      if (is.null(dados)) {
        cat("Nenhum dado carregado. Use a opcao 1 primeiro.\n")
        next
      }
      snapshot <- criar_snapshot_execucao(
        dados$plantio_df,
        dados$insumos_df,
        caminho_entrada
      )
      tryCatch(
        {
          salvar_execucao_historico(snapshot, caminho_historico)
          cat(sprintf("Execucao salva com sucesso em %s\n", caminho_historico))
        },
        error = function(e) {
          cat(sprintf("Erro ao salvar historico: %s\n", conditionMessage(e)))
        }
      )
    } else if (opcao == 6) {
      execucoes <- tryCatch(
        listar_ultimas_execucoes(caminho_historico, limite = 5),
        error = function(e) {
          cat(sprintf("Erro ao ler historico: %s\n", conditionMessage(e)))
          list()
        }
      )
      exibir_execucoes_historico(execucoes)
    } else {
      cat("Encerrando aplicacao R.\n")
      break
    }
  }
}

main()
