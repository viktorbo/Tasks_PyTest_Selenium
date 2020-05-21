from selenium.common.exceptions import NoSuchElementException

from Pages.Dresses import Dresses
from Pages.SearchResult import SearchResult
from Pages.Women import Women
from utils import wait_n_click, BaseClass


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
