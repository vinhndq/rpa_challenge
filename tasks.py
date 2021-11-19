import os

from RPA.Excel.Files import Files

from agency_summary_bot import AgencySummaryBot
from caching.system_caching import SystemCaching
from investment_summary_bot import InvestSummaryBot
from it_dashboard_bot import ItDashBoardBot
from executor import Executor


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    browser_lib = SystemCaching.get_browser()
    browser_lib.set_download_directory(
        os.path.dirname(os.path.abspath(__file__)) + os.sep + 'output' + os.sep)
    executor = Executor(browser_lib)
    executor.main()
