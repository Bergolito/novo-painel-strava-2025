#!/bin/bash
# Script de configuração automática do painel Strava
# Gera datasets e organiza arquivos conforme painel-strava-passo-a-passo-configuracao.md

set -e

# ============================================================
# Passo 1: Extrair arquivos .gz da pasta strava-activities
# ============================================================
echo "Zipando arquivos da pasta datasets com a data de hoje"
nome_arquivo="$(date +%Y-%m-%d)-backup.zip"
if [ ! -f "$nome_arquivo" ]; then
    zip -r "$nome_arquivo" datasets
    echo "Arquivo $nome_arquivo criado."
    mv "$nome_arquivo" backups/
else
    echo "Arquivo $nome_arquivo já existe."
fi

# ============================================================
# Passo 2: Pré-processamento dos arquivos
# ============================================================
if [ -f config/painel_config_preprocessamento.py ]; then
    echo "Executando painel_config_preprocessamento.py..."
    python3.10 config/painel_config_preprocessamento.py
fi

# ============================================================
# Passo 3: Geração dos datasets
# ============================================================
if [ -f config/painel_config_geracao_dados.py ]; then
    echo "Executando painel_config_geracao_dados.py..."
    python3.10 config/painel_config_geracao_dados.py
fi

echo "Processo finalizado."
