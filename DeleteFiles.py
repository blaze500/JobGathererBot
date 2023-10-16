import os
import shutil

def DeleteJobFiles():

    fileNames=["LinkedinJobs.csv", "RefinedLinkedInJobCSV.csv", "IndeedJobs.csv", "RefinedIndeedJobCSV.csv"]
    for file in fileNames:
        if os.path.exists(file):
            # Due to windows giving a "[WinError 5] Access is denied python" for os.remove in python
            # due to it needing permissions, sometimes the folders need to be deleted by shutil.rmtree
            try:
                os.remove(file)
            except:
                shutil.rmtree(file)
