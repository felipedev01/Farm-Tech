criar_plantio_df_vazio <- function() {
  data.frame(
    cultura = character(0),
    area_total = numeric(0),
    quantidade_ruas = numeric(0),
    comprimento_total_ruas = numeric(0),
    area_por_metro_rua = numeric(0),
    stringsAsFactors = FALSE
  )
}

criar_insumos_df_vazio <- function() {
  data.frame(
    registro_id = integer(0),
    cultura = character(0),
    insumo_nome = character(0),
    unidade = character(0),
    consumo_total = numeric(0),
    stringsAsFactors = FALSE
  )
}

normalizar_insumos_registro <- function(insumos, registro_id, cultura) {
  if (is.null(insumos)) {
    return(criar_insumos_df_vazio())
  }

  if (!is.list(insumos)) {
    stop(sprintf("Registro #%d invalido: insumos deve ser uma lista.", registro_id))
  }

  if (length(insumos) == 0) {
    return(criar_insumos_df_vazio())
  }

  linhas <- lapply(seq_along(insumos), function(j) {
    item <- insumos[[j]]
    if (!is.list(item)) {
      stop(sprintf("Registro #%d, insumo #%d invalido: esperado objeto.", registro_id, j))
    }

    campos_obrigatorios <- c("nome", "unidade", "consumo_total")
    faltantes <- setdiff(campos_obrigatorios, names(item))
    if (length(faltantes) > 0) {
      stop(
        sprintf(
          "Registro #%d, insumo #%d invalido: campos ausentes [%s].",
          registro_id,
          j,
          paste(faltantes, collapse = ", ")
        )
      )
    }

    insumo_nome <- tolower(trimws(as.character(item$nome)))
    unidade <- tolower(trimws(as.character(item$unidade)))
    consumo_total <- suppressWarnings(as.numeric(item$consumo_total))

    if (!is.finite(consumo_total)) {
      stop(
        sprintf(
          "Registro #%d, insumo #%d invalido: consumo_total deve ser numerico finito.",
          registro_id,
          j
        )
      )
    }

    data.frame(
      registro_id = as.integer(registro_id),
      cultura = cultura,
      insumo_nome = insumo_nome,
      unidade = unidade,
      consumo_total = consumo_total,
      stringsAsFactors = FALSE
    )
  })

  do.call(rbind, linhas)
}

