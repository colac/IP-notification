#https://automatetheboringstuff.com/2e/chapter18/
#https://www.devdungeon.com/content/read-and-send-email-python
import smtplib, json, os, keyring, requests, socket, datetime
from email.message import EmailMessage
#currentDirectory = os.getcwd()

def sendMail(subject, body, currentDirectory):
    #Read emails in emailsNotifications.json
    with open(currentDirectory + '/' + 'emailsNotifications.json') as jsonFileEmails:
        emails = json.load(jsonFileEmails)
    #Since the created var emails is NOT a dictonary, it's necessary to place the position [0]
    emailSendNotification = emails["emails"][0]["sendNotification"]
    emailReceiveNotification = emails["emails"][0]["receiveNotification"]
    #Retreive password, in keyring, for the email used to send notifications
    #password = keyring.get_password("IP_notification", emailSendNotification)
    with open(currentDirectory + '/' + 'secrets.json') as jsonSecrets:
        secrets = json.load(jsonSecrets)
    password = secrets["password"]
    #Connect with smtp from google
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(emailSendNotification, password)
    #build the body
    #subject = "[Notification] - External IP"
    #body = "New External IP: %s \nHostname: %s \nHost IP: %s \nOld External IP: %s" %(external_IP, hostname, ip_private, oldIP)
    email_message = EmailMessage()
    email_message.add_header('Subject', subject)
    email_message.add_header('X-Priority', '1')
    email_message.set_content(body)
    #Send the email
    sendmailStatus = smtpObj.sendmail(emailSendNotification, emailReceiveNotification, email_message.as_bytes())
    if sendmailStatus != {}:
        print('There was a problem sending email to %s: %s' % (emailReceiveNotification, sendmailStatus))
    smtpObj.quit()