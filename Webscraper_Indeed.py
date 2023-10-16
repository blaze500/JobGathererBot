import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os


class IndeedJobs:

    def __init__(self, type, field, inPerson, fullTime, salary, location, education, experience, writeTo, numberOfJobsLimit, seleniumDriver):
        self.type = type
        self.field = 'developer'
        self.inPerson = inPerson
        self.fullTime = fullTime
        self.salary = salary
        self.location = 'remote'
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
    def indeedJobsLinkMaker(self):

        self.indeedJobsLink = "https://www.indeed.com/jobs?"

        # Turns spaces into +, as weblinks cannot function with spaces in them. Normally however, this
        # is done by turning the space into its character number and then hexadecimal equivalent.
        if self.field != "" or self.salary >0:
            self.indeedJobsLink += "&q="
            if self.field != "":
                self.indeedJobsLink += self.field.replace(" ", "+")
            if self.salary > 0:
                if len(self.indeedJobsLink) > 31:
                    self.indeedJobsLink += "+"
                salaryWithCommas= '%24'+str("{:,}".format(self.salary))
                self.indeedJobsLink +=salaryWithCommas.replace(",","%2C")

        # Turns spaces into +, as weblinks cannot function with spaces in them. Normally however, this
        # is done by turning the space into its character number and then hexadecimal equivalent.
        if len(self.location) > 0:
            self.indeedJobsLink +="&l=" + self.location.replace(" ", "+")

        self.indeedJobsLink += "&sc=0kf%3A"

        if self.education == "associate":
            self.indeedJobsLink += "attr(FCGTU%7CQJZM9%7CUTPWG%252COR)"
        elif self.education == "bachelor":
            self.indeedJobsLink +="attr(FCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)"
        elif self.education == "masters":
            self.indeedJobsLink +="attr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)"
        else:
            self.indeedJobsLink += "attr(FCGTU%7CQJZM9%252COR)"

        if self.type == "internship":
            self.indeedJobsLink += "jt(internship)"
        elif self.fullTime == "full time":
            self.indeedJobsLink +="jt(fulltime)"
        elif self.fullTime == "part time":
            self.indeedJobsLink +="jt(parttime)"

        if self.inPerson == "remote":
            self.indeedJobsLink +="attr(DSQF7)"

        if self.experience == "entry":
            self.indeedJobsLink +="explvl(ENTRY_LEVEL)"
        elif self.experience =="mid":
            self.indeedJobsLink +="explvl(MID_LEVEL)"
        elif self.experience =="senior":
            self.indeedJobsLink +="explvl(SENIOR_LEVEL)"
        else:
            self.indeedJobsLink +="attr(D7S5D)"

        self.indeedJobsLink +="attr(X62BT)"

        self.indeedJobsLink += "%3B"
        print(self.indeedJobsLink)









    # Takes the link, turns it into something the Selenium driver can read
    # And waits for the page to load with the jobs
    def linkToHTML(self, link):
        #Gets URL, add .content to turn it into something readable
        self.seleniumDriver.get(link.strip())
        time.sleep(5)
        try:
            WebDriverWait(self.seleniumDriver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "li"))
            )
        except:
            #self.seleniumDriver.quit()
            #self.seleniumDriver.close()
            return None

        return self.seleniumDriver.find_elements(By.TAG_NAME, "a")










    # The skeleton of the search algorithm for gathering each webpage that contains
    # job links.
    def findLinks(self):
        link = self.indeedJobsLink
        page = 1
        # Makes a CSV if one doesnt exist, as the job links will be stored in a CSV
        if not os.path.exists(self.writeTo + '.csv'):
            open(self.writeTo + '.csv', 'x')
        if not os.path.exists('previousIndeedJobs.csv'):
            open('previousIndeedJobs.csv', 'x')
        while True:
            # Grabs a webpages a tags (an HTML DOM element which holds web links)
            a_tags = self.linkToHTML(link)
            print("current link: " + link)
            #print(urlHTML)
            if a_tags is not None:
                # Gathers the job postings on a page or stops the algorithm when there are none
                keepGoing = self.linkAlgorithm(a_tags)
                if keepGoing == False:
                    break
                page += 1
                #Goes to the next page of job listings on the job search engine.
                link = self.indeedJobsLink + "&start=" + str((page-1)*10)
                print("nextLink= " + link)
            else:
                print("Did not find what you are looking for!")
                break
        #self.seleniumDriver.quit()
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
        if "/rc/clk?jk=" in url:
            return True
        return False





    # Generic algorithm which takes all the links from the webpage/selenium objects and
    # filters them so that only the jobs remain and then writes them to a csv file.
    def linkAlgorithm(self, a_tags):
        #Gets all of the links that are not a downlodable one
        urlCleaning=[a_tag.get_attribute("href") for a_tag in a_tags if self.isProperLink(a_tag.get_attribute("href"))]
        # Gets all of the links that are job postings
        urls=[url for url in urlCleaning if self.linkConditions(url)]
        nonDuplicateURLS = [*set(urls)]
        urlsInCSV = [url for url in nonDuplicateURLS if url not in open('previousIndeedJobs.csv', encoding="utf-8").read()]
        print(urlsInCSV)
        if len(urlsInCSV) > 0:
            for url in urlsInCSV:
                self.writeToCSV(url, self.writeTo)
                self.writeToCSV(url, "previousIndeedJobs")
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