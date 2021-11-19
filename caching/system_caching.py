from configparser import ConfigParser
import os
from typing import NewType

from RPA.Browser.Selenium import Selenium
from datetime import timedelta


class SystemCaching:
    __configs = {}
    __browser = None

    @staticmethod
    def getConfig(section_key, key):
        if section_key not in SystemCaching.__configs:
            path = os.path.dirname(os.path.realpath(__file__))
            ini = '/'.join([path, "../config.ini"])
            config = ConfigParser()
            config.read(ini)
            SystemCaching.__configs = {section: dict(config.items(section)) for section in config.sections()}
        return SystemCaching.__configs[section_key][key]

    @staticmethod
    def get_browser():
        if SystemCaching.__browser is None:
            SystemCaching.__browser = Selenium()
        return SystemCaching.__browser
