#!/bin/bash
echo "Iniciando docker-entrypoint..."

# Criar superusuário se não existir
echo "Criando superusuário Django..."
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='${WEB_USER}').exists() or User.objects.create_superuser('${WEB_USER}', '${WEB_EMAIL}', '${WEB_PASSWORD}')"

# Finalizando
echo "Superusuário criado com sucesso."

# Manter o container em execução
exec "$@"
