#https://automatetheboringstuff.com/2e/chapter18/
#https://www.devdungeon.com/content/read-and-send-email-python
import smtplib, json, os, keyring, requests, socket, datetime
from email.message import EmailMessage
currentDirectory = os.getcwd()

def getExternalIP():
    # Get the IP from the API endpoint.
    response = requests.get("https://api.myip.com")
    datas = response.json()
    external_IP = datas["ip"]
    hostname = socket.gethostname()
    ip_private = socket.gethostbyname(hostname)

    date = datetime.datetime.now()
    dateFormatted = date.strftime("%d-%m-%Y %X")

    #Create json object to be used in IP-log.json
    jsonExternalIP = {}
    #jsonExternalIP['IPs'] = []
    jsonExternalIP = {
        'external_IP' : external_IP,
        'date' : dateFormatted
        }
    #Write IP in IP-current.json
    with open('%s/IP-current.json' % currentDirectory,'w') as jsonFileIPs:
        json.dump(jsonExternalIP, jsonFileIPs, indent=4)
    return (external_IP, hostname, ip_private, dateFormatted)

#Read IP in IP-log.json
with open('%s/IP-current.json' % currentDirectory) as jsonFileIPsRead:
    fileIP = json.load(jsonFileIPsRead)
#Used to compare external_IP in file and the one retreived from the API.
oldIP = fileIP["external_IP"]

getExternalIP()
external_IP = getExternalIP()[0]
hostname = getExternalIP()[1]
ip_private = getExternalIP()[2]
dateFormatted = getExternalIP()[3]

if oldIP != external_IP:
    #Read emails in emailsNotifications.json
    with open('%s/emailsNotifications.json' % currentDirectory) as jsonFileEmails:
        emails = json.load(jsonFileEmails)
    #Since the created var emails is NOT a dictonary, it's necessary to place the position [0]
    emailSendNotification = emails["emails"][0]["sendNotification"]
    emailReceiveNotification = emails["emails"][0]["receiveNotification"]
    #Retreive password, in keyring, for the email used to send notifications
    password = keyring.get_password("IP_notification", emailSendNotification)
    #Connect with smtp from google
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(emailSendNotification, password)
    #build the body
    subject = "[Notification] - External IP"
    body = "New External IP: %s \nHostname: %s \nHost IP: %s \nOld External IP: %s" %(external_IP, hostname, ip_private, oldIP)
    email_message = EmailMessage()
    email_message.add_header('Subject', subject)
    email_message.add_header('X-Priority', '1')
    email_message.set_content(body)
    #Send the email
    sendmailStatus = smtpObj.sendmail(emailSendNotification, emailReceiveNotification, email_message.as_bytes())
    if sendmailStatus != {}:
        print('There was a problem sending email to %s: %s' % (emailReceiveNotification, sendmailStatus))
    smtpObj.quit()
#Write the IP and time of execute on .log file
with open('%s/IP-log.log' % currentDirectory, 'a+') as f:
    f.write('IP: '+ external_IP + ' Date: '+ dateFormatted + '\n' )
    f.close()