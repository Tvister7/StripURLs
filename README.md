<img src="https://img.shields.io/badge/flask-2.0.1-blue">  <img src="https://img.shields.io/badge/redis-3.5.3-critical">  <img src="https://img.shields.io/badge/python-3.9-success">

# StripURLs

Тестовое задание для FunBox

# Описание

Flask-приложение для учета посещенных ссылок с помощью Redis

# Инструкция по запуску

```
cd your_repository
git clone https://github.com/Tvister7/StripURLs
cd StripURLs
```

- Запуск с использованием **_Docker_**

`docker-compose up`

___

- Запуск из терминала 

```
pip install -r requirements.txt
python ./app.py
```

# Проверка работоспособности

## POST-запрос

`curl -X POST -H "Content-Type: application/json" --data @post.json http://localhost:5000/visited_links`

## GET-запрос

`curl "localhost:5000/visited_domains?from=1&to=154521763822"`

## Тестирование

`pytest`