carregar_registros <- function(path_arquivo) {
  if (!file.exists(path_arquivo)) {
    stop(sprintf("Arquivo de dados nao encontrado: %s", path_arquivo))
  }

  payload <- tryCatch(
    jsonlite::fromJSON(path_arquivo, simplifyVector = FALSE),
    error = function(e) {
      stop(sprintf("Falha ao ler JSON de entrada: %s", conditionMessage(e)))
    }
  )

  if (!is.list(payload)) {
    stop("JSON invalido: raiz deve ser um objeto.")
  }

  if (is.null(payload$version) || payload$version != 2) {
    stop("JSON invalido: esperado campo version=2.")
  }

  registros <- payload$registros
  if (is.null(registros) || !is.list(registros)) {
    stop("JSON invalido: campo registros deve ser uma lista.")
  }

  colunas_obrigatorias <- c(
    "cultura",
    "area_total",
    "quantidade_ruas",
    "comprimento_total_ruas",
    "area_por_metro_rua"
  )

  if (length(registros) == 0) {
    return(
      list(
        plantio_df = criar_plantio_df_vazio(),
        insumos_df = criar_insumos_df_vazio()
      )
    )
  }

  linhas_plantio <- lapply(seq_along(registros), function(i) {
    item <- registros[[i]]
    if (!is.list(item)) {
      stop(sprintf("Registro #%d invalido: esperado objeto.", i))
    }

    faltantes <- setdiff(colunas_obrigatorias, names(item))
    if (length(faltantes) > 0) {
      stop(
        sprintf(
          "Registro #%d invalido: campos ausentes [%s].",
          i,
          paste(faltantes, collapse = ", ")
        )
      )
    }

    cultura <- tolower(trimws(as.character(item$cultura)))
    area_total <- suppressWarnings(as.numeric(item$area_total))
    quantidade_ruas <- suppressWarnings(as.numeric(item$quantidade_ruas))
    comprimento_total_ruas <- suppressWarnings(as.numeric(item$comprimento_total_ruas))
    area_por_metro_rua <- suppressWarnings(as.numeric(item$area_por_metro_rua))

    if (!is.finite(area_total) ||
      !is.finite(quantidade_ruas) ||
      !is.finite(comprimento_total_ruas) ||
      !is.finite(area_por_metro_rua)) {
      stop(sprintf("Registro #%d invalido: metrica numerica invalida.", i))
    }

    data.frame(
      cultura = cultura,
      area_total = area_total,
      quantidade_ruas = quantidade_ruas,
      comprimento_total_ruas = comprimento_total_ruas,
      area_por_metro_rua = area_por_metro_rua,
      stringsAsFactors = FALSE
    )
  })

  linhas_insumos <- lapply(seq_along(registros), function(i) {
    item <- registros[[i]]
    cultura <- tolower(trimws(as.character(item$cultura)))
    normalizar_insumos_registro(item$insumos, i, cultura)
  })

  plantio_df <- do.call(rbind, linhas_plantio)
  insumos_com_dados <- Filter(function(df) nrow(df) > 0, linhas_insumos)
  insumos_df <- if (length(insumos_com_dados) == 0) {
    criar_insumos_df_vazio()
  } else {
    do.call(rbind, insumos_com_dados)
  }

  list(plantio_df = plantio_df, insumos_df = insumos_df)
}

carregar_historico <- function(path_arquivo) {
  if (!file.exists(path_arquivo)) {
    return(list(version = 1, executions = list()))
  }

  historico <- tryCatch(
    jsonlite::fromJSON(path_arquivo, simplifyVector = FALSE),
    error = function(e) {
      stop(sprintf("Falha ao ler historico JSON: %s", conditionMessage(e)))
    }
  )

  if (!is.list(historico)) {
    stop("Historico invalido: raiz deve ser um objeto.")
  }

  if (is.null(historico$version) || historico$version != 1) {
    stop("Historico invalido: esperado campo version=1.")
  }

  if (is.null(historico$executions) || !is.list(historico$executions)) {
    stop("Historico invalido: campo executions deve ser lista.")
  }

  historico
}

salvar_execucao_historico <- function(snapshot, path_arquivo) {
  historico <- carregar_historico(path_arquivo)
  historico$executions <- c(historico$executions, list(snapshot))

  dir_saida <- dirname(path_arquivo)
  if (!dir.exists(dir_saida)) {
    dir.create(dir_saida, recursive = TRUE, showWarnings = FALSE)
  }

  arquivo_temp <- paste0(path_arquivo, ".tmp")
  conteudo <- jsonlite::toJSON(
    historico,
    auto_unbox = TRUE,
    pretty = TRUE,
    na = "null",
    null = "null"
  )

  writeLines(conteudo, con = arquivo_temp, useBytes = TRUE)
  if (!file.rename(arquivo_temp, path_arquivo)) {
    ok <- file.copy(arquivo_temp, path_arquivo, overwrite = TRUE)
    unlink(arquivo_temp, force = TRUE)
    if (!ok) {
      stop("Falha ao persistir historico em disco.")
    }
  }

  invisible(NULL)
}

listar_ultimas_execucoes <- function(path_arquivo, limite = 5) {
  historico <- carregar_historico(path_arquivo)
  total <- length(historico$executions)
  if (total == 0) {
    return(list())
  }

  inicio <- max(1, total - limite + 1)
  historico$executions[inicio:total]
}
