import random
import string

class TestDataGenerator:

    @staticmethod
    def random_string(length=10):
        """Генерирует случайную строку из букв и цифр"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def random_number():
        """Генерирует случайное число от 100 до 10000"""
        return str(random.randint(100, 10000))

    @staticmethod
    def random_image_url():
        """Генерирует случайную ссылку на изображение"""
        return f"https://picsum.photos/200?random={random.randint(1, 1000)}"
