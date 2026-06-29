#!/usr/bin/env bash
# Script de build executado pelo Render durante o deploy

set -o errexit  # Interrompe o script se algum comando falhar

# Instala as dependências do projeto
pip install -r requirements.txt

# Coleta os arquivos estáticos (CSS, JS, imagens) para a pasta staticfiles/
python djangoproject/manage.py collectstatic --no-input

# Aplica as migrações do banco de dados
python djangoproject/manage.py migrate
