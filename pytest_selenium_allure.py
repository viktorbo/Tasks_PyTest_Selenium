import os
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as driver_wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pytest

def exit_browser(obj, original = False):
    try:
        obj.driver.quit()
    except:
        if original:
            raise RuntimeError("Something went wrong when closing the browser!")
        pass

@pytest.fixture(scope='class')
def browser_env(request):
    request.cls.resource_path = 'http://automationpractice.com'
    request.cls.driver_path = Path(os.getcwd()) / ('geckodriver' + ('.exe' if 'win' in sys.platform else ''))
    request.cls.clickable_timeout = 5
    yield
    exit_browser(request.cls)


@pytest.fixture(scope='function')
def browser_run(request):
    print(f'\nSetup driver...\n'
          f'Path to driver: {request.cls.driver_path}')
    request.cls.driver = webdriver.Firefox(executable_path=str(request.cls.driver_path))
    request.cls.action = webdriver.ActionChains(request.cls.driver)
    print(f'Running driver...\n'
          f'Site: {request.cls.resource_path}')
    try:
        request.cls.driver.get(request.cls.resource_path)
    except:
        raise AssertionError("Problems with driver.get(...)")
    yield
    exit_browser(request.cls, original=True)


@pytest.mark.usefixtures('browser_env', 'browser_run')
class Test_Site_with_Clothes:

    def wait_n_click_obj_xpath(self, obj_xpath, wait=True, wait_time=None, click=True):
        if wait:
            driver_wait(self.driver, wait_time if wait_time else self.clickable_timeout).until(EC.element_to_be_clickable((By.XPATH, obj_xpath)))
        if click:
            try:
                self.driver.find_element_by_xpath(obj_xpath).click()
            except NoSuchElementException:
                raise  NoSuchElementException(f"Object {obj_xpath} not found.")
            except:
                raise RuntimeError("Something went wrong.")

    def test_Add_to_Cart(self):
        item_name = 'Blouse'
        self.driver.find_element_by_name('search_query').send_keys(item_name)
        self.driver.find_element_by_name('submit_search').click()

        #  SEARCH
        try:
            self.driver.implicitly_wait(self.clickable_timeout)
            self.driver.find_element_by_xpath("//ul[@class='product_list grid row']/li[1]")
            print(f"{item_name} has been found.")
        except NoSuchElementException:
            raise AssertionError(f"{item_name} not found.")

        #  STOCK CHECKING
        """
        Проверяется только наличие элемента с надписью 'In stock' после поиска блузки.
        Ожидается, что будет найдена одна блузка.
        Товаров с подписью "не в наличии" на тестовом сайте я не обнаружил,
        поэтому проверка реализована так.
        """
        try:
            self.driver.find_element_by_class_name('available-now')
            print(f'{item_name} in stock.')
        except NoSuchElementException:
            print(f'No items with name "{item_name}".')
            raise AssertionError(f"Item {item_name} not in stock.")

        #  ADDING TO CART
        self.action.move_to_element(self.driver.find_element_by_class_name('right-block')).perform()

        add_to_cart_button_xpath = "//div[@class='button-container']/a[@title='Add to cart']"
        self.wait_n_click_obj_xpath(add_to_cart_button_xpath)

        continue_shopping_button = "//div[@class='layer_cart_cart col-xs-12 col-md-6']/div[@class='button-container']/span[@title='Continue shopping']"
        self.wait_n_click_obj_xpath(continue_shopping_button)

        #  CART CHECKING
        self.action.move_to_element(self.driver.find_element_by_xpath("//div[@class='shopping_cart']/a[1]")).perform()

        checkout_button = "//p[@class='cart-buttons']/a[1]/span[1]"
        self.wait_n_click_obj_xpath(checkout_button)

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
        except NoSuchElementException:
            raise AssertionError("Cart is empty.")

    def test_Check_Specials(self):
        transition_sequence = ['Women', 'Specials']
        seq_iterator = iter(transition_sequence)

        #  GO TO 'WOMEN / SPECIALS'
        try:
            self.driver.find_element_by_xpath(f"//div[@id='block_top_menu']/ul[1]/li[1]/a[@title='{next(seq_iterator)}']").click()
            self.driver.find_element_by_xpath(f"//div[@id='left_column']/div[@id='special_block_right']/p[@class='title_block']/a[@title='{next(seq_iterator)}']").click()
        except NoSuchElementException:
            raise AssertionError(f"Something went wrong when moving into {'/'.join(transition_sequence)}.")

        #  SALE CHECKING
        products_xpath = "//ul[@class='product_list grid row']/li"
        number_of_products = len(self.driver.find_elements_by_xpath(products_xpath))
        try:
            products_with_sale = [self.driver.find_element_by_xpath(f"{products_xpath}[{i+1}]/div[@class='product-container']/div[@class='right-block']/div[@class='content_price']/span[@class='price-percent-reduction']") for i in range(number_of_products)]
            print("All products display with a discount.")
        except NoSuchElementException:
            raise AssertionError(f"Something went wrong. Check {'/'.join(transition_sequence)} on web-site.\n"
                                 f"*(Maybe one or more products are displayed without a discount.)")

    def test_Products_Comparison(self):
        max_products_to_compare = 3
        target_name = 'Dresses'

        #  ADDING PRODUCTS TO COMPARE AND CHECKING OVERLAY
        try:
            self.driver.find_element_by_xpath(f"//div[@id='block_top_menu']/ul[1]/li[2]/a[@title='{target_name}']").click()
        except NoSuchElementException:
            raise AssertionError(f"Something went wrong when moving into '{target_name}'.")

        products_xpath = "//ul[@class='product_list grid row']/li"
        try:
            products = self.driver.find_elements_by_xpath(products_xpath)
        except NoSuchElementException:
            raise AssertionError(f"No products in '{target_name}'.")

        product_properties = []

        for pid, product in enumerate(products):

            try:
                self.action.move_to_element(product).perform()
            except:
                product.location_once_scrolled_into_view
                self.action.move_to_element(product).perform()

            add_to_compare_button_xpath = f"{products_xpath}[{pid+1}]/div[@class='product-container']/div[@class='functional-buttons clearfix']/div[@class='compare']/a[1]"
            self.wait_n_click_obj_xpath(add_to_compare_button_xpath)

            try:
                overlay_cross_xpath = "//div[@class='fancybox-overlay fancybox-overlay-fixed']/div[@class='fancybox-wrap fancybox-desktop fancybox-type-html fancybox-opened']/div[@class='fancybox-skin']/a[@title='Close']"
                self.wait_n_click_obj_xpath(overlay_cross_xpath, click=False)
                print("Overlay is displayed.")
                assert str(max_products_to_compare) in self.driver.find_element_by_class_name("fancybox-error").text, "Number of products in compare and number of products in error message don't match."
                assert str(pid) in self.driver.find_element_by_class_name("fancybox-error").text, "Something went wrong with overlay calling. Check max number of products to compare."
                print("Overlay massage is correct.")
                self.wait_n_click_obj_xpath(overlay_cross_xpath, wait=False)
                break
            except TimeoutException:
                product_img_src = self.driver.find_element_by_xpath(
                    f"{products_xpath}[{pid + 1}]/div/div[1]/div/a[@class='product_img_link']/img").get_attribute('src')
                product_name = self.driver.find_element_by_xpath(
                    f"{products_xpath}[{pid + 1}]/div/div[2]/h5/a").get_attribute('title')
                product_properties.append({'img_src': product_img_src, 'name': product_name})
                continue
            except:
                raise AssertionError("Something went wrong in overlay calling.")

        #  GO TO 'COMPARE'
        try:
            target_name = "Compare"
            compare_button_xpath = "//button[@class='btn btn-default button button-medium bt_compare bt_compare']/span[1]"
            self.driver.find_element_by_xpath(compare_button_xpath).submit()

        except NoSuchElementException:
            raise AssertionError(f"Something went wrong when moving into '{target_name}'.")

        #  CHECK COMPARING PRODUCTS
        #  Это можно в одну строчку сделать, но это будет громоздко и нечитаемо
        self.driver.implicitly_wait(self.clickable_timeout)
        compare_product_properties = []
        for i in range(2, len(self.driver.find_elements_by_xpath("//tbody/tr[1]/td"))+1):
            compare_product_img_src = self.driver.find_element_by_xpath(f"//tbody/tr[1]/td[{i}]/div[2]/a/img").get_attribute('src')
            compare_product_name = self.driver.find_element_by_xpath(f"//tbody/tr[1]/td[{i}]/h5/a").get_attribute('title')
            compare_product_properties.append({'img_src': compare_product_img_src, 'name': compare_product_name})

        for property in compare_product_properties:
            if property not in product_properties:
                raise AssertionError("Added and compared products do not match.")

        #  REMOVE ONE OF PRODUCTS IN COMPARING
        removable_property = {'img_src': self.driver.find_element_by_xpath(f"//tbody/tr[1]/td[{i}]/div[2]/a/img").get_attribute('src'),
                              'name': self.driver.find_element_by_xpath(f"//tbody/tr[1]/td[{i}]/h5/a").get_attribute('title')}
        compare_product_properties.pop(compare_product_properties.index(removable_property))
        self.driver.find_element_by_xpath(f"//tbody/tr[1]/td[{i}]/div[@class='remove']/a").click()

        #  CHECKING COMPARING PRODUCTS
        chck_compare_product_properties = []
        for i in range(2, len(self.driver.find_elements_by_xpath("//tbody/tr[1]/td")) + 1):
            chck_compare_product_img_src = self.driver.find_element_by_xpath(
                f"//tbody/tr[1]/td[{i}]/div[2]/a/img").get_attribute('src')
            chck_compare_product_name = self.driver.find_element_by_xpath(f"//tbody/tr[1]/td[{i}]/h5/a").get_attribute(
                'title')
            chck_compare_product_properties.append({'img_src': chck_compare_product_img_src, 'name': chck_compare_product_name})

        for property in chck_compare_product_properties:
            if property not in compare_product_properties:
                raise AssertionError("Expected and current products do not match.")

        print("Product comparison works correctly.")

