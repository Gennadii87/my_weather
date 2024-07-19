build:
	docker build -t my_weather .

run:
	docker run -d --rm --name my_weather_container -p 8000:80 my_weather

stop:
	docker stop my_weather_container