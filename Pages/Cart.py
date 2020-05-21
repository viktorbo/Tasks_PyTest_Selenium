import allure
from selenium.common.exceptions import NoSuchElementException

from utils import BaseClass

@allure.description("Страница КОРЗИНА")
class Cart(BaseClass):
    @allure.step("Проверка наличия блузки в корзине.")
    def check_product_in_cart(self, item_name):
        try:
            """
            По-хорошему еще надо проверять сколько товаров было до этого в корзине и что после добавления одного товара
            в корзину добавляется только добавленный товар в правильном количестве, но я решил не отходить от пунктов в задаче.
            Также можно добавить проверку на соответствие stock-статуса в корзине для добавленного товара,
            но я не стал загромождать и излишне усложнять задание.
            """
            self.driver.find_element_by_xpath(
                "//div[@id='order-detail-content']/table[@id='cart_summary']/tbody/tr[@id='product_2_7_0_0']")
            print(f'{item_name} has been added to cart.')
            return True
        except NoSuchElementException:
            return False
