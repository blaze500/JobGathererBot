import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import Webscraper_Linkedin
import Webscraper_Indeed
import TestGetJobText
import pandas as pd
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc


class JobFinder:

    #Starts the Program
    def __init__(self):
        options = uc.ChromeOptions()
        self.seleniumDriver = uc.Chrome()
        self.LoginToJobs()


    def LoginToJobs(self):
        """
        self.seleniumDriver.get(
            "https://secure.indeed.com/auth?hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed.com%2F&tmpl=desktop&service=my&from=gnav-util-homepage&jsContinue=https%3A%2F%2Fwww.indeed.com%2F&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess&_ga=2.216882070.1436526071.1662068128-19035690.1662068128")

        time.sleep(7)
        self.seleniumDriver.find_element(By.CSS_SELECTOR, "[name='__email']").send_keys("jobautomatorbottestacc@gmail.com")
        button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[type='submit']")
        self.seleniumDriver.execute_script("arguments[0].click();", button)
        time.sleep(5)

        try:
            button = self.seleniumDriver.find_element(By.ID, "auth-page-google-password-fallback")
            self.seleniumDriver.execute_script("arguments[0].click();", button)
        except:
            print("Was Unable To Click On The Put In Password Due To Captcha On Indeed")
            wait = input("Press Enter to continue.")

        time.sleep(5)
        self.seleniumDriver.find_element(By.CSS_SELECTOR, "[name='__password']").send_keys("fakepassword")
        button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[type='submit']")
        self.seleniumDriver.execute_script("arguments[0].click();", button)

        time.sleep(5)
        """



        self.seleniumDriver.get("https://www.linkedin.com/login")

        time.sleep(2)

        self.seleniumDriver.find_element(By.ID, "username").send_keys("jobautomatorbottestacc@gmail.com")
        time.sleep(5)
        self.seleniumDriver.find_element(By.ID, "password").send_keys("fakepassword")
        time.sleep(5)
        button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[aria-label='Sign in']")
        self.seleniumDriver.execute_script("arguments[0].click();", button)

        time.sleep(2)

        self.RefineJobLinks()



    def RefineJobLinks(self):

        getJobText = TestGetJobText.JobTextGrabberTest(self.seleniumDriver)

        links = []

        getJobText.getLinkedinJobText(links)
        #getJobText.getIndeedJobText("IndeedJobs")


JobFinder()