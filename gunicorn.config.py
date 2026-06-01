import os

bind = '0.0.0.0:8000'
worker_class = 'gthread'
loglevel = 'info'
timeout = 90
keepalive = 5

env = os.getenv('FLASK_ENV', 'LOCAL')

print('[INFO] GUNICORN STARTUP')
print('[INFO] ENV: {0}'.format(env))

if env == 'DEV':
    workers = 1
    threads = 2
elif env == 'UAT':
    workers = 3
    # EN REFACTORIZACIÓN EVALUAR 4 THREADS
    threads = 2
else:
    workers = 1
    threads = 2
