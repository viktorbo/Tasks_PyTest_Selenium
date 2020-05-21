import allure
from selenium.common.exceptions import NoSuchElementException

from Pages.Specials import Specials
from utils import wait_n_click, BaseClass


@allure.description("Страница Woman")
class Women(BaseClass):
    @allure.step("Переход к Specials.")
    def go_to_specials(self):
        try:
            print("Go to 'Specials'")
            wait_n_click(self, "//div[@id='left_column']/div[@id='special_block_right']/p[@class='title_block']/a[@title='Specials']")
        except NoSuchElementException:
            raise AssertionError("Something went wrong when moving into 'Specials'.")
        return Specials(self.driver, self.action)
