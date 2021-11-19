import time
import os
from typing import Counter
from caching.system_caching import SystemCaching


class BotAdapter :

    def __init__(self, browser, url) :
        self.browser = browser
        self.url = url
        self.time_out = SystemCaching.getConfig("Timeout", "max.wait.time")

    def check_if_element_exist_by_tag(self, parent_element, tag) :
        try :
            element = parent_element.find_element_by_tag_name(tag)
        except Exception :
            print("Element not exist")
            return False
        return True

    def check_if_elements_exist_by_tag(self, parent_element, tag) :
        try :
            element = parent_element.find_elements_by_tag_name(tag)
            if not element :
                return False
        except Exception :
            print("Element not exist")
            return False
        return True

    def check_if_element_exist_by_location(self, browser, locator) :
        try :
            element = browser.find_element(locator)
        except Exception :
            print("Element not exist")
            return False
        return True

    def check_if_elements_exist_by_location(self, browser, locator) :
        try :
            element = browser.find_elements(locator)
            if not element :
                return False
        except Exception :
            print("Element not exist")
            return False
        return True

    def wait_for_element_by_location(self, locator) :
        counter =  0
        print("wait for %s ..." % locator)
        item_existed = False
        while not item_existed :
            time.sleep(1)
            item_existed = self.check_if_element_exist_by_location(self.browser, locator)
            counter += 1
            if counter == self.time_out :
                raise TimeoutError("max wait time reach")

    def wait_for_elements_by_location(self, locator) :
        counter = 0
        print("wait for %s ..." % locator)
        item_existed = False
        counter = 0
        while not item_existed :
            time.sleep(1)
            item_existed = self.check_if_elements_exist_by_location(self.browser, locator)
            counter += 1
            if counter == self.time_out :
                raise TimeoutError("max wait time reach")

    def wait_for_element_by_tag(self, parent_element, tag) :
        counter = 0
        print("wait for %s ..." % tag)
        item_existed = False
        while not item_existed :
            time.sleep(1)
            item_existed = self.check_if_element_exist_by_tag(parent_element, tag)

    def wait_for_elements_by_tag(self, parent_element, tag) :
        counter = 0
        print("wait for %s ..." % tag)
        item_existed = False
        while not item_existed :
            time.sleep(1)
            item_existed = self.check_if_elements_exist_by_tag(parent_element, tag)
            counter += 1
            if counter == self.time_out :
                raise TimeoutError("max wait time reach")

    def wait_for_file_download(self, dir) :
        counter = 0
        file_exist = False
        while not file_exist :
            time.sleep(1)
            file_exist = os.path.isfile(dir)
            counter += 1
            if counter == self.time_out :
                raise TimeoutError("max wait time reach")