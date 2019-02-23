web: gunicorn git_inspect.wsgi --limit-request-line 8188 --log-file -
worker: celery worker --app=git_inspect --loglevel=info
