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
        infoString=""
        jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title")
        title=html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML")).replace("\n", "")
        print("Passed 4")
        infoString= title.replace(",", "") + ","
        jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__primary-description-container")
        text=html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML")).replace("\n", "").replace("*", "")
        print("Passed 5")
        print(text)
        splitText=text.split("·")
        print(splitText)
        infoString += re.sub("\[|\]|\(http.+\)|,", "", splitText[0]) + "," + re.sub(",", "", splitText[1]) + ","

        SalaryAmdRemote = self.seleniumDriver.find_element(By.CLASS_NAME,
                                                                  "job-details-jobs-unified-top-card__job-insight")
        text2 = html2text.html2text(SalaryAmdRemote.get_attribute("innerHTML")).replace("\n", "").replace(",","")
        text2= re.sub(r"\s+-\s+", "-", text2)
        text2 = re.sub(r"\s+level", "-level", text2)
        print(text2)

        categories = text2.split()
        print(categories)
        location=categories[0]

        salary="No Salary Found"

        if "$" in categories[0]:
           salary=categories[0]
           location=categories[1]

        infoString += location + "," + splitText[2] + "," + splitText[3] + "," + salary
        print(infoString)

        """
        splitText1 = re.split("(?=\d)", re.sub(" +", " " ,splitText[2].replace(",", " ").replace("Reposted", '')), 1)

        print(splitText1)
        print(splitText1[0])
        print(splitText1[1])

        if ("second" in splitText1[1]) or ("minute" in splitText1[1]) or ("hour" in splitText1[1]):
            splitText1[1] = str(datetime.date.today().strftime("%m/%d/%Y"))
            print(splitText1[1])
        elif "day" in splitText1[1]:
            splitText1[1] = str((datetime.date.today() - datetime.timedelta(days=int(re.findall(r'\d+', splitText1[1])[0]))).strftime("%m/%d/%Y"))
            print(splitText1[1])
        elif "week" in splitText1[1]:
            splitText1[1] = str((datetime.date.today() - datetime.timedelta(days=7 * int(re.findall(r'\d+', splitText1[1])[0]))).strftime("%m/%d/%Y"))
            print(splitText1[1])
        elif "month" in splitText1[1]:
            splitText1[1] = str((datetime.date.today() - datetime.timedelta(days=31 * int(re.findall(r'\d+', splitText1[1])[0]))).strftime("%m/%d/%Y"))
            print(splitText1[1])

        infoString += ",".join(splitText1) + ","


        infoString += splitText[2].replace("*", "").replace(",", "") + ","
        """
        return str(infoString)

