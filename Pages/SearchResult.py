import allure
from selenium.common.exceptions import NoSuchElementException

from Pages.Cart import Cart
from utils import wait_n_click, BaseClass


@allure.description("Страница поиска")
class SearchResult(BaseClass):

    def __init__(self, driver, action, search_request=None):
        super().__init__(driver, action)
        if search_request:
            self.search_request = search_request

    @allure.step("Проверка найденных товаров (Блузки).")
    def check_search(self):
        try:
            self.driver.find_element_by_xpath("//ul[@class='product_list grid row']/li[1]")
            print(f"{self.search_request} has been found.")
            return True
        except NoSuchElementException:
            return False

    @allure.step("Проверка наличия найденных товаров (Блузки).")
    def check_stock(self):
        try:
            self.driver.find_element_by_class_name('available-now')
            print(f'{self.search_request} in stock.')
            return True
        except NoSuchElementException:
            return False

    @allure.step("Добавление в корзину.")
    def add_to_cart(self):
        self.action.move_to_element(self.driver.find_element_by_class_name('right-block')).perform()

        try:
            add_to_cart_button_xpath = "//div[@class='button-container']/a[@title='Add to cart']"
            wait_n_click(self, add_to_cart_button_xpath)
        except:
            raise AssertionError("Problems with 'Add to cart' button.")

        try:
            continue_shopping_button = "//div[@class='layer_cart_cart col-xs-12 col-md-6']/div[@class='button-container']/span[@title='Continue shopping']"
            wait_n_click(self, continue_shopping_button)
        except:
            raise AssertionError("Problems with 'Continue shopping' button.")

    @allure.step("Переход в корзину.")
    def go_to_cart(self):
        self.action.move_to_element(self.driver.find_element_by_xpath("//div[@class='shopping_cart']/a[1]")).perform()

        checkout_button = "//p[@class='cart-buttons']/a[1]/span[1]"
        wait_n_click(self, checkout_button)

        return Cart(self.driver, self.action)
