import pytest
from playwright.sync_api import sync_playwright
from pages.main_page import MainPage


@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()


def test_create_ad(browser):
    main_page = MainPage(browser)
    main_page.open()

    main_page.click_create_ad()
    assert browser.is_visible(MainPage.xpath_header_create), "Окно создания не появилось"

    main_page.fill_ad_form("Продам велосипед", "5000", "Отличный велосипед!", "http://image.com/bike.jpg")
    main_page.save_ad()

    assert browser.is_visible("//div[contains(text(), 'Объявление опубликовано')]"), "Объявление не опубликовано"
