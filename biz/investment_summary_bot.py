import time
from biz.bot_adapter import BotAdapter
from caching.system_caching import SystemCaching
import os
import sys
import shutil
import PyPDF2
import glob


class InvestSummaryBot(BotAdapter) :
    def __init__(self, browser, url, item) :
        super().__init__(browser, url)
        self.item = item
        self.browser.set_download_directory(os.path.dirname(sys.modules['__main__'].__file__) + os.sep + 'output')

    def open_the_website(self):
        self.browser.open_available_browser(self.url)

    def download(self) :
        # item_existed = False
        self.browser.set_download_directory(os.path.dirname(sys.modules['__main__'].__file__) + os.sep + 'output')
        self.wait_for_element_by_location("id: business-case-pdf")
        self.browser.click_element("id: business-case-pdf")
        # while not item_existed :
        #     time.sleep(2)
        #     item_existed = self.check_if_element_exist_by_location(self.browser, "id: business-case-pdf")
        #     if item_existed :
        #         self.browser.click_element("id: business-case-pdf")\
        file_name = self.item + '.pdf'
        target_path = os.path.dirname(sys.modules['__main__'].__file__) + os.sep + 'output' + os.sep + file_name
        # self.wait_for_file_download(target_path)
        time.sleep(10)
        try :
            print(glob.glob(os.path.dirname(sys.modules['__main__'].__file__) + os.sep + 'output' + os.sep+"*.pdf"))
            return self.get_pdf_content(target_path)
        except Exception :
            print("file not found %s " %target_path)
            return None

    def get_pdf_content(self, file_path) :
        pdfFileObj = open(file_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0)
        file_content = pageObj.extractText()
        name_of_invest = (file_content.split("1. Name of this Investment:")[1]).split("2. Unique Investment Identifier (UII):")[0].strip()
        uii = (file_content.split("2. Unique Investment Identifier (UII):")[1]).split("Section B: Investment Detail")[0].strip()
        return [name_of_invest, uii]