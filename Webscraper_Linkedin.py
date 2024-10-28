import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import os
import regex as re
import html2text
import math

class LinkedinJobs:

    def __init__(self, type, field, inPerson, fullTime, salary, location, education, experience, writeTo, numberOfJobsLimit, seleniumDriver):
        self.type = type
        self.field = field
        self.inPerson = inPerson
        self.fullTime = fullTime
        self.salary = salary
        self.location = location
        self.education = education
        self.experience = experience
        self.writeTo = writeTo
        self.numberOfJobsLimit = 1000000
        if numberOfJobsLimit is not None:
            self.numberOfJobsLimit = numberOfJobsLimit
        self.seleniumDriver = seleniumDriver










    # Makes the link based off of search filters in the search engine. This is done by figuring
    # out what filter (for example, salary, degree type, job type) is correlated to in the link
    # when you click on a filter. By doing this instead of say, clicking on each filter with a
    # selenium bot, it saves a lot of time and is more or less prone to the same errors a selenium
    # bot that clicks on the websites filters is (things moving, words changing, ect.).
    def LinkedinLinkMaker(self):

        self.LinkedinJobsLink = "https://www.linkedin.com/jobs/search/?"


        if self.experience == "entry" or self.experience == "mid" or self.experience == "senior" or self.experience == "":
            self.LinkedinJobsLink += "&f_E="
            if self.experience == "entry":
                self.LinkedinJobsLink += "2"
            elif self.experience == "mid" or "senior":
                self.LinkedinJobsLink +="4"

        if self.fullTime == "full time" or self.fullTime == "part time" or self.fullTime == "both" or self.type == "internship":
            #Because I need to check what gets added to this, I will add this to the end of the link at the end
            timeStartingCode = "&f_JT="
            if self.fullTime == "full time":
                timeStartingCode +="F"
            elif self.fullTime == "part time":
                timeStartingCode +="P"
            elif self.fullTime == "both":
                timeStartingCode +="F%2CP"
            if self.type == "internship":
                if len(timeStartingCode) > 5:
                    timeStartingCode += "%2C"
                timeStartingCode += "I"
            self.LinkedinJobsLink += timeStartingCode

        if self.inPerson == "in person":
            self.LinkedinJobsLink +="&f_WT=1%2C3"
        elif self.inPerson == "remote":
            self.LinkedinJobsLink += "&f_WT=2"
        elif self.inPerson == "both":
            self.LinkedinJobsLink += "&f_WT=1%2C2%2C3"


        # Made salary an int, as it was a string
        salary = int(self.salary)
        # There is a salary button starting at 40k and it goes up in increments of 20k
        if salary > 39999:
            # Checking to see how much money is left after 40k
            salaryAbove40k = salary-40000
            # This is to remove the extra numbers as it only goes in increments of 20k
            salaryModulus20k = salary % 20000
            # Does math to see if its 40k, 60k, ..., 200k, and puts the appropriate number in the slot (1 being 40k, 2 being 60k, ect)
            above40kInIncsOf20k = int((salaryAbove40k-salaryModulus20k)/20000)
            if above40kInIncsOf20k > 8:
                self.LinkedinJobsLink += "&f_SB2=9"
            else:
                self.LinkedinJobsLink += "&f_SB2=" + str(1+above40kInIncsOf20k)

        # Replaces spaces and commas with their character number and then hexadecimal equivalent, as web links cannot function with a space and/or comma in them.
        if len(self.location) > 0:
            self.LinkedinJobsLink +="&location=" + self.location.replace(" ", "%20").replace(",", "%2C") + "%2C%20United%20States"

        # Replaces spaces with its character number and then hexadecimal equivalent, as web links cannot function with a in them.
        if self.field != "":
            self.LinkedinJobsLink +="&keywords=" + self.field.replace(" ", "%20")

        if len(self.LinkedinJobsLink) > 40:
            self.LinkedinJobsLink = self.LinkedinJobsLink.replace("https://www.linkedin.com/jobs/search/?&", "https://www.linkedin.com/jobs/search/?")

        self.LinkedinJobsLink += "&sortBy=DD"

        print(self.LinkedinJobsLink)









    # Takes the link, turns it into something the Selenium driver can read
    # And waits for the page to load with the jobs
    def linkToHTML(self, link):
        #Gets URL, add .content to turn it into something readable
            print("In The Link Algorithm")
            self.seleniumDriver.get(link.strip())
            time.sleep(5)
            print("Next Phase Of Link Algorithm")
            try:
                WebDriverWait(self.seleniumDriver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "li"))
                )
                time.sleep(2)
            except:
                return None

            return self.seleniumDriver.find_elements(By.TAG_NAME, "a")










    # The skeleton of the search algorithm for gathering each webpage that contains
    # job links.
    def findLinks(self):
        self.ErrorLink = ""
        link = self.LinkedinJobsLink
        page = 1
        stopOnPage = 40
        # Makes a CSV if one doesnt exist, as the job links will be stored in a CSV
        if not os.path.exists(self.writeTo + '.csv'):
            open(self.writeTo + '.csv', 'x')
        if not os.path.exists('previousLinkedinJobs.csv'):
            open('previousLinkedinJobs.csv', 'x')
        self.seleniumDriver.get(link.strip())

        #Checks to see if it can find the number of postings then converts them into page numbers, so the scraper doesnt look over blank pages, thus saving time.
        try:
            time.sleep(5)
            numberOfJobsTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "jobs-search-results-list__subtitle")
            numberOfJobs=html2text.html2text(numberOfJobsTextHTML.get_attribute("innerHTML")).replace("\n", "")
            numberOfPages = math.ceil(int(re.findall(r'\d+', numberOfJobs.replace(",", ""))[0])/25)
            print("Number Of Pages: " + str(numberOfPages))
            if numberOfPages < stopOnPage:
                stopOnPage = numberOfPages
                print("StopOnPage: " + str(numberOfPages))
        except:
            print("Was unable to find the number of jobs.\nDefaulting to 40 pages (the max you can get)")

        while True:
            # Grabs a webpages a tags (an HTML DOM element which holds web links)
            a_tags = self.linkToHTML(link)
            print("current link: " + link)
            #print(urlHTML)
            if a_tags is not None:
                # Gathers the job postings on a page or stops the algorithm when there are none
                keepGoing = self.linkAlgorithm(a_tags)

                #Removed so it can search the maximum amount of jobs
                """
                if keepGoing == False:
                    break
                """
                page += 1
                if page >= stopOnPage:
                    break
                # Goes to the next page of job listings on the job search engine.
                link = self.LinkedinJobsLink + "&start=" + str(25*(page-1))
                print("nextLink= " + link)
            else:
                print("Did not find what you are looking for!")
                break


        print("Task Ended Sucessfully")







    # Checks to see if the link is not downloadable as we are not downloading anything
    def isProperLink(self, url):
        # Checks if the href is actually a word
        if url is not None:
            # Checks if the href is actually there (at least one letter)
            if len(url) > 0:
                # Checks to make sure it is not a downloadable file type (i.e, the link is not sending you to a download)
                if "pdf" not in url and "zIp" not in url and "zip" not in url \
                        and "win" not in url and "mp3" not in url and "mp4" not in \
                        url and "jpg" not in url and "JPEG" not in url and \
                        "jpeg" not in url and "docx" not in url and "pptx" not in \
                        url and "png" not in url:
                    return True

        return False





    # Checking conditions for link in order to get the links that have job.
    # Typically each job search will have their own thing in each link to
    # differentiate a job from some other link.
    def linkConditions(self, url):
        #if "/jobs/view/" in url and "/jobs/view/externalApply/" not in url and "JOBS_HOME_ORGANIC" not in url and "alternateChannel" not in url:
        if "/jobs/view/" in url:
            return True
        return False





    # Generic algorithm which takes all the links from the webpage/selenium objects and
    # filters them so that only the jobs remain and then writes them to a csv file.
    def linkAlgorithm(self, a_tags):
        #Gets all of the links that are not a downlodable one
        urlCleaning=[a_tag.get_attribute("href") for a_tag in a_tags if self.isProperLink(a_tag.get_attribute("href"))]
        # Gets all of the links that are job postings
        urls=[re.sub(r'\/\?.+', "", url) for url in urlCleaning if self.linkConditions(url)]
        nonDuplicateURLS = [*set(urls)]
        urlsInCSV = [url for url in nonDuplicateURLS if url not in open('previousLinkedinJobs.csv', encoding="utf-8").read()]
        print(urlsInCSV)
        if len(urlsInCSV) > 0:
            for url in urlsInCSV:
                self.writeToCSV(url, self.writeTo)
                self.writeToCSV(url, "previousLinkedinJobs")
                if self.checkIfEnoughLinksInCSV():
                    return False
            return True
        return False





    # Generic CSV writter, which takes URLS (or any string for that matter) and places them in a CSV.
    def writeToCSV(self, finalURL, writeTo):
        csv = open(writeTo + '.csv', 'a', encoding="utf-8")
        csv.write(finalURL + "\n")
        csv.close()

    def checkIfEnoughLinksInCSV(self):
        csv = open(self.writeTo + '.csv', encoding="utf-8")
        numberOfLines = len(csv.readlines())
        csv.close()
        if numberOfLines >= self.numberOfJobsLimit:
            return True
        return False
