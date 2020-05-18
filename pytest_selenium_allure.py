import os
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as driver_wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import select


class Test_Site_with_Clothes:
    def setup_class(self):
        self.resource_path = 'http://automationpractice.com'
        self.driver_path = Path(os.getcwd()) / ('geckodriver' + ('.exe' if 'win' in sys.platform else ''))
        self.clickable_timeout = 10

    def setup_method(self):
        print(f'Setup driver for test class.\n'
              f'Path to driver: {self.driver_path}')
        self.driver = webdriver.Firefox(executable_path=str(self.driver_path))
        self.action = webdriver.ActionChains(self.driver)

    def setup(self):
        print(f'Running driver...\n'
              f'Site: {self.resource_path}')
        try:
            self.driver.get(self.resource_path)
        except:
            raise AssertionError("Problems with driver.get(...)")

    def teardown_method(self):
        try:
            self.driver.quit()
        except:
            raise AssertionError("Something went wrong.")
        print("Browser has been closed.")

    def teardown_class(self):
        try:
            self.driver.quit()
            print("Driver has been closed (with 'quit').")
        except:
            print("Driver was closed (with 'quit').")

    def test_add_to_cart(self):
        item_name = 'Blouse'
        self.driver.find_element_by_name('search_query').send_keys(item_name)
        self.driver.find_element_by_name('submit_search').click()

        #  Search
        try:
            self.driver.find_element_by_xpath("//ul[@class='product_list grid row']/li[1]")
            print(f"{item_name} has been found.")
        except NoSuchElementException:
            raise AssertionError(f"{item_name} not found.")

        #  Stock checking
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

        #  Adding to cart
        self.action.move_to_element(self.driver.find_element_by_class_name('right-block'))
        self.action.perform()

        add_to_cart_button_xpath = "//div[@class='button-container']/a[@title='Add to cart']"
        driver_wait(self.driver, self.clickable_timeout).until(
            EC.element_to_be_clickable((By.XPATH, add_to_cart_button_xpath)))
        self.driver.find_element_by_xpath(add_to_cart_button_xpath).click()

        continue_shopping_button = "//div[@class='layer_cart_cart col-xs-12 col-md-6']/div[@class='button-container']/span[@title='Continue shopping']"
        driver_wait(self.driver, self.clickable_timeout).until(
            EC.element_to_be_clickable((By.XPATH, continue_shopping_button)))
        self.driver.find_element_by_xpath(continue_shopping_button).click()

        #  Cart checking
        self.action.move_to_element(self.driver.find_element_by_xpath("//div[@class='shopping_cart']/a[1]"))
        self.action.perform()

        checkout_button = "//p[@class='cart-buttons']/a[1]/span[1]"
        driver_wait(self.driver, self.clickable_timeout).until(EC.element_to_be_clickable((By.XPATH, checkout_button)))
        self.driver.find_element_by_xpath(checkout_button).click()

        try:
            """
            Также можно добавить проверку на соответствие stock-статуса в корзине для добавленного товара,
            но я не стал загромождать и излишне усложнять задание.
            """
            self.driver.find_element_by_xpath(
                "//div[@id='order-detail-content']/table[@id='cart_summary']/tbody/tr[@id='product_2_7_0_0']")
            print(f'{item_name} has been added to cart.\n'
                  f'TEST PASSED')
        except NoSuchElementException:
            print("Cart is empty.")
            raise AssertionError("FAILED")
