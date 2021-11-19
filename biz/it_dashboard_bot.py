import time
from page.it_dashboard import ItDashboard
from biz.bot_adapter import BotAdapter


class ItDashBoardBot(BotAdapter):

    def __init__(self, browser, url):
        super().__init__(browser, url)

    def open_the_website(self):
        self.browser.open_available_browser(self.url)

    def get_data(self) :
        self.browser.click_element('xpath://*[@id="node-23"]/div/div/div/div/div/div/div/a')
        time.sleep(2)
        return self.get_list_Xlsx_Item()

    def get_list_Xlsx_Item(self) :
        parent = self.browser.find_element('id:agency-tiles-widget')
        elements = parent.find_elements_by_class_name("noUnderline")
        it_dashboard_items = []
        for item in elements :
            agency = item.find_element_by_class_name("w200")
            price = item.find_element_by_class_name("w900")
            view_btn = item.find_element_by_class_name("btn-sm").get_attribute('href')
            it_dashboard_items.append(ItDashboard(agency.text, price.text, view_btn))
        return it_dashboard_items
    
    def go_to_detail(self) :
        self.browser.click_link('xpath: //*[@id="agency-tiles-widget"]/div/div[1]/div[1]/div/div/div/div[2]/a')

    def search_for(self, term: str):
        input_field = "id:login-id"
        self.browser.input_text(input_field, term)
        self.browser.click_button("class:login-btn")

