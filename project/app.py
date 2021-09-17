from urllib.parse import urlparse
import arrow
import redis
from flask import request, jsonify, Flask
from flask_redis import Redis

from project.config import Config

# Создаем приложение
# app = create_app()
# app.app_context().push()

app = Flask(__name__)
app.config.from_object(Config)
db = Redis(app)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify(status="Page not found 404. Don't be sad mate, try another time :)")


@app.route("/visited_links", methods=["POST"])
def add_links():
    # Получаем json
    links = request.get_json()
    # Ищем ключ 'links' в json'е и очищаем его содержимое
    if 'links' in links:
        for link in links['links']:
            domain = urlparse(link).netloc or urlparse(link).path
            date = arrow.utcnow().timestamp()
            # Устанавливаем временную метку и создаем объект для передачи в базу
            data = f"{domain}:{date}"
            try:
                db.zadd("domains:timestamp", {data.lower(): date})
            except redis.exceptions.ConnectionError:
                return jsonify(status='Проблема с базой данных')
    else:
        return jsonify(status='Нет ссылок')

    return jsonify(status='ok')


@app.route("/visited_domains", methods=["GET"])
def get_domains():
    # Получаем данные из атрибутов запроса
    with app.app_context():
        date_from = request.args.get('from') or "None"
        date_to = request.args.get('to') or "None"
    user_response = dict(domains=[], status='')
    # Проверка на корректность данных (можно еще вставить дополнительные проверки типа данных и т.п.)
    if date_from.isdigit() and date_to.isdigit():
        if date_from > date_to:
            user_response['status'] = 'Некорректный интервал времени'
            return user_response

        # Получаем данные из базы по корректному временному интервалу
        try:
            data = db.zrangebyscore('domains:timestamp', date_from, date_to, withscores=True)
        except redis.exceptions.ConnectionError:
            return jsonify(status='Проблема с базой данных')

        # Разбираемся с кодировкой
        for item in data:
            # user_response['domains'].append(item)
            strip_item = item[0].decode("utf-8").split(':')[0]
            if strip_item != '':
                user_response["domains"].append(strip_item)
        # Оставляем только уникальные записи
        user_response["domains"] = sorted(set(user_response["domains"]))

        user_response['status'] = 'ok'
    else:
        user_response['status'] = 'Параметры url-адреса введены неверно'

    return user_response


if __name__ == '__main__':
    app.run(debug=True)
