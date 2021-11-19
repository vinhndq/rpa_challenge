import os
import time
from datetime import timedelta


from caching.system_caching import SystemCaching


class AbstractBot:

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.time_out = SystemCaching.getConfig("Timeout", "max.wait.time")
        self.browser.set_selenium_timeout(timedelta(seconds=20))

    def check_if_element_exist_by_tag(self, parent_element, tag):
        try:
            element = parent_element.find_element_by_tag_name(tag)
        except Exception:
            return False
        return True

    def check_if_elements_exist_by_tag(self, parent_element, tag):
        try:
            element = parent_element.find_elements_by_tag_name(tag)
            if not element:
                return False
        except Exception:
            return False
        return True

    def check_if_element_exist_by_location(self, browser, locator):
        try:
            element = browser.find_element(locator)
        except Exception:
            return False
        return True

    def check_if_elements_exist_by_location(self, browser, locator):
        try:
            element = browser.find_elements(locator)
            if not element:
                return False
        except Exception:
            return False
        return True

    def wait_for_file_download(self, path):
        counter = 0
        file_exist = False
        while not file_exist:
            file_exist = os.path.isfile(path)
            counter += 1

    def wait_for_loading(self, locator):
        old_info = self.browser.find_element(
            locator).text
        new_info = self.browser.find_element(
            locator).text
        while new_info == old_info:
            new_info = self.browser.find_element(
                locator).text
