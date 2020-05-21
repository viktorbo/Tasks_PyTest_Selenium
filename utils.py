
from selenium.webdriver.support.ui import WebDriverWait as driver_wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class BaseClass:
    clickable_timeout = 5

    def __init__(self, driver, action):
        self.driver = driver
        self.action = action


def exit_browser(obj, original=False):
    try:
        obj.driver.quit()
    except:
        if original:
            raise RuntimeError("Something went wrong when closing the browser!")
        pass


def wait_n_click(self, xpath, wait=True, click=True):
    if wait:
        driver_wait(self.driver, self.clickable_timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    obj = self.driver.find_element_by_xpath(xpath)
    if click:
        try:
            obj.click()
        except NoSuchElementException:
            raise NoSuchElementException(f"Object with XPATH={xpath} not found.")
        except:
            raise RuntimeError("Something went wrong.")