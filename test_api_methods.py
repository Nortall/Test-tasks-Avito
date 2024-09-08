import requests
import pytest


# Константы
BASE_URL = "https://qa-internship.avito.com/api/1/"
POST_ITEM_URL = f"{BASE_URL}item"
GET_ITEM_URL = f"{BASE_URL}item/"
SELLER_ENDPOINT = "/item"

# Переменные
valid_ad_id = "70dfbe84-5ecb-46ba-8782-67598440dfa6"
valid_sellerId = 3452
valid_limit = 5
valid_offset = 5

invalid_limit = "5@#41fd"
invalid_offset = "adsf@@"

# Тестовые данные

# Валидные значения параметров для метода POST (покрывают тест-кейсы ТС-1 - ТС-6, исключая ТС-5)
valid_data = [
    {
        "name": "Телефон",
        "price": 25000,
        "sellerId": 3455,
        "statistics": {
            "contacts": 100,
            "like": 43,
            "viewCount": 140
        },
    },
    {
        "price": 27000,
        "sellerId": 3456,
        "statistics": {
            "contacts": 102,
            "like": 21,
            "viewCount": 112
        },
    },

    {
        "name": "Телефон",
        "sellerId": 3457,
        "statistics": {
            "contacts": 15,
            "like": 12,
            "viewCount": 22
        },
    },

    {
        "name": "Телефон",
        "price": 37000,
        "statistics": {
            "contacts": 100,
            "like": 43,
            "viewCount": 140
        },
    },

    {
        "name": "",
        "statistics": {
        },
    }
]

# Для ТС-5 (отсутствие параметра 'statistics' приводит к багу B-1)
bug_data = [
    {
        "name": "Телефон",
        "price": 37000,
        "sellerId": 3457,
    },
]

# Невалидные значения параметров для метода POST (покрывают тест-кейсы ТС-7 и ТС-8)
invalid_data = [
    {
        "name": 1234,
        "price": "price",
        "sellerId": "id2",
        "statistics": {
        }
    },
    {

    }
]

# Невалидные значения для метода GET (Получение объявления по его идентификатору, покрывают ТС-11 и ТС-12)
ad_id_data = [
    ("70dfbe84-5ecb-46ba-8782-99998440dfa6"),
    ("@@@@@@@@@@")
]

# Невалидные значения для метода GET (Получение всех объявлений по идентификатору продавца, покрывают ТС-15 и ТС-16)
invalid_sellerId = [
    ("111111111111111111111"),
    ("@@@@@!!!!&&&")
]


# Фикстура для получения URL с sellerId
@pytest.fixture
def get_url_with_sellerId():
    return f"{BASE_URL}/{valid_sellerId}{SELLER_ENDPOINT}"


# Тесты

@pytest.mark.parametrize("valid_data", valid_data)
def test_post_create_ad_valid_data(valid_data):
    """ТС-1 - ТС-6, исключая ТС-5"""
    response = requests.post(POST_ITEM_URL, json=valid_data)
    assert response.status_code == 200, "Expected status code '200', but it was not found!"
    data = response.json()
    assert 'status' in data, "Expected 'status' in response, but it was not found"


@pytest.mark.parametrize("bug_data", bug_data)
@pytest.mark.xfail(reason="Баг на стороне сервера, возвращает статус код 500, вместо 200")
def test_post_create_ad_bug_data(bug_data):
    """ТС-5"""
    response = requests.post(POST_ITEM_URL, json=bug_data)
    assert response.status_code == 200, "Expected status code '200', but it was not found!"
    data = response.json()
    assert 'status' in data, "Expected 'status' in response, but it was not found"


@pytest.mark.parametrize("invalid_data", invalid_data)
@pytest.mark.xfail(reason="Баг на стороне сервера, возвращается статус код 500 вместо 200", strict=False) #баг, связанный с ТС-7
def test_post_create_ad_invalid_data(invalid_data):
    """ТС-7 и ТС-8"""
    response = requests.post(POST_ITEM_URL, json=invalid_data)
    assert response.status_code == 400, "Expected status code '400', but it was not found!"
    data = response.json()
    assert 'message' in data, "Expected 'message' in response, but it was not found"


