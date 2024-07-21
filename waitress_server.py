from waitress import serve
from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')
application = get_wsgi_application()

if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=8001, threads=4)
