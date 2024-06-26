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
import SendEmailToMyself

class JobFinder:

    #Starts the Program
    def __init__(self):

        options = uc.ChromeOptions()
        try:
            self.seleniumDriver = uc.Chrome()
        except:
            self.seleniumDriver = webdriver.Chrome()
        self.automate = False

    def LoginToJobs(self):
        linkedInLoginFile = open('LinkedInLogin.txt', 'r', encoding="utf-8")
        linkedInLoginInfo = linkedInLoginFile.read().splitlines()

        self.seleniumDriver.get("https://www.linkedin.com/login")

        time.sleep(5)

        self.seleniumDriver.find_element(By.ID, "username").send_keys(linkedInLoginInfo[0])
        time.sleep(5)
        self.seleniumDriver.find_element(By.ID, "password").send_keys(linkedInLoginInfo[1])
        time.sleep(5)
        button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[aria-label='Sign in']")
        self.seleniumDriver.execute_script("arguments[0].click();", button)

        time.sleep(5)



    def GetJobLinks(self):

        """
        indeedJobs = Webscraper_Indeed.IndeedJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                  self.salary, self.location, self.education,
                                                  self.experience, 'IndeedJobs', None, self.seleniumDriver)
        indeedJobs.indeedJobsLinkMaker()
        indeedJobs.findLinks()
        """

        fields = open('LinkedInFieldSearch.txt', 'r', encoding="utf-8").read().splitlines()
        fieldAttributes=open('LinkedInFieldsMinusLocation.txt', 'r', encoding="utf-8").read().splitlines()
        locations=open('LinkedInLocationOfJobs.txt', 'r', encoding="utf-8").read().splitlines()
        for location in locations:
            for field in fields:
                LinkedinJobs = Webscraper_Linkedin.LinkedinJobs(fieldAttributes[0], field, fieldAttributes[1], fieldAttributes[2],
                                                                int(fieldAttributes[3]), location, fieldAttributes[4],
                                                                fieldAttributes[5], 'LinkedinJobs', None, self.seleniumDriver)
                LinkedinJobs.LinkedinLinkMaker()
                LinkedinJobs.findLinks()


    def RefineJobLinks(self):

        getJobText = Webscraper_GetJobText.JobTextGrabber(self.seleniumDriver)

        getJobText.getLinkedinJobTextAlgorithm("LinkedinJobs")

        refinedList = pd.read_csv('RefinedLinkedInJobCSV.csv')
        refinedList.dropna(axis=0, how='all', inplace=True)
        refinedList.to_csv('RefinedLinkedInJobCSV.csv', index=False)
        """

        getJobText.getIndeedJobText("IndeedJobs")
        """



    def EndProgram(self):
        self.seleniumDriver.quit()
