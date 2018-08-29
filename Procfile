web: gunicorn vle_webapp.wsgi --log-file -
worker: python -c 'from webapp import worker; worker.main()'