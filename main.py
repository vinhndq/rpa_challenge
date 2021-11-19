# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from biz.agency_summary_bot import AgencySummaryBot
from page import dashboard_summary, it_dashboard
from biz.it_dashboard_bot import ItDashBoardBot
from RPA.Browser.Selenium import Selenium
from biz.investment_summary_bot import InvestSummaryBot
import os
import sys
from RPA.Excel.Files import Files

browser = Selenium()


def write_agencies(lib, agencies):
    lib.create_worksheet("agencies")
    for item in agencies:
        lib.append_rows_to_worksheet({0: item.agency, 1: item.price})


def download_file(urls):
    file_contents = {}
    for file, url in urls.items():
        browser.go_to(url)
        invest_summary = InvestSummaryBot(browser, url, file)
        content = invest_summary.download()
        if content is not None:
            file_contents[file] = content
    return file_contents


def write_investment(lib, investment_data):
    lib.create_worksheet("investments")
    investments = investment_data['data']
    pdf_urls = investment_data['invest_url']
    first_row = True
    pdf_file_content = download_file(browser, pdf_urls)
    for item in investments:
        if first_row:
            item.append("Name of this Investment")
            item.append("Unique Investment Identifier (UII)")
            item.append("Compare Name of Invest vs Investment Title")
            item.append("Compare Investment Identifier vs UII")
        else:
            uii = item[0]
            if uii in pdf_file_content:
                file_content = pdf_file_content[item[0]]
                item.append(file_content[0])
                item.append(file_content[1])
                item.append("same" if item[2] == file_content[0] else "diff")
                item.append("same" if uii == file_content[1] else "diff")
        lib.append_rows_to_worksheet(dict(enumerate(item)))
        first_row = False


def main():
    browser.set_download_directory(os.path.dirname(sys.modules['__main__'].__file__) + os.sep + 'output' + os.sep)
    # browser.set_download_directory("output")
    lib = Files()
    lib.create_workbook("output/agencies.xlsx")
    #
    # workbook = xlsxwriter.Workbook('output/result.xlsx')
    # worksheet = workbook.add_worksheet("agencies")
    it_dashboard_bot = ItDashBoardBot(browser, "https://itdashboard.gov/")
    it_dashboard_bot.open_the_website()
    agencies = it_dashboard_bot.get_data()
    write_agencies(lib, agencies)
    it_dashboard_bot.go_to_detail()
    browser.go_to(agencies[0].url)
    dashboard_summary_bot = AgencySummaryBot(browser, agencies[0].url)
    investment_data = dashboard_summary_bot.get_table_data()
    write_investment(lib, investment_data)
    lib.save_workbook()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
