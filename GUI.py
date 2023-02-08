import LocationChecker
import easygui as gui
import Webscraper_JobFinder as JobFinder
import sys
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import multidict as multidict
import DeleteFiles

class GUI:

    #Starts the Program
    def __init__(self):
        start = gui.buttonbox("Welcome to the Job Analytics Bot?", title='Job Analytics Bot', choices=["Start", "Exit"])
        if start == "Exit" or start is None:
            sys.exit()
        DeleteFiles.DeleteJobFiles()
        self.Questionare()

        msg0 = "What words must be in these job descriptions?"
        self.mustHaveWords = gui.enterbox(msg0, title='Job Analytics Bot')
        if self.mustHaveWords is None:
            sys.exit()
        else:
            txtFile = open('mustHaveWords.txt', 'a', encoding="utf-8")
            txtFile.write(self.mustHaveWords.lower().replace(', ', '\n'))
            txtFile.close()

        msg1 = "What words should the job descriptions contain at least one of?"
        self.atLeastOneOfWords = gui.enterbox(msg1, title='Job Analytics Bot')
        if self.atLeastOneOfWords is None:
            sys.exit()
        else:
            txtFile = open('atLeastOneOfWords.txt', 'a', encoding="utf-8")
            txtFile.write(self.atLeastOneOfWords.lower().replace(', ', '\n'))
            txtFile.close()
        gui.msgbox("Please Do Not Close The Browser That Will Open Up After Reading This Message \nAt Any Point While Using The Program Or It Will Cause An Error!", title='Job Analytics Bot')
        self.JobFinder = JobFinder.JobFinder(self.field, self.type, self.location, self.inPerson, self.fullTime, self.salary, self.experience, self.education)
        gui.msgbox("This Browser Is What Will Be Referred To As The Selenium Browser. \nAgain, Please Do NOT Close This Browser At Any Point During The Program!", title='Job Analytics Bot')
        self.DoProgram()

    def DoProgram(self):
        self.JobFinder.LoginToJobs()
        self.JobFinder.GetJobLinks()
        self.JobFinder.RefineJobLinks()
        self.JobFinder.EndProgram()


    def Questionare(self):
        msg1 = "What Field Of Work Are You Looking For?"
        fow = "Field Of Word"
        self.field = gui.enterbox(msg1, title='Job Analytics Bot')
        if self.field is None:
            sys.exit()
        elif len(self.field) > 0:
            self.field.lower()


        msg2 = "Are You Looking For a Job or Internship?"
        joi = ["Job", "Internship"]
        self.type = gui.buttonbox(msg2, title='Job Analytics Bot', choices=joi)
        if self.type is None:
            sys.exit()
        else:
            self.type.lower()

        while True:
            msg3 = "What city do you want this job to be located at? \nIf you are not looking for a specific location leave these fields blank"
            cos = ["City", "State"]
            cityAndState = gui.multenterbox(msg3, title='Job Analytics Bot', fields=cos)

            if cityAndState is None:
                sys.exit()
            if cityAndState[0] == "" and cityAndState[1] == '':
                self.location = ""
                break
            elif LocationChecker.isCity(cityAndState[0]) and LocationChecker.isState(cityAndState[1]):
                if LocationChecker.isLocation(cityAndState[0] + "," + cityAndState[1]):
                    self.location = cityAndState[0] + "," + cityAndState[1]
                    break
                else:
                    gui.msgbox("The City And State You Have Choosen Do Not Exist Together. \nPlease Try Again.")
            else:
                if len(cityAndState[0]) > 0 and len(cityAndState[1]) > 0:
                    gui.msgbox("The City And State You Have Choosen Do Not Exist Together. \nPlease Try Again.")
                else:
                    gui.msgbox("You Must Either Leave Both Fields Blank or Fill Them BOTH Out. \nPlease Try Again.")

        msg4 = "Do You Want This Job To Be Remote, In Person, or Both?"
        roip = ["Remote", "In Person", "Both"]
        self.inPerson = gui.buttonbox(msg4, title='Job Analytics Bot', choices=roip).lower()
        if self.inPerson is None:
            sys.exit()
        else:
            self.inPerson.lower()

        msg5 = "Do You Want This Job To Be Full Time, Part Time, Or Both?"
        ftopt = ["Full Time", "Part Time", "Both"]
        self.fullTime = gui.buttonbox(msg5, title='Job Analytics Bot', choices=ftopt).lower()
        if self.fullTime is None:
            sys.exit()
        else:
            self.fullTime.lower()

        msg6 = "What Yearly Salary Are You Looking For?\nYour Salary Cannot Exceed One Million Dollars Nor Be Lesser Than 0\nType In 0 If You Aren't Looking For A Specific Salary"
        self.salary = gui.integerbox(msg6, title='Job Analytics Bot', upperbound=1000000)
        if self.salary is None:
            sys.exit()

        msg7 = "What Is The Highest Level Of College Education You Have?"
        degree = ["Associate", "Bachelor", "Masters", "None"]
        self.education = gui.buttonbox(msg7, title='Job Analytics Bot', choices=degree).lower()
        if self.education is None:
            sys.exit()
        elif self.education == "None":
            self.experience = ''
        else:
            self.education.lower()

        msg8 = "What is your experience level?"
        experience = ["Entry", "Mid", "Senior", "None"]
        self.experience = gui.buttonbox(msg8, title='Job Analytics Bot', choices=experience).lower()
        if self.experience is None:
            sys.exit()
        elif self.experience == "None":
            self.experience = ''
        else:
            self.experience.lower()



GUI()
