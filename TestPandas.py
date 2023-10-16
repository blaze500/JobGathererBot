import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import Webscraper_Linkedin
import Webscraper_Indeed
import Webscraper_GetJobText
import pandas as pd
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
refinedList = pd.read_csv('RefinedLinkedInJobCSV.csv')
refinedList.dropna(axis=0, how='all', inplace=True)
refinedList.to_csv('RefinedLinkedInJobCSV.csv', index=False)
