from agency_summary_bot import AgencySummaryBot
from investment_summary_bot import InvestSummaryBot
from it_dashboard_bot import ItDashBoardBot
from RPA.Excel.Files import Files


class Executor:

    def __init__(self, browser_lib):
        self.browser_lib = browser_lib

    def open_the_website(self, url):
        self.browser_lib.open_available_browser(url)

    def search_for(self, term):
        input_field = "css:input"
        self.browser_lib.input_text(input_field, term)
        self.browser_lib.press_keys(input_field, "ENTER")

    def store_screenshot(self, filename):
        self.browser_lib.screenshot(filename=filename)

    def write_agencies(self, lib, agencies):
        lib.create_worksheet("agencies")
        for item in agencies:
            lib.append_rows_to_worksheet({0: item.agency, 1: item.price})

    def download_file(self, urls):
        file_contents = {}
        for file, url in urls.items():
            self.browser_lib.go_to(url)
            invest_summary = InvestSummaryBot(self.browser_lib, url, file)
            content = invest_summary.download()
            if content is not None:
                file_contents[file] = content
                # break

        return file_contents

    def write_investment(self, lib, investment_data):
        lib.create_worksheet("investments")
        investments = investment_data['data']
        pdf_urls = investment_data['invest_url']
        first_row = True
        pdf_file_content = self.download_file(pdf_urls)
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

    # Define a main() function that calls the other functions in order:
    def main(self):
        try:
            self.open_the_website("https://itdashboard.gov/")
            lib = Files()
            lib.create_workbook("output/agencies.xlsx")
            it_dashboard_bot = ItDashBoardBot(self.browser_lib, "https://itdashboard.gov/")
            it_dashboard_bot.open_the_website()
            agencies = it_dashboard_bot.get_data()
            self.write_agencies(lib, agencies)
            self.browser_lib.go_to(agencies[0].url)
            dashboard_summary_bot = AgencySummaryBot(self.browser_lib, agencies[0].url)
            investment_data = dashboard_summary_bot.get_table_data()
            self.write_investment(lib, investment_data)
            lib.save_workbook()
        finally:
            print("")
            # self.browser_lib.close_all_browsers()
