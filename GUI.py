import os
import Webscraper_JobFinder as JobFinder
import DeleteFiles
import SendEmailToMyself
import pandas as pd
import sys

class GUI:

    #Starts the Program
    def __init__(self):
        os.chdir("/Users/jaden/PycharmProjects/JobGathererBot")
        DeleteFiles.DeleteJobFiles()
        self.Questionare()

        #self.JobFinder = JobFinder.JobFinder(self.field, self.type, self.location, self.inPerson, self.fullTime, self.salary, self.experience, self.education)
        self.JobFinder = JobFinder.JobFinder()
        self.DoProgram()

    def DoProgram(self):
        #Is writting down any print statements into a file so that it can be checked in case there have been site changes/errors
        sys.stdout = open("report.txt", "w")

        self.JobFinder.LoginToJobs()
        self.JobFinder.GetJobLinks()
        self.JobFinder.RefineJobLinks()
        self.JobFinder.EndProgram()

        sys.stdout.close()

        SendEmailToMyself.sendEmailToMyself()


    def Questionare(self):
        self.field = '"python" OR "java"'
        self.type = 'job'
        self.location = "jacksonville,florida"
        self.inPerson = "both"
        self.fullTime = "full time"
        self.salary = 0
        self.education = "bachelor"
        self.experience = "entry"

GUI()