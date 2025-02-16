from playwright.sync_api import Page

class MainPage:
    xpath_button_create = "//button[text()='Создать']"
    xpath_header_create = "//header[text()='Создать объявление']"
    xpath_input_name = "//input[@placeholder='Название']"
    xpath_input_price = "//input[@placeholder='Цена']"
    xpath_input_description = "//input[@placeholder='Описание']"
    xpath_input_image_url = "//input[@placeholder='Ссылка на изображение']"
    xpath_button_save = "//button[text()='Сохранить']"
    xpath_input_search = "//input[@placeholder='Поиск по объявлениям']"
    xpath_button_search = "//button[@class='chakra-button css-1oamcjg' and text()='Найти']"
    xpath_grid = "//div[@class='css-1w07v7s']"
    xpath_ad_card = "//div[@class='css-1s2t5t1']"
    xpath_ad_card_image = "//div[@class='chakra-image css-cwl1kn']"
    xpath_ad_card_name = "//div[@class='css-rkqtls']"
    xpath_ad_card_price = "//div[@class='css-1n43xc7']"
    xpath_ad_page

    def __init__(self, page: Page):
        self.page = page
        self.url = "http://tech-avito-intern.jumpingcrab.com/advertisements/"

    def open(self):
        self.page.goto(self.url)

    def click_create_ad(self):
        self.page.click(self.xpath_button_create)

    def fill_ad_form(self, title, price, description, image_url):
        self.page.fill(self.xpath_input_name, title)
        self.page.fill(self.xpath_input_price, price)
        self.page.fill(self.xpath_input_description, description)
        self.page.fill(self.xpath_input_image_url, image_url)

    def save_ad(self):
        self.page.click(self.xpath_button_save)
