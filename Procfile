web: gunicorn portfolio.wsgi --log-file -
worker: celery -A portfolio worker --loglevel=info
release: python manage.py migrate && python manage.py collectstatic --noinput