from selenium.webdriver.support.ui import WebDriverWait as driver_wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class BaseClass:
    def __init__(self, driver, action):
        self.driver = driver
        self.action = action


class MainPage(BaseClass):
    def search(self, search_request):
        self.driver.find_element_by_name('search_query').send_keys(search_request)
        self.driver.find_element_by_name('submit_search').click()
        return SearchResult(self.driver, self.action, search_request)


class SearchResult(BaseClass):
    clickable_timeout = 5

    def __init__(self, driver, action, search_request=None):
        super().__init__(driver, action)
        if search_request:
            self.search_request = search_request

    def wait_n_click(self, xpath):
        driver_wait(self.driver, self.clickable_timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def check_search(self):
        try:
            self.driver.find_element_by_xpath("//ul[@class='product_list grid row']/li[1]")
            print(f"{self.search_request} has been found.")
        except NoSuchElementException:
            raise AssertionError(f"{self.search_request} not found.")

    def check_stock(self):
        try:
            self.driver.find_element_by_class_name('available-now')
            print(f'{self.search_request} in stock.')
            return True
        except NoSuchElementException:
            print(f'No items with name "{self.search_request}".')
            return False

    def add_to_cart(self):
        self.action.move_to_element(self.driver.find_element_by_class_name('right-block')).perform()

        try:
            add_to_cart_button_xpath = "//div[@class='button-container']/a[@title='Add to cart']"
            self.wait_n_click(add_to_cart_button_xpath)
        except:
            raise AssertionError("Problems with 'Add to cart' button.")

        try:
            continue_shopping_button = "//div[@class='layer_cart_cart col-xs-12 col-md-6']/div[@class='button-container']/span[@title='Continue shopping']"
            self.wait_n_click(continue_shopping_button)
        except:
            raise AssertionError("Problems with 'Continue shopping' button.")

    def go_to_cart(self):
        self.action.move_to_element(self.driver.find_element_by_xpath("//div[@class='shopping_cart']/a[1]")).perform()

        checkout_button = "//p[@class='cart-buttons']/a[1]/span[1]"
        self.wait_n_click(checkout_button)

        return Cart(self.driver, self.action)


class Cart(BaseClass):
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
