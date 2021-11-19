import time

from selenium.common.exceptions import TimeoutException

from abstract_bot import AbstractBot
from datetime import timedelta


class AgencySummaryBot(AbstractBot):

    def __init__(self, browser, url):
        super().__init__(browser, url)


    def open_the_website(self):
        self.browser.open_available_browser(self.url)

    def get_table_data(self):
        summary = []
        invest_url_dic = {}
        summary.append(self.get_header())
        has_next = True
        current_page = 0
        # while has_next:
        self.browser.click_element('name: investments-table-object_length')
        self.browser.click_element('''//*[@name="investments-table-object_length"]
                                                     /option[4]''')
        self.wait_for_loading("id:investments-table-object_info")
        self.set_table_content_data(current_page, summary, invest_url_dic)
        return {'data': summary, 'invest_url': invest_url_dic}

    def set_table_content_data(self, current_page, summary, invest_url_dic):

        self.browser.wait_until_element_is_visible('class:datasource-table')
        self.browser.wait_until_element_is_visible('id:investments-table-object')
        table = self.browser.find_element('id:investments-table-object')
        tbody = table.find_element_by_tag_name('tbody')
        trs = tbody.find_elements_by_tag_name('tr')
        for tr in trs:
            data = []
            for index, td in enumerate(tr.find_elements_by_tag_name('td')):
                td_text = td.text
                data.append(td_text)
                if index == 0 and self.check_if_element_exist_by_tag(td, 'a'):
                    invest_url_dic[td_text] = td.find_element_by_tag_name('a').get_attribute('href')
            summary.append(data)

    def get_header(self):
        data = []
        try:
            self.browser.wait_until_element_is_visible('class:datasource-table')
            tables = self.browser.find_elements('class:datasource-table')
            data_table = tables[0]
            header_element = data_table.find_elements_by_tag_name('th')
            for e in header_element:
                data.append(e.text)
        except TimeoutException:
            print("element takes too much time to load")
        return data
