import time
from selenium.webdriver.common.by import By
import csv
import html2text
import re

class JobTextGrabber:

    #Starts the Program
    def __init__(self, seleniumDriver):
        self.seleniumDriver = seleniumDriver

    def getLinkedinJobText(self, csvName):
        self.writeToCSV("RefinedLinkedInJobCSV", "Link, Title, Company, (Physical) Location, Remote/In Person (Blank), How Long Has This Been Posted Since Gathering, Number Of Applicants, Salary")
        reader = csv.reader(open(csvName + '.csv', 'rt'), delimiter=',')
        for row in reader:
            goToNext = False

            self.seleniumDriver.get(row[0])
            time.sleep(3)

            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.ID, "job-details")
                jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                jobDescriptionTitleHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "jobs-unified-top-card__job-title")
                jobDescriptionTitle = html2text.html2text(jobDescriptionTitleHTML.get_attribute("innerHTML"))
                if self.ContainsSpecialWords(jobDescriptionText, jobDescriptionTitle):
                    print("We Have Found A Job That Fits The Description:" + str(row[0]))
                    self.writeToCSV("RefinedLinkedInJobCSV", str(row[0]) + "," + self.grabLinkedInJobInfo())
                    print("The data for this description is done being gathered \n")
            except:
                goToNext = True

            if goToNext is True:
                try:
                    jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
                    jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                    jobDescriptionTitleHTML = self.seleniumDriver.find_element(By.CLASS_NAME,
                                                                               "jobs-unified-top-card__job-title")
                    jobDescriptionTitle = html2text.html2text(jobDescriptionTitleHTML.get_attribute("innerHTML"))
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

    def ContainsSpecialWords(self, jobText, title):
        cleanedJobText= re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", jobText.lower())
        mustHaveWordsFile = open('mustHaveWords.txt', 'r', encoding="utf-8")
        mustHaveWords = mustHaveWordsFile.read().splitlines()
        atLeastOneOfWordsFile = open('atLeastOneOfWords.txt', 'r', encoding="utf-8")
        atLeastOneOfWords = atLeastOneOfWordsFile.read().splitlines()

        if all(word in cleanedJobText for word in mustHaveWords):
            if any(re.search(r'\b' + word + r'\b', cleanedJobText) for word in atLeastOneOfWords) or any(re.search(r'\b' + word + r'\b', title.lower()) for word in atLeastOneOfWords):
                return True
        return False

    def grabLinkedInJobInfo(self):
        possibleElements=["jobs-unified-top-card__job-title", "jobs-unified-top-card__company-name", "jobs-unified-top-card__bullet", "jobs-unified-top-card__workplace-type", "jobs-unified-top-card__posted-date", "jobs-unified-top-card__applicant-count"]
        infoString=""
        for element in possibleElements:
            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, element)
                text=html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML")).replace("\n", "")
                uselessInfoRemovedText= re.sub("\(.*?\)","()",text)
                specailCharactersGoneText = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", uselessInfoRemovedText)
                infoString += re.sub("\s\s+" , " ", specailCharactersGoneText) + ","
            except:
                infoString += " ,"
                print("There has been an error or the following element doesn't exist:" + str(element))
        try:
            salary=self.seleniumDriver.find_element(By.PARTIAL_LINK_TEXT, "/yr (from job description)")
            infoString+=html2text.html2text(salary.get_attribute("innerHTML")).replace("/yr", "").replace(",", "")

        except:
            print("There has been an error or the salary of the job doesn't exist")
            infoString += "No Info Found On Page"
        return str(infoString)