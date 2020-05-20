
from selenium.webdriver.support.ui import WebDriverWait as driver_wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def wait_n_click(self, xpath, wait=True):
    if wait:
        driver_wait(self.driver, self.clickable_timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    self.driver.find_element_by_xpath(xpath).click()