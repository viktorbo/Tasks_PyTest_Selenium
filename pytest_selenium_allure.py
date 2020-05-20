import os
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as driver_wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pytest

from pages import MainPage, SearchResult, Cart

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

    def wait_n_click_obj_xpath(self, obj_xpath=None, obj_name=None, obj_cls_name=None, wait=True, wait_time=None, click=True):
        if wait:
            driver_wait(self.driver, wait_time if wait_time else self.clickable_timeout).until(EC.element_to_be_clickable((By.XPATH, obj_xpath)))
        obj = None
        if obj_xpath:
            obj = self.driver.find_element_by_xpath(obj_xpath)
        elif obj_name:
            obj = self.driver.find_element_by_name(obj_name)
        elif obj_cls_name:
            obj = self.driver.find_element_by_class_name(obj_cls_name)
        if click:
            try:
                obj.click()
            except NoSuchElementException:
                raise NoSuchElementException(f"Object {obj_xpath} not found.")
            except:
                raise RuntimeError("Something went wrong.")

    def test_Add_to_Cart(self):
        item_name = 'Blouse'

        main_page = MainPage(self.driver, self.action)
        search_result = main_page.search(item_name)
        assert search_result.check_search(), f"{search_result.search_request} not found."
        assert search_result.check_stock(), f"No items with name '{search_result.search_request}'."
        search_result.add_to_cart()

        cart = search_result.go_to_cart()

        assert cart.check_product_in_cart(item_name), "Cart is empty."

    def test_Check_Specials(self):


        main_page = MainPage(self.driver, self.action)

        specials = main_page.go_to_women().go_to_specials()

        assert specials.check_discounts(), "Something went wrong. Check 'Specials' on web-site.\n" \
                                           "*(Maybe one or more products are displayed without a discount.)"

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
