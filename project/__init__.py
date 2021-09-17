# from flask import Flask
# from flask_redis import Redis
# from project.config import Config
#
# # Инициализируем базовый объект базы данных
# db = Redis()
#
#
# # Шаблон фабрики приложений
# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(config_class)
#     db.init_app(app)
#
#     return app
