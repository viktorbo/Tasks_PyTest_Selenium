import allure

from utils import wait_n_click, BaseClass


@allure.description("Страница сравнения товаров.")
class Compare(BaseClass):
    def __init__(self, driver, action, product_properties=None):
        super().__init__(driver, action)
        if product_properties:
            self.product_properties = product_properties

    @allure.step("Проверка текущих товаров в сравнении.")
    def check_products(self):
        assert hasattr(self, 'product_properties'), "Error in Compare.check_products."
        compare_product_properties = []
        self.driver.implicitly_wait(self.clickable_timeout)
        self.number_of_products_in_compare_with_notprod_clmn = len(
            self.driver.find_elements_by_xpath("//tbody/tr[1]/td"))
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

    @allure.step("Удаление одного из продуктов в сравнении.")
    def remove_product(self):
        assert hasattr(self,
                       'number_of_products_in_compare_with_notprod_clmn') and self.number_of_products_in_compare_with_notprod_clmn != 0, "Empty compare list."
        removable_property = {
            'img_src': self.driver.find_element_by_xpath(
                f"//tbody/tr[1]/td[{self.number_of_products_in_compare_with_notprod_clmn}]/div[2]/a/img").get_attribute(
                'src'),
            'name': self.driver.find_element_by_xpath(
                f"//tbody/tr[1]/td[{self.number_of_products_in_compare_with_notprod_clmn}]/h5/a").get_attribute(
                'title')}
        self.product_properties.pop(self.product_properties.index(removable_property))
        wait_n_click(self,
                     f"//tbody/tr[1]/td[{self.number_of_products_in_compare_with_notprod_clmn}]/div[@class='remove']/a")
