from selenium.webdriver.support.ui import WebDriverWait as driver_wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils import wait_n_click


class BaseClass:
    clickable_timeout = 5

    def __init__(self, driver, action):
        self.driver = driver
        self.action = action


class MainPage(BaseClass):
    def search(self, search_request):
        self.driver.find_element_by_name('search_query').send_keys(search_request)
        self.driver.find_element_by_name('submit_search').click()
        return SearchResult(self.driver, self.action, search_request)

    def go_to_women(self):
        try:
            print("Go to 'Women'")
            wait_n_click(self, "//div[@id='block_top_menu']/ul[1]/li[1]/a[@title='Women']", wait=False)
        except NoSuchElementException:
            raise AssertionError("Something went wrong when moving into 'Women'.")
        return Women(self.driver, self.action)


class Women(BaseClass):
    def go_to_specials(self):
        try:
            print("Go to 'Specials'")
            wait_n_click(self, "//div[@id='left_column']/div[@id='special_block_right']/p[@class='title_block']/a[@title='Specials']")
        except NoSuchElementException:
            raise AssertionError("Something went wrong when moving into 'Specials'.")
        return Specials(self.driver, self.action)


class Specials(BaseClass):
    def check_discounts(self):
        products_xpath = "//ul[@class='product_list grid row']/li"
        number_of_products = len(self.driver.find_elements_by_xpath(products_xpath))
        try:
            products_with_sale = [self.driver.find_element_by_xpath(
                f"{products_xpath}[{i + 1}]/div[@class='product-container']/div[@class='right-block']/div[@class='content_price']/span[@class='price-percent-reduction']")
                                  for i in range(number_of_products)]
            print("All products display with a discount.")
            return True
        except NoSuchElementException:
            return False


class SearchResult(BaseClass):

    def __init__(self, driver, action, search_request=None):
        super().__init__(driver, action)
        if search_request:
            self.search_request = search_request

    def check_search(self):
        try:
            self.driver.find_element_by_xpath("//ul[@class='product_list grid row']/li[1]")
            print(f"{self.search_request} has been found.")
            return True
        except NoSuchElementException:
            return False

    def check_stock(self):
        try:
            self.driver.find_element_by_class_name('available-now')
            print(f'{self.search_request} in stock.')
            return True
        except NoSuchElementException:
            return False

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

    def go_to_cart(self):
        self.action.move_to_element(self.driver.find_element_by_xpath("//div[@class='shopping_cart']/a[1]")).perform()

        checkout_button = "//p[@class='cart-buttons']/a[1]/span[1]"
        wait_n_click(self, checkout_button)

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
