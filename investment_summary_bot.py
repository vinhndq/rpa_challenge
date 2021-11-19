import glob
import os

import PyPDF2

from abstract_bot import AbstractBot


class InvestSummaryBot(AbstractBot):
    def __init__(self, browser, url, item):
        super().__init__(browser, url)
        self.item = item
        self.browser.set_download_directory(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'output')

    def open_the_website(self):
        self.browser.open_available_browser(self.url)

    def download(self):
        # item_existed = False
        self.browser.wait_until_element_is_visible("id: business-case-pdf")
        self.browser.click_element("id: business-case-pdf")
        # while not item_existed :
        #     time.sleep(2)
        #     item_existed = self.check_if_element_exist_by_location(self.browser, "id: business-case-pdf")
        #     if item_existed :
        #         self.browser.click_element("id: business-case-pdf")\
        file_name = self.item + '.pdf'
        target_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'output' + os.sep + file_name
        self.wait_for_file_download(target_path)
        # time.sleep(10)
        try:
            print(glob.glob(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'output' + "*.pdf"))
            return self.get_pdf_content(target_path)
        except Exception:
            print("file not found %s " % target_path)
            return None

    def get_pdf_content(self, file_path):
        pdf_file_obj = open(file_path, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
        page_obj = pdf_reader.getPage(0)
        file_content = page_obj.extractText()
        name_of_invest = \
            (file_content.split("1. Name of this Investment:")[1]).split("2. Unique Investment Identifier (UII):")[
                0].strip()
        uii = (file_content.split("2. Unique Investment Identifier (UII):")[1]).split("Section B: Investment Detail")[
            0].strip()
        return [name_of_invest, uii]