def test_post_wihtout_body():
    """ТС-9"""
    response = requests.post(POST_ITEM_URL)
    assert response.status_code == 400, "Expected status code '400', but it was not found!"
    data = response.json()
    assert len(data) > 0


def test_get_ad_by_valid_id():
    """ТС-10"""
    response = requests.get(GET_ITEM_URL + valid_ad_id)
    assert response.status_code == 200, "Expected status code '200', but it was not found!"
    data = response.json()
    assert data[0]['id'] == valid_ad_id, "Expected 'id' in response, but it was not found"


@pytest.mark.parametrize("ad_id_data", ad_id_data)
def test_get_ad_by_invalid_id(ad_id_data):
    """ТС-11 и ТС-12"""
    response = requests.get(GET_ITEM_URL + str(ad_id_data))
    assert response.status_code == 404, "Expected status code '404', but it was not found!"
    data = response.json()
    assert 'status' in data, "Expected 'status' in response, but it was not found"


def test_get_ad_without_id():
    """ТС-13"""
    response = requests.get(GET_ITEM_URL)
    assert response.status_code == 404, "Expected status code '404', but it was not found!"
    data = response.json()
    assert 'code' in data, "Expected 'code' in response, but it was not found"


def test_get_ads_by_valid_sellerId(get_url_with_sellerId):
    """ТС-14"""
    response = requests.get(f"{get_url_with_sellerId}")
    assert response.status_code == 200, "Expected status code '200', but it was not found!"
    data = response.json()
    assert len(data) > 0


@pytest.mark.parametrize("invalid_sellerId", invalid_sellerId)
@pytest.mark.xfail(reason="Баг на стороне сервера, возвращается статус код 200 вместо 404")
def test_get_ads_by_invalid_sellerId(invalid_sellerId, get_url_with_sellerId):
    """ТС-15 и ТС-16"""
    response = requests.get(f"{get_url_with_sellerId}")
    assert response.status_code == 404, "Expected status code '404', but it was not found!"
    data = response.json()
    assert 'status' in data, "Expected 'status' in response, but it was not found"


@pytest.mark.xfail(reason="Баг на стороне сервера, параметр limit не влияет на работу метода")
def test_get_ads_with_limit(get_url_with_sellerId):
    """ТС-17"""
    response = requests.get(f"{get_url_with_sellerId}?limit={valid_limit}")
    assert response.status_code == 200, "Expected status code '200', but it was not found!"
    data = response.json()
    assert len(data) == 5


@pytest.mark.xfail(reason="Баг на стороне сервера, параметр offset не влияет на работу метода")
def test_get_ads_with_offset(get_url_with_sellerId):
    """ТС-18"""
    response_without_offset = requests.get(f"{get_url_with_sellerId}")
    assert response_without_offset.status_code == 200, "Expected status code '200', but it was not found!"
    data_withouth_offset = response_without_offset.json()
    assert len(data_withouth_offset) > 0

    response_with_offset = requests.get(f"{get_url_with_sellerId}?offset={valid_offset}")
    assert response_with_offset.status_code == 200, "Expected status code '200', but it was not found!"
    data_with_offset = response_with_offset.json()
    assert len(data_with_offset) > 0

    assert data_withouth_offset != data_with_offset


@pytest.mark.xfail(reason="Баг на стороне сервера, параметры limit и offset не влияют на работу метода")
def test_get_abs_with_invalid_limit_and_offset(get_url_with_sellerId):
    """ТС-19"""
    response = requests.get(f"{get_url_with_sellerId}?limit={invalid_limit}&offset={invalid_offset}")
    assert response.status_code == 400, "Expected status code '400', but it was not found!"














