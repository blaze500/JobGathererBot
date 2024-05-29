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
        try:
            jobDescriptionTextHTML = self.seleniumDriver.find_element(By.ID, "job-details")
            jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
            jobDescriptionTitleHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title")
            jobDescriptionTitle = html2text.html2text(jobDescriptionTitleHTML.get_attribute("innerHTML"))

            if self.ContainsSpecialWords(jobDescriptionText, jobDescriptionTitle):
                print("Passed 3")
                print("We Have Found A Job That Fits The Description:")
                print("Title: " + jobDescriptionTitle)
                print("Link: " + str(row[0]))
                self.writeToCSV("RefinedLinkedInJobCSV", str(row[0]) + "," + self.grabLinkedInJobInfo())
                print("The data for this description is done being gathered \n\n\n")
        except:
            goToNext = True

        if goToNext is True:
            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
                jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                jobDescriptionTitleHTML = self.seleniumDriver.find_element(By.CLASS_NAME,
                                                                           "job-details-jobs-unified-top-card__job-title")
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

        if (("master's" not in cleanedJobText) and ("masters" not in cleanedJobText)) or ("bachelor" in cleanedJobText):
            if any(re.search(r'\b' + word + r'\b', cleanedJobText) for word in atLeastOneOfWords) or any(re.search(r'\b' + word + r'\b', title.lower()) for word in atLeastOneOfWords):
                return True
        return False


    def grabLinkedInJobInfo(self):
        infoString=""
        jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title")
        title=html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML")).replace("\n", "").replace("#", "")
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


        if ("second" in infoString[2]) or ("minute" in infoString[2]) or ("hour" in infoString[2]):
            infoString[2] = str(datetime.date.today().strftime("%m/%d/%Y"))
            print(infoString[2])
        elif "day" in infoString[2]:
            infoString[2] = str(
                (datetime.date.today() - datetime.timedelta(days=int(re.findall(r'\d+', infoString[2])[0]))).strftime(
                    "%m/%d/%Y"))
            print(infoString[2])
        elif "week" in infoString[2]:
            infoString[2] = str((datetime.date.today() - datetime.timedelta(
                days=7 * int(re.findall(r'\d+', infoString[2])[0]))).strftime("%m/%d/%Y"))
            print(infoString[2])
        elif "month" in infoString[2]:
            infoString[2] = str((datetime.date.today() - datetime.timedelta(
                days=31 * int(re.findall(r'\d+', infoString[2])[0]))).strftime("%m/%d/%Y"))
            print(infoString[2])

        print("Passed 6")
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


"""
    def grabLinkedInJobInfo(self):
        possibleElements=["jobs-unified-top-card__job-title", "jobs-unified-top-card__company-name", "jobs-unified-top-card__bullet", "jobs-unified-top-card__workplace-type", "jobs-unified-top-card__posted-date"]
        infoString=""
        over200=False
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
            jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "jobs-unified-top-card__applicant-count")
            text = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML")).replace("\n", "")
            uselessInfoRemovedText = re.sub("\(.*?\)", "()", text)
            specailCharactersGoneText = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", uselessInfoRemovedText)
            infoString += re.sub("\s\s+", " ", specailCharactersGoneText) + ","
        except:
            over200 = True

        if over200:
            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_elements(By.CLASS_NAME, "jobs-unified-top-card__bullet")[-1]
                text = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML")).replace("\n", "")

                jobDescriptionTextHTML2 = self.seleniumDriver.find_element(By.CLASS_NAME, "jobs-unified-top-card__bullet")
                text2 = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML")).replace("\n", "")

                if text == text2:
                    uselessInfoRemovedText = re.sub("\(.*?\)", "()", text)
                    specailCharactersGoneText = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", uselessInfoRemovedText)
                    infoString += re.sub("\s\s+", " ", specailCharactersGoneText) + ","
                else:
                    infoString += " 0 applicants,"
            except:
                print("There has been an error")

        try:
            salary=self.seleniumDriver.find_element(By.PARTIAL_LINK_TEXT, "/yr (from job description)")
            infoString+=html2text.html2text(salary.get_attribute("innerHTML")).replace("/yr", "").replace(",", "")
        except:
            print("There has been an error or the salary of the job doesn't exist")
            infoString += "No Salary Found"
        return str(infoString)
"""