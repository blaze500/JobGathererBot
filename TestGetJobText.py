import time
from selenium.webdriver.common.by import By
import csv
import html2text
import re
import os
import datetime

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
        # The string that will be put into the CSV
        infoString = ""

        # The title of the job
        jobTitle = self.seleniumDriver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title").text.replace(",", "")
        print(jobTitle)

        # The company of the job
        jobCompanyName = self.seleniumDriver.find_element(By.CLASS_NAME,
                                                          "job-details-jobs-unified-top-card__company-name").text.replace(",", "")
        print(jobCompanyName)

        # The location, time the application has been open, and number of applicants
        jobInfo1 = self.seleniumDriver.find_element(By.CLASS_NAME,
                                                    "job-details-jobs-unified-top-card__primary-description-container").text.replace(
            ",", "")
        print(jobInfo1)

        # The (Salary), Remote or In person, Fulltime or Part Time, and Skills/missing skills of job. This is only important for the first 3 things, ignore the rest.
        jobInfo2 = self.seleniumDriver.find_element(By.CLASS_NAME, "job-details-preferences-and-skills").text.replace(
            ",", "")
        print(jobInfo2)

        splitText = jobInfo1.split(" · ")
        print(splitText)

        splitText2 = jobInfo2.split("\n")
        print(splitText2)

        # Converts the length of time the job has been to a numerical date
        if ("second" in splitText[1]) or ("minute" in splitText[1]) or ("hour" in splitText[1]):
            splitText[1] = str(datetime.date.today().strftime("%m/%d/%Y"))
            print(splitText[1])
        elif "day" in splitText[1]:
            splitText[1] = str(
                (datetime.date.today() - datetime.timedelta(days=int(re.findall(r'\d+', splitText[1])[0]))).strftime(
                    "%m/%d/%Y"))
            print(splitText[1])
        elif "week" in splitText[1]:
            splitText[1] = str((datetime.date.today() - datetime.timedelta(
                days=7 * int(re.findall(r'\d+', splitText[1])[0]))).strftime("%m/%d/%Y"))
            print(splitText[1])
        elif "month" in splitText[1]:
            splitText[1] = str((datetime.date.today() - datetime.timedelta(
                days=31 * int(re.findall(r'\d+', splitText[1])[0]))).strftime("%m/%d/%Y"))
            print(splitText[1])

        infoString += jobTitle + "," + jobCompanyName + ","

        # Putting all the info together. Checks to see if there is a salary or not before doing.
        if "/yr" in splitText2[0]:
            infoString += splitText[0] + "," + splitText2[1] + "," + splitText[1] + "," + splitText[2] + "," + \
                          splitText2[2] + ","
            splitText2[0] = re.sub("/yr,", "", splitText2[0]).replace(" ", "")
            infoString += re.sub("\++,", "", splitText2[0])
        else:
            infoString += splitText[0] + "," + splitText2[0] + "," + splitText[1] + "," + splitText[2] + "," + \
                          splitText2[1] + "," + "No Salary Found"



        print(infoString)
        return str(infoString)

