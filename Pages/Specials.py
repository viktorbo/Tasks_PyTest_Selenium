from selenium.common.exceptions import NoSuchElementException

from utils import BaseClass


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
