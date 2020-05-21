from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as driver_wait

from Pages.Compare import Compare
from utils import wait_n_click, BaseClass


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
        assert str(self.max_products_to_compare) in self.driver.find_element_by_class_name(
            "fancybox-error").text, "Number of products in compare and number of products in error message don't match."
        assert str(pid) in self.driver.find_element_by_class_name(
            "fancybox-error").text, "Something went wrong with overlay calling. Check max number of products to compare."
        print("Overlay massage is correct.")
        wait_n_click(self, overlay_cross_xpath, wait=False)

    def add_products_to_compare(self):
        products_xpath = "//ul[@class='product_list grid row']/li"
        try:
            driver_wait(self.driver, self.clickable_timeout).until(
                EC.presence_of_element_located((By.XPATH, products_xpath)))
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
            wait_n_click(self, compare_button_xpath)
        except NoSuchElementException:
            raise AssertionError(f"Something went wrong when moving into 'Compare'.")
        return Compare(self.driver, self.action, self.product_properties)
