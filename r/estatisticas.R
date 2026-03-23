metricas_plantio <- c(
  "area_total",
  "quantidade_ruas",
  "comprimento_total_ruas",
  "area_por_metro_rua"
)

rotulos_metricas <- c(
  area_total = "Area total",
  quantidade_ruas = "Quantidade de ruas",
  comprimento_total_ruas = "Comprimento total das ruas",
  area_por_metro_rua = "Area por metro de rua",
  consumo_total = "Consumo total"
)

calcular_estatistica_vetor <- function(valores) {
  numeros <- as.numeric(valores)
  numeros <- numeros[is.finite(numeros)]
  n <- length(numeros)

  media <- if (n > 0) mean(numeros) else NA_real_
  desvio <- if (n >= 2) stats::sd(numeros) else NA_real_

  list(n = n, mean = media, sd = desvio)
}

calcular_resumo_geral <- function(df) {
  resumo <- lapply(metricas_plantio, function(metrica) {
    calcular_estatistica_vetor(df[[metrica]])
  })
  names(resumo) <- metricas_plantio
  resumo
}

calcular_resumo_por_cultura <- function(df) {
  if (nrow(df) == 0) {
    return(list())
  }

  agrupado <- dplyr::group_by(df, cultura)
  chaves <- dplyr::group_keys(agrupado)
  grupos <- dplyr::group_split(agrupado, .keep = TRUE)

  resumo <- list()
  for (i in seq_along(grupos)) {
    cultura <- as.character(chaves$cultura[[i]])
    resumo[[cultura]] <- calcular_resumo_geral(grupos[[i]])
  }
  resumo
}

calcular_resumo_insumos_por_cultura <- function(insumos_df) {
  if (nrow(insumos_df) == 0) {
    return(list())
  }

  grupos_cultura <- split(insumos_df, insumos_df$cultura, drop = TRUE)
  resumo <- list()

  for (cultura in names(grupos_cultura)) {
    df_cultura <- grupos_cultura[[cultura]]
    grupos_insumo <- split(df_cultura, df_cultura$insumo_nome, drop = TRUE)

    resumo_insumos <- list()
    for (insumo_nome in names(grupos_insumo)) {
      df_insumo <- grupos_insumo[[insumo_nome]]
      grupos_unidade <- split(df_insumo, df_insumo$unidade, drop = TRUE)

      resumo_unidades <- lapply(grupos_unidade, function(df_unidade) {
        list(consumo_total = calcular_estatistica_vetor(df_unidade$consumo_total))
      })
      resumo_insumos[[insumo_nome]] <- resumo_unidades
    }

    resumo[[cultura]] <- resumo_insumos
  }

  resumo
}

criar_snapshot_execucao <- function(plantio_df, insumos_df, source_file) {
  list(
    generated_at = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
    source_file = source_file,
    input_count = nrow(plantio_df),
    insumos_count = nrow(insumos_df),
    overall = calcular_resumo_geral(plantio_df),
    by_culture = calcular_resumo_por_cultura(plantio_df),
    insumos_by_culture = calcular_resumo_insumos_por_cultura(insumos_df)
  )
}

formatar_numero <- function(valor) {
  if (is.na(valor)) {
    return("NA")
  }

  formatC(
    valor,
    format = "f",
    digits = 2,
    decimal.mark = ",",
    big.mark = "."
  )
}

formatar_amostra <- function(valor) {
  formatC(as.integer(valor), format = "d", big.mark = ".", decimal.mark = ",")
}

rotulo_metrica <- function(metrica) {
  if (!is.na(rotulos_metricas[metrica])) {
    return(rotulos_metricas[metrica])
  }
  metrica
}

imprimir_bloco_resumo <- function(titulo, resumo) {
  cat("\n", titulo, "\n", sep = "")
  cat(strrep("-", nchar(titulo)), "\n", sep = "")

  for (metrica in names(resumo)) {
    estat <- resumo[[metrica]]
    cat(sprintf("%s\n", rotulo_metrica(metrica)))
    cat(sprintf("  Numero de amostras: %s\n", formatar_amostra(estat$n)))
    cat(sprintf("  Media: %s\n", formatar_numero(estat$mean)))
    cat(sprintf("  Desvio padrao: %s\n", formatar_numero(estat$sd)))
  }
}

exibir_resumo_geral <- function(resumo_geral) {
  imprimir_bloco_resumo("Estatistica de plantio - Geral", resumo_geral)
}

exibir_resumo_por_cultura <- function(resumo_por_cultura) {
  if (length(resumo_por_cultura) == 0) {
    cat("\nNenhuma cultura disponivel para exibir estatisticas de plantio.\n")
    return(invisible(NULL))
  }

  for (cultura in names(resumo_por_cultura)) {
    titulo <- sprintf("Estatistica de plantio da cultura: %s", cultura)
    imprimir_bloco_resumo(titulo, resumo_por_cultura[[cultura]])
  }

  invisible(NULL)
}

exibir_resumo_insumos_por_cultura <- function(resumo_por_cultura) {
  if (length(resumo_por_cultura) == 0) {
    cat("\nNenhum insumo disponivel para estatistica por cultura.\n")
    return(invisible(NULL))
  }

  for (cultura in names(resumo_por_cultura)) {
    cat(sprintf("\nCultura: %s\n", cultura))
    cat(strrep("-", 10 + nchar(cultura)), "\n", sep = "")

    insumos <- resumo_por_cultura[[cultura]]
    for (insumo_nome in names(insumos)) {
      unidades <- insumos[[insumo_nome]]
      for (unidade in names(unidades)) {
        titulo <- sprintf("Insumo: %s (unidade: %s)", insumo_nome, unidade)
        imprimir_bloco_resumo(titulo, unidades[[unidade]])
      }
    }
  }

  invisible(NULL)
}

exibir_execucoes_historico <- function(execucoes) {
  if (length(execucoes) == 0) {
    cat("\nHistorico vazio.\n")
    return(invisible(NULL))
  }

  cat("\nUltimas execucoes salvas:\n")
  for (i in seq_along(execucoes)) {
    execucao <- execucoes[[i]]
    insumos_count <- if (is.null(execucao$insumos_count)) {
      "n/a"
    } else {
      as.character(execucao$insumos_count)
    }

    cat(sprintf(
      "%d) %s | registros=%s | insumos=%s | fonte=%s\n",
      i,
      as.character(execucao$generated_at),
      as.character(execucao$input_count),
      insumos_count,
      as.character(execucao$source_file)
    ))
  }

  invisible(NULL)
}
