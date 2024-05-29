import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def sendEmailToMyself():
    emailMyselfInfo = open('EmailMyselfInfo.txt', 'r', encoding="utf-8").read().splitlines()
    fromaddr = emailMyselfInfo[0]
    toaddr = emailMyselfInfo[1]
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Jobs For The Day"
    body = "Here is your CSV with your jobs for the day."
    msg.attach(MIMEText(body, 'plain'))
    filename = "RefinedLinkedInJobCSV.csv"
    attachment = open("RefinedLinkedInJobCSV.csv", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, emailMyselfInfo[2])
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
