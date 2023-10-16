import os
import Webscraper_JobFinder as JobFinder
import DeleteFiles
import SendEmailToMyself
import pandas as pd

class GUI:

    #Starts the Program
    def __init__(self):
        os.chdir("/Users/EpicGamerDude/PycharmProjects/pythonProject1")
        DeleteFiles.DeleteJobFiles()
        self.Questionare()

        #self.JobFinder = JobFinder.JobFinder(self.field, self.type, self.location, self.inPerson, self.fullTime, self.salary, self.experience, self.education)
        self.JobFinder = JobFinder.JobFinder()
        self.DoProgram()

    def DoProgram(self):
        self.JobFinder.LoginToJobs()
        self.JobFinder.GetJobLinks()
        self.JobFinder.RefineJobLinks()
        self.JobFinder.EndProgram()
        results = pd.read_csv('RefinedLinkedInJobCSV.csv')
        if len(results) > 0:
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