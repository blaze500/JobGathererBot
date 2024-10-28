import time
from selenium.webdriver.common.by import By
import csv
import html2text
import re
import os
import datetime
import undetected_chromedriver as uc

class JobTextGrabber:

    #Starts the Program
    def __init__(self, seleniumDriver):
        self.seleniumDriver = seleniumDriver

    def getIndeedJobText(self, csvName):
        self.writeToCSV("RefinedIndeedJobCSV", "Link, Title, Company, (Physical) Location, Remote/In Person (Blank), How Long Has This Been Posted Since Gathering, Number Of Applicants, Salary")
        reader = csv.reader(open(csvName + '.csv', 'rt'), delimiter=',')
        for row in reader:
            self.seleniumDriver.get(row[0])
            time.sleep(5)

            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "jobsearch-JobComponent-embeddedHeader")
                jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                print(jobDescriptionText)
                #self.writeToCSV("RefinedIndeedJobCSV", str(row[0]) + "," + self.grabIndeedJobInfo())
            except:
                print("This link caused a problem in the getIndeedJobText method: " + row[0])

    def getLinkedinJobTextAlgorithm(self, csvName):
        self.writeToCSV("RefinedLinkedInJobCSV", "Link, Title, Company, (Physical) Location, Remote/In Person (Blank), How Long Has This Been Posted Since Gathering, Number Of Applicants, Salary")
        reader = csv.reader(open(csvName + '.csv', 'rt'), delimiter=',')
        for row in reader:
            goToNext = False
            try:
                self.seleniumDriver.get(row[0])
                time.sleep(5)
                self.getLinkedinJobText(row)
            except:
                print("Could not get the link.\nGrabbing next link in list.")

    def getLinkedinJobText(self, row):

        # Checks to see any info is on the page. Sometimes they switch things up, so if this one fails, it will go to the next case
        try:
            jobDescriptionTextHTML = self.seleniumDriver.find_element(By.ID, "job-details")
            jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
            jobDescriptionTitle = self.seleniumDriver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title").text

            #Check to see if it has any of the words found in the atLeastOneOfWords file
            if self.ContainsSpecialWords(jobDescriptionText, jobDescriptionTitle):
                print("Passed 3")
                print("We Have Found A Job That Fits The Description:")
                print("Title: " + jobDescriptionTitle)
                print("Link: " + str(row[0]))
                self.writeToCSV("RefinedLinkedInJobCSV", str(row[0]) + "," + self.grabLinkedInJobInfo())
                print("The data for this description is done being gathered \n\n\n")
        except:
            goToNext = True

        #Secondary check in case first one fails but there is potential information
        if goToNext is True:
            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
                jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                jobDescriptionTitle = self.seleniumDriver.find_element(By.CLASS_NAME,
                                                                       "job-details-jobs-unified-top-card__job-title").text
                if self.ContainsSpecialWords(jobDescriptionText, jobDescriptionTitle):
                    print("We Have Found A Job That Fits The Description:" + str(row[0]))
                    self.writeToCSV("RefinedLinkedInJobCSV", str(row[0]) + "," + self.grabLinkedInJobInfo())
                    print("The data for this description is done being gathered \n")
            except:
                print("This link caused a problem in the getLinkedinJobText method: " + row[0])


    def writeToCSV(self, name, finalURL):
        csv = open(name + '.csv', 'a', encoding="utf-8")
        csv.write(finalURL + "\n")
        csv.close()

    #Checks to see if any words in the file are on the posting
    def ContainsSpecialWords(self, jobText, title):
        cleanedJobText= re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", jobText.lower())
        atLeastOneOfWordsFile = open('atLeastOneOfWords.txt', 'r', encoding="utf-8")
        atLeastOneOfWords = atLeastOneOfWordsFile.read().splitlines()

        if (("master's" not in cleanedJobText) and ("masters" not in cleanedJobText)) or ("bachelor" in cleanedJobText):
            if any(re.search(r'\b' + word + r'\b', cleanedJobText) for word in atLeastOneOfWords) or any(re.search(r'\b' + word + r'\b', title.lower()) for word in atLeastOneOfWords):
                return True
        return False

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
            infoString += splitText[0] + "," + splitText2[1] + "," + splitText[1] + "," + splitText[2] + ","
            splitText2[0] = re.sub("/yr,", "", splitText2[0]).replace(" ", "")
            infoString += re.sub("\++,", "", splitText2[0])
        elif ("Hybrid" or "Remote" or "On-site") in splitText2[0]:
            infoString += splitText[0] + "," + splitText2[0] + "," + splitText[1] + "," + splitText[2] + "," + "No Salary Found"
        else:
            infoString += splitText[0] + "," + "Could Not Find" + "," + splitText[1] + "," + splitText[2] + "," + "No Salary Found"

        print(infoString)

        return str(infoString)