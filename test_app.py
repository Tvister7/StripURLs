import pytest
from flask_redis import Redis

from project.config import Config
from project.app import app, db


class TestConfig(Config):
    TESTING = True
    REDIS_DB = 10


GET_URL = "/visited_domains?from=1&to=154521763822"
POST_URL = "/visited_links"
TEST_DATA = {
    "links": [
        "https://ya.ru",
        "https://ya.ru?q=123",
        "funbox.ru",
        "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
        "GITHUB.COM"
    ]
}


@pytest.fixture
def client():
    app.config.from_object(TestConfig)
    db.delete('domains:timestamp')

    with app.test_client() as client:
        with app.app_context():
            yield client


def test_wrong_url(client):
    response = client.get("/someway")
    expected_response = {"status": "Page not found 404. Don't be sad mate, try another time :)"}
    assert response.get_json() == expected_response


def test_add_good_links(client):
    test_data = {
        "links": [
            "github.com",
            "http://yandex.ru",
            "https://ya.ru?q=1234",
            "www.wikipedia.org",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
        ]
    }

    response = client.post(POST_URL, json=test_data)
    expected_response = {"status": "ok"}
    assert response.get_json() == expected_response


def test_add_bad_json(client):
    test_data1 = {"links": []}
    test_data2 = {
        "link": [
            "github.com",
            "http://yandex.ru",
            "https://ya.ru?q=1234",
            "www.wikipedia.org",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
            "links"
        ]
    }
    test_data3 = {}
    response1 = client.post(POST_URL, json=test_data1).get_json()
    expected_response1 = {"status": 'ok'}
    response2 = client.post(POST_URL, json=test_data2).get_json()
    expected_response2 = {"status": 'Нет ссылок'}
    response3 = client.post(POST_URL, json=test_data3).get_json()
    expected_response3 = {"status": 'Нет ссылок'}
    assert response1 == expected_response1
    assert response2 == expected_response2
    assert response3 == expected_response3


def test_get_domains(client):
    client.post(POST_URL, json=TEST_DATA)
    response = client.get(GET_URL)
    expected_response = {
        "domains": [
            "funbox.ru",
            "github.com",
            "stackoverflow.com",
            "ya.ru"
        ],
        "status": "ok"
    }
    assert response.get_json() == expected_response


def test_get_wrong_parameters(client):
    client.post(POST_URL, json=TEST_DATA)
    response1_1 = client.get("/visited_domains?from=1&to=154521763822&too=2134").get_json()['status']
    response1_2 = client.get("/visited_domains?to=123456789&from=1").get_json()['status']
    response2_1 = client.get("/visited_domains?from=11235346&to=1").get_json()['status']
    response3_1 = client.get("/visited_domains").get_json()['status']
    response3_2 = client.get("/visited_domains?Fram=12&two=1").get_json()['status']
    response3_3 = client.get("/visited_domains?from=1&To=10000").get_json()['status']
    response3_4 = client.get("/visited_domains?from=hundred&to=million").get_json()['status']

    expected_response1 = 'ok'
    expected_response2 = 'Некорректный интервал времени'
    expected_response3 = 'Параметры url-адреса введены неверно'

    assert response1_1 == expected_response1
    assert response1_2 == expected_response1

    assert response2_1 == expected_response2

    assert response3_1 == expected_response3
    assert response3_2 == expected_response3
    assert response3_3 == expected_response3
    assert response3_4 == expected_response3


def test_get_empty_database(client):
    response = client.get(GET_URL).get_json()['status']
    assert response == "ok"
