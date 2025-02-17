from playwright.sync_api import Page, expect


class AdvertisementPage:

    xpath_input_search = "//input[@placeholder='Поиск по объявлениям']"
    xpath_button_search = "//button[text()='Найти']"
    xpath_button_create = "//button[text()='Создать']"
    xpath_header_create = "//header[text()='Создать объявление']"
    xpath_input_name = "//input[@placeholder='Название']"
    xpath_input_price = "//input[@placeholder='Цена']"
    xpath_input_description = "//input[@placeholder='Описание']"
    xpath_input_image_url = "//input[@placeholder='URL изображения']"
    xpath_button_save = "//button[text()='Сохранить']"
    xpath_ad_card_name = "//h4[@class='css-rkqtls']"
    xpath_ad_card_price = "//div[@class='css-1n43xc7']"
    xpath_ad_card_image = "//img[@class='chakra-image css-cwl1kn']"
    xpath_ad_page_image = "//img[@class='chakra-image css-6ofinu']"
    xpath_ad_page_title = "//h2[@class='chakra-heading css-1mr9o9q']"
    xpath_ad_page_description = "//p[@class='chakra-text css-i3jkqk']"
    xpath_ad_page_price = "//p[@class='chakra-text css-r1bsln']"
    selector_ad_page_edit_and_confirm_button = "#root > div > div.chakra-container.css-1lle71m > div > div.css-nb383z > svg"
    xpath_ad_page_input_image = "//input[@name='imageUrl']"
    xpath_ad_page_input_title = "//input[@name='name']"
    xpath_ad_page_input_price = "//input[@name='price']"
    xpath_ad_page_input_description = "//textarea[@name='description']"

    def __init__(self, page: Page):
        self.page = page
        self.url = "http://tech-avito-intern.jumpingcrab.com/advertisements/"

    def open(self):
        """Открывает страницу объявлений"""
        self.page.goto(self.url)
        self.page.wait_for_selector(self.xpath_button_create)

    def create_ad(self, title, price, description, image_url):
        """Создает новое объявление"""
        self.page.click(self.xpath_button_create)
        expect(self.page.locator(self.xpath_header_create)).to_be_visible(timeout=5000)
        self.page.fill(self.xpath_input_name, title)
        self.page.fill(self.xpath_input_price, price)
        self.page.fill(self.xpath_input_description, description)
        self.page.fill(self.xpath_input_image_url, image_url)
        self.page.click(self.xpath_button_save)
        self.page.wait_for_selector(self.xpath_button_create)

    def verify_ad_not_visible(self):
        """Проверяет, что поп-ап создания объявления закрылся"""
        expect(self.page.locator(self.xpath_input_name)).not_to_be_visible()
        expect(self.page.locator(self.xpath_input_price)).not_to_be_visible()
        expect(self.page.locator(self.xpath_input_description)).not_to_be_visible()
        expect(self.page.locator(self.xpath_input_image_url)).not_to_be_visible()

    def search_ad(self, query):
        """Ищет объявление по названию"""
        self.page.fill(self.xpath_input_search, query)
        self.page.click(self.xpath_button_search)
        expect(self.page).to_have_url(f"{self.url}?q={query}")

    def open_ad_page(self, title):
        """Открывает страницу объявления после поиска по названию"""
        self.search_ad(title)
        self.page.click(f"{self.xpath_ad_card_name}[text()='{title}']")

    def verify_search_result(self, expected_name, expected_price, expected_image_url):
        """Проверяет карточку найденного объявления в поиске на соответствие полей"""
        self.page.wait_for_selector(self.xpath_ad_card_name)
        ad_name = self.page.inner_text(self.xpath_ad_card_name)
        ad_price = self.page.inner_text(self.xpath_ad_card_price).replace("\xa0", "").replace("₽", "")
        ad_image_src = self.page.get_attribute(self.xpath_ad_card_image, "src")

        assert ad_name == expected_name, f"Название не совпадает: {ad_name} != {expected_name}"
        assert ad_price == expected_price, f"Цена не совпадает: {ad_price} != {expected_price}"
        assert ad_image_src == expected_image_url, f"Изображение не совпадает: {ad_image_src} != {expected_image_url}"

    def edit_ad(self, new_title, new_price, new_description, new_image):
        """Редактирует объявление"""
        self.page.click(self.selector_ad_page_edit_and_confirm_button)
        self.page.fill(self.xpath_ad_page_input_title, new_title)
        self.page.fill(self.xpath_ad_page_input_price, new_price)
        self.page.fill(self.xpath_ad_page_input_description, new_description)
        self.page.fill(self.xpath_ad_page_input_image, new_image)
        self.page.click(self.selector_ad_page_edit_and_confirm_button)
        self.page.wait_for_selector(self.xpath_ad_page_title)
        self.page.reload()

    def verify_updated_ad(self, new_title, new_price, new_description, new_image):
        """Проверяет, что данные в карточке объявления изменились после редактирования"""
        title = self.page.inner_text(self.xpath_ad_page_title)
        price = self.page.inner_text(self.xpath_ad_page_price).replace("\xa0", "").replace("₽", "")
        description = self.page.inner_text(self.xpath_ad_page_description)
        image_src = self.page.get_attribute(self.xpath_ad_page_image, "src")

        assert title == new_title, f"Название не совпадает: {title} != {new_title}"
        assert price == new_price, f"Цена не совпадает: {price} != {new_price}"
        assert description == new_description, f"Описание не совпадает: {description} != {new_description}"
        assert image_src == new_image, f"Изображение не совпадает: {image_src} != {new_image}"
