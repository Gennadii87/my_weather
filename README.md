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
    - информация выводиться в виде графика
    - сохраняется сессия для пользователя и история просмотра городов
    - показывается последний просмотренный город
    - есть api для просмотра статистики запросов по городам с ранжированием
    - есть документация api
</pre>
<hr/>

<h2>Развертывание локально</h2>
Установка зависимостей:

`pip install -r .\requirements.txt` <br/>

Обновите менеджер пакетов (при необходимости):
`python -m pip install --upgrade pip` <br/>

Создайте миграции:
`python manage.py makemigrations` <br/>

Выполните миграции:
`python manage.py migrate` <br/>

Запустить проект:
`python manage.py runserver` <br/>

<hr/>

<h2>Тесты</h2>

Запустить тесты:
`python manage.py test weather` <br/>

<hr/>
<h2>API</h2>

![API](/image/api.png)
<br>

Документация api статистики количества запросов по городам `http://127.0.0.1:8000/swagger-ui/#/`
<hr/>
<h2>Запуск через Docker</h2>
Разверните Docker на своей Ubuntu, установите пакет <code>sudo apt install make</code><br/>

*make* это короткие команды которые прописаны в файле `Makefile`, пример команды в терминале: <pre>`make build`</pre>

<h3>Развертывание через docker-compose</h3>

Запуск в фоновом режиме `docker-compose up -d` <br/>
Остановка с удалением томов `docker-compose down -v` <br/>




