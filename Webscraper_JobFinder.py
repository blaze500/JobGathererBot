import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import LocationChecker
import Webscraper_Linkedin
import Webscraper_GetJobText
import easygui as gui
import sys

class JobFinder:

    #Starts the Program\
    def __init__(self, field, type, location, inPerson, fullTime, salary, experience, education):
        self.field = field
        self.type = type
        self.location = location
        self.inPerson = inPerson
        self.fullTime = fullTime
        self.salary = salary
        self.experience = experience
        self.education = education
        self.seleniumDriver = webdriver.Chrome("chromedriver.exe")
        self.automate = False

    def LoginToJobs(self):

            self.seleniumDriver.get("https://www.linkedin.com/login")
            gui.msgbox("Please Log In To Your Linkedin Account On The Selenium Browser. Once You Are Done Click OK On This Message Box. \nDo not exit the Browser!", title='Job Analytics Bot')


    def GetJobLinks(self):

        LinkedinJobs = Webscraper_Linkedin.LinkedinJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                        self.salary, self.location, self.education,
                                                        self.experience, 'LinkedinJobs', None, self.seleniumDriver)
        LinkedinJobs.LinkedinLinkMaker()
        LinkedinJobs.findLinks()


    def RefineJobLinks(self):
        getJobText = Webscraper_GetJobText.JobTextGrabber(self.seleniumDriver)
        getJobText.getLinkedinJobText("LinkedinJobs")


    def EndProgram(self):
        self.seleniumDriver.quit()
