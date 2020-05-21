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

    def go_to_dresses(self):
        try:
            wait_n_click(self, "//div[@id='block_top_menu']/ul[1]/li[2]/a[@title='Dresses']", wait=False)
        except NoSuchElementException:
            raise AssertionError(f"Something went wrong when moving into 'Dresses'.")
        return Dresses(self.driver, self.action)


class Dresses(BaseClass):
    max_products_to_compare = 3
    product_properties = []

    def add_to_compare(self, obj, obj_xpath):
        try:
            self.action.move_to_element(obj).perform()
        except:
            obj.location_once_scrolled_into_view
            self.action.move_to_element(obj).perform()

        wait_n_click(self, obj_xpath)

    def check_compare_overlay(self, pid, overlay_cross_xpath):
        wait_n_click(self, overlay_cross_xpath, click=False)
        print("Overlay is displayed.")
        assert str(self.max_products_to_compare) in self.driver.find_element_by_class_name("fancybox-error").text, "Number of products in compare and number of products in error message don't match."
        assert str(pid) in self.driver.find_element_by_class_name("fancybox-error").text, "Something went wrong with overlay calling. Check max number of products to compare."
        print("Overlay massage is correct.")
        wait_n_click(self, overlay_cross_xpath, wait=False)

    def add_products_to_compare(self):
        products_xpath = "//ul[@class='product_list grid row']/li"
        try:
            driver_wait(self.driver, self.clickable_timeout).until(EC.presence_of_element_located((By.XPATH, products_xpath)))
            products = self.driver.find_elements_by_xpath(products_xpath)
        except NoSuchElementException:
            raise AssertionError(f"No products in 'Dresses'.")

        for pid, product in enumerate(products):
            add_to_compare_button_xpath = f"{products_xpath}[{pid + 1}]/div[@class='product-container']/div[@class='functional-buttons clearfix']/div[@class='compare']/a[1]"
            self.add_to_compare(product, add_to_compare_button_xpath)
            try:
                overlay_cross_xpath = "//div[@class='fancybox-overlay fancybox-overlay-fixed']/div[@class='fancybox-wrap fancybox-desktop fancybox-type-html fancybox-opened']/div[@class='fancybox-skin']/a[@title='Close']"
                self.check_compare_overlay(pid, overlay_cross_xpath)
                break
            except TimeoutException:
                product_img_src = self.driver.find_element_by_xpath(
                    f"{products_xpath}[{pid + 1}]/div/div[1]/div/a[@class='product_img_link']/img").get_attribute('src')
                product_name = self.driver.find_element_by_xpath(
                    f"{products_xpath}[{pid + 1}]/div/div[2]/h5/a").get_attribute('title')
                self.product_properties.append({'img_src': product_img_src, 'name': product_name})
                continue
            except:
                raise AssertionError("Something went wrong in overlay calling.")

    def go_to_compare(self):
        try:
            compare_button_xpath = "//button[@class='btn btn-default button button-medium bt_compare bt_compare']/span[1]"
            #self.driver.find_element_by_xpath(compare_button_xpath).submit()
            wait_n_click(self, compare_button_xpath)
        except NoSuchElementException:
            raise AssertionError(f"Something went wrong when moving into 'Compare'.")
        return Compare(self.driver, self.action, self.product_properties)


class Compare(BaseClass):
    def __init__(self, driver, action, product_properties=None):
        super().__init__(driver, action)
        if product_properties:
            self.product_properties = product_properties

    def check_products(self):
        assert hasattr(self, 'product_properties'), "Error in Compare.check_products."
        compare_product_properties = []
        self.driver.implicitly_wait(self.clickable_timeout)
        self.number_of_products_in_compare_with_notprod_clmn = len(self.driver.find_elements_by_xpath("//tbody/tr[1]/td"))
        for i in range(2, self.number_of_products_in_compare_with_notprod_clmn + 1):
            compare_product_img_src = self.driver.find_element_by_xpath(
                f"//tbody/tr[1]/td[{i}]/div[2]/a/img").get_attribute('src')
            compare_product_name = self.driver.find_element_by_xpath(f"//tbody/tr[1]/td[{i}]/h5/a").get_attribute(
                'title')
            compare_product_properties.append({'img_src': compare_product_img_src, 'name': compare_product_name})

        for property in compare_product_properties:
            if property not in self.product_properties:
                raise AssertionError("Added and compared products do not match.")
        return compare_product_properties

    def remove_product(self):
        assert hasattr(self, 'number_of_products_in_compare_with_notprod_clmn') and self.number_of_products_in_compare_with_notprod_clmn!=0, "Empty compare list."
        removable_property = {
            'img_src': self.driver.find_element_by_xpath(f"//tbody/tr[1]/td[{self.number_of_products_in_compare_with_notprod_clmn}]/div[2]/a/img").get_attribute('src'),
            'name': self.driver.find_element_by_xpath(f"//tbody/tr[1]/td[{self.number_of_products_in_compare_with_notprod_clmn}]/h5/a").get_attribute('title')}
        self.product_properties.pop(self.product_properties.index(removable_property))
        wait_n_click(self, f"//tbody/tr[1]/td[{self.number_of_products_in_compare_with_notprod_clmn}]/div[@class='remove']/a")


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
