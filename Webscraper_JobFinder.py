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
        self.seleniumDriver = uc.Chrome()

        """
        self.seleniumDriver = webdriver.Chrome()
        """

        self.automate = False

    def LoginToJobs(self):

        """
        self.seleniumDriver.get(
            "https://secure.indeed.com/auth?hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed.com%2F&tmpl=desktop&service=my&from=gnav-util-homepage&jsContinue=https%3A%2F%2Fwww.indeed.com%2F&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess&_ga=2.216882070.1436526071.1662068128-19035690.1662068128")

        time.sleep(7)
        self.seleniumDriver.find_element(By.CSS_SELECTOR, "[name='__email']").send_keys("")
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
        self.seleniumDriver.find_element(By.CSS_SELECTOR, "[name='__password']").send_keys("")
        button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[type='submit']")
        self.seleniumDriver.execute_script("arguments[0].click();", button)

        time.sleep(5)

        """



        self.seleniumDriver.get("https://www.linkedin.com/login")

        time.sleep(2)

        self.seleniumDriver.find_element(By.ID, "username").send_keys("")
        time.sleep(5)
        self.seleniumDriver.find_element(By.ID, "password").send_keys("")
        time.sleep(5)
        button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[aria-label='Sign in']")
        self.seleniumDriver.execute_script("arguments[0].click();", button)

        time.sleep(2)



    def GetJobLinks(self):

        """
        indeedJobs = Webscraper_Indeed.IndeedJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                  self.salary, self.location, self.education,
                                                  self.experience, 'IndeedJobs', None, self.seleniumDriver)
        indeedJobs.indeedJobsLinkMaker()
        indeedJobs.findLinks()
        """


        fields = ['("Quality" OR "DevOps" OR "Python" OR "Java" OR "Automation" OR "site reliability") AND NOT ("Senior" OR "Mid" OR "Mid-level" OR "II" OR "III" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")',
                  '"Analyst" NOT ("Quality" OR "DevOps" OR "Python" OR "Java" OR "Automation" OR "site reliability" OR "Senior" OR "Mid" OR "Mid-level" OR "II" OR "III" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")',
                  '"software" NOT ("Quality" OR "DevOps" OR "Python" OR "Java" OR "Automation" OR "site reliability" OR "Senior" OR "Mid" OR "Mid-level" OR "II" OR "III" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")',
                  '"data" NOT ("Quality" OR "DevOps" OR "Python" OR "Java" OR "Automation" OR "site reliability" OR "Senior" OR "Mid" OR "Mid-level" OR "II" OR "III" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")',
                  '"Developer" NOT ("python" OR "java" OR "software" OR "data"  OR "Automation" OR "Analyst" OR "Quality" OR "DevOps" OR  "site reliability" OR "JavaScript" OR "Swift" OR "C++" OR "C" OR "PHP" OR "Angular" OR "Senior" OR "Mid" OR "Mid-level" OR ".Net" OR "II" OR "III" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")',
                  '"Engineer" NOT ("python" OR "java" OR "software" OR "data"  OR "Automation" OR "Analyst" OR "Quality" OR "DevOps" OR  "site reliability" OR "JavaScript" OR "Swift" OR "C++" OR "C" OR "PHP" OR "Angular" OR "Senior" OR "Mid" OR "Mid-level" OR ".Net" OR "II" OR "III" OR "electrical" OR "civil" OR "mechanical" OR "chemical" OR "aerospace" OR "biomedical" OR "petroleum" OR "agricultural" OR "Environmental" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")'
                  ]


        for field in fields:
            LinkedinJobs = Webscraper_Linkedin.LinkedinJobs("", field, "", "",
                                                            0, "Jacksonville, Florida", "",
                                                            "entry", 'LinkedinJobs', None, self.seleniumDriver)
            LinkedinJobs.LinkedinLinkMaker()
            LinkedinJobs.findLinks()
            


        fieldsFlorida = ['("Quality" OR "DevOps" OR "Python" OR "Java" OR "Automation" OR "site reliability") AND NOT ("Senior" OR "Mid" OR "Mid-level" OR "II" OR "III" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")',
                  '"Analyst" NOT ("Quality" OR "DevOps" OR "Python" OR "Java" OR "Automation" OR "site reliability" OR "Senior" OR "Mid" OR "Mid-level" OR "II" OR "III" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")',
                  '"software" NOT ("Quality" OR "DevOps" OR "Python" OR "Java" OR "Automation" OR "site reliability" OR "Senior" OR "Mid" OR "Mid-level" OR "II" OR "III" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")',
                  '"data" NOT ("Quality" OR "DevOps" OR "Python" OR "Java" OR "Automation" OR "site reliability" OR "Senior" OR "Mid" OR "Mid-level" OR "II" OR "III" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")',
                  '"Developer" NOT ("python" OR "java" OR "software" OR "data"  OR "Automation" OR "Analyst" OR "Quality" OR "DevOps" OR  "site reliability" OR "JavaScript" OR "Swift" OR "C++" OR "C" OR "PHP" OR "Angular" OR "Senior" OR "Mid" OR "Mid-level" OR ".Net" OR "II" OR "III" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")',
                  '"Engineer" NOT ("python" OR "java" OR "software" OR "data"  OR "Automation" OR "Analyst" OR "Quality" OR "DevOps" OR  "site reliability" OR "JavaScript" OR "Swift" OR "C++" OR "C" OR "PHP" OR "Angular" OR "Senior" OR "Mid" OR "Mid-level" OR ".Net" OR "II" OR "III" OR "electrical" OR "civil" OR "mechanical" OR "chemical" OR "aerospace" OR "biomedical" OR "petroleum" OR "agricultural" OR "Environmental" OR "IV" OR "V" OR "Sr" OR "Sr." OR "2" OR "3" OR "4" OR "5")'
                  ]


        for field in fieldsFlorida:
            LinkedinJobs = Webscraper_Linkedin.LinkedinJobs("", field, "in person", "",
                                                            0, "Florida", "",
                                                            "entry", 'LinkedinJobs', None, self.seleniumDriver)
            LinkedinJobs.LinkedinLinkMaker()
            LinkedinJobs.findLinks()



    def RefineJobLinks(self):

        getJobText = Webscraper_GetJobText.JobTextGrabber(self.seleniumDriver)

        getJobText.getLinkedinJobText("LinkedinJobs")

        refinedList = pd.read_csv('RefinedLinkedInJobCSV.csv')
        refinedList.dropna(axis=0, how='all', inplace=True)
        refinedList.to_csv('RefinedLinkedInJobCSV.csv', index=False)
        """

        getJobText.getIndeedJobText("IndeedJobs")
        """



    def EndProgram(self):
        self.seleniumDriver.quit()
