# MY_WEATHER
<h2>Приложение для просмотра погоды в разных городах</h2><br/>

![weather](/image/weather.png)
<br>
![history](/image/history.png)
<br>

Основные функции:
<pre>
    - показывает температуру в промежутке времени
    - словарь для автозавершения в строке поиска
    - показывает координаты введенного города
    - показывает подробную локацию (край, регион, область)
    - информация выводиться в виде графика
    - сохраняется сессия для пользователя и история просмотра городов
    - показывается последний просмотренный город
    - есть api для просмотра статистики запросов по городам с ранжированием
    - есть документация api
</pre>
<hr/>

<h2>Развертывание локально</h2>
Установка зависимостей:

    pip install -r .\requirements.txt

Обновите менеджер пакетов (при необходимости):

    python -m pip install --upgrade pip

Создайте миграции:

    python manage.py makemigrations

Выполните миграции:

    python manage.py migrate

Запустить проект:

    python manage.py runserver
 
*Добавлен запуск через web сервер waitress (по умолчанию установлен порт 8001)*
    
    python waitress_server.py 

<hr/>
<h2>Тесты</h2>
Запустить тесты:

    python manage.py test weather

<hr/>
<h2>API</h2>

![API](/image/api.png)

<br>
Документация api http://127.0.0.1:8000/swagger-ui/#/
<hr/>
<h2>Запуск через Docker</h2>
Разверните Docker на своей Ubuntu, установите пакет <pre>sudo apt install make</pre>

*make* это короткие команды которые прописаны в файле `Makefile`, пример команды в терминале: <pre>`make build`</pre>

<h3>Развертывание через docker-compose</h3>

Запуск в фоновом режиме <pre> `docker-compose up -d` </pre>
Остановка с удалением томов <pre> `docker-compose down -v` </pre> 
