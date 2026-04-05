#!/usr/bin/env bash
# Build script para Render

# Instalar dependências
pip install -r requirements.txt

# O Render usa gunicorn como servidor de produção
pip install gunicorn
