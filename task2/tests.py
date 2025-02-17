import pytest
from playwright.sync_api import sync_playwright
from advertisements_page import AdvertisementPage
from test_data_generator import TestDataGenerator

@pytest.fixture(scope="module")
def browser():
    """Открывает браузер один раз на все тесты"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()

@pytest.fixture(scope="module")
def test_data():
    """Создает набор данных, используемый во всех тестах"""
    tdg = TestDataGenerator()
    data = {
        "title": tdg.random_string(20),
        "price": tdg.random_number(),
        "description": tdg.random_string(20),
        "image_url": tdg.random_image_url(),
    }
    return data

@pytest.fixture(scope="module", autouse=True)
def setup_advertisement(browser, test_data):
    """Создает объявление перед тестами"""
    ap = AdvertisementPage(browser)
    ap.open()
    ap.create_ad(test_data["title"], test_data["price"], test_data["description"], test_data["image_url"])
    yield

def test_search_ad(browser, test_data):
    """Ищет объявление и проверяет его на соответствие полей с искомым"""
    ap = AdvertisementPage(browser)
    ap.open()
    ap.search_ad(test_data["title"])
    ap.verify_search_result(test_data["title"], test_data["price"], test_data["image_url"])

def test_edit_ad(browser, test_data):
    """Редактирует объявление и проверяет изменения"""
    ap = AdvertisementPage(browser)
    tdg = TestDataGenerator()

    new_data = {
        "title": tdg.random_string(15),
        "price": tdg.random_number(),
        "description": tdg.random_string(25),
        "image_url": tdg.random_image_url(),
    }

    ap.open()
    ap.open_ad_page(test_data["title"])
    ap.edit_ad(new_data["title"], new_data["price"], new_data["description"], new_data["image_url"])
    ap.verify_updated_ad(new_data["title"], new_data["price"], new_data["description"], new_data["image_url"])

def test_create_ad(browser, test_data):
    """Создает объявление и проверяет, что оно создалось и данные передались корректно"""
    ap = AdvertisementPage(browser)
    ap.open()
    ap.create_ad(test_data["title"], test_data["price"], test_data["description"], test_data["image_url"])
    ap.verify_ad_not_visible()
    ap.search_ad(test_data["title"])
    ap.verify_search_result(test_data["title"], test_data["price"], test_data["image_url"])
