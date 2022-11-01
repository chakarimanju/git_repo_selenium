from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.utils import Utils
import time


class BaseDriver:
    log = Utils.custom_logger()
    time_out = 60

    def __init__(self, driver):
        self.driver = driver

    def page_scroll(self):
        java_script = "window.scrollTo(0, document.body.scrollHeight);var pageLength=document.body.scrollHeight;return pageLength;"
        pageLength = self.driver.execute_script(java_script)
        match = False
        while (match == False):
            lastCount = pageLength
            time.sleep(1)
            pageLength = self.driver.execute_script()
            if lastCount == pageLength:
                match = True
        time.sleep(4)

    def wait_until_element_present(self, locator_type, locator):
        # wait 10 seconds before looking for element
        element = WebDriverWait(self.driver, self.time_out).until(
            EC.presence_of_element_located((locator_type, locator))
        )
        self.log.info('The web element is present now')

        return element

    def wait_until_elements_present(self, locator_type, locator):
        # wait 10 seconds before looking for element
        WebDriverWait(self.driver, self.time_out).until(
            EC.presence_of_element_located((locator_type, locator))
        )
        self.log.info('The web elements are present now')

        return self.driver.find_elements(locator_type, locator)
