import time
from selenium.webdriver.common.by import By
import csv
import html2text
import re
import os

class JobTextGrabberTest:

    #Starts the Program
    def __init__(self, seleniumDriver):
        self.seleniumDriver = seleniumDriver

    def getIndeedJobText(self, csvName):
        self.writeToCSV("RefinedIndeedJobCSV", "Link, Title, Company, (Physical) Location, Remote/In Person (Blank), How Long Has This Been Posted Since Gathering, Number Of Applicants, Salary")
        reader = csv.reader(open(csvName + '.csv', 'rt'), delimiter=',')
        for row in reader:
            self.seleniumDriver.get(row[0])
            time.sleep(3)

            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "jobsearch-JobComponent-embeddedHeader")
                jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                print(jobDescriptionText)
                #self.writeToCSV("RefinedIndeedJobCSV", str(row[0]) + "," + self.grabIndeedJobInfo())
            except:
                print("This link caused a problem in the getIndeedJobText method: " + row[0])

    def getLinkedinJobText(self, links):
        for link in links:
            self.seleniumDriver.get(link)
            time.sleep(3)

            self.grabLinkedInJobInfo()




    def grabLinkedInJobInfo(self):
        jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "jobs-unified-top-card__primary-description")
        text=html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML")).replace("\n", "").replace("*", "")
        print(text +"\n")
        splitText=text.split(" · ")
        splitText[0] = re.sub("\[|\]|\(http.+\)", "", splitText[0])
        print(splitText[0])
        splitText[1] = re.split("\(|\)", splitText[1])
        print(splitText[1])
        splitText[2] = splitText[2].replace("*", "")
        print(splitText[2])
        print("\n\n\n")
