import os
import sys
from pathlib import Path
from selenium import webdriver
import pytest
from utils import exit_browser
from Pages.MainPage import MainPage


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

        main_page = MainPage(self.driver, self.action)

        dresses = main_page.go_to_dresses()
        dresses.add_products_to_compare()

        compare = dresses.go_to_compare()

        products_before_remove = compare.check_products()
        compare.remove_product()
        products_after_remove = compare.check_products()
        assert len(products_before_remove)-len(products_after_remove) == 1, "Problems with COMPARE function."
        print("Product comparison works correctly.")
