#https://automatetheboringstuff.com/2e/chapter18/
#https://www.devdungeon.com/content/read-and-send-email-python
import smtplib, json, os, keyring, requests, socket, datetime
from email.message import EmailMessage
currentDirectory = os.getcwd()

# Get the IP from the API endpoint.
response = requests.get("https://api.myip.com")
datas = response.json()
ip_public = datas["ip"]
hostname = socket.gethostname()
ip_private = socket.gethostbyname(hostname)

date = datetime.datetime.now()
dateFormatted = date.strftime("%d-%m-%Y %X")

#Create json object to be used in IP-log.json
jsonExternalIP = {}
jsonExternalIP['IPs'] = []
jsonExternalIP['IPs'].append({
    'external_IP' : ip_public,
    'date' : dateFormatted
    })
#Write IP in IP-log.json
with open('%s/IP-log.json' % currentDirectory,'w') as jsonFileIPs:
    json.dump(jsonExternalIP, jsonFileIPs)

#Read IP in IP-log.json
with open('%s/IP-log.json' % currentDirectory) as jsonFileIPsRead:
    fileIP = json.load(jsonFileIPsRead)

oldIP = fileIP["IPs"][0]["external_IP"]
print(oldIP)

#Read emails in emailsNotifications.json
with open('%s/emailsNotifications.json' % currentDirectory) as jsonFileEmails:
    emails = json.load(jsonFileEmails)

#Since the created var emails is NOT a dictonary it is needed to place the position [0]
emailSendNotification = emails["emails"][0]["sendNotification"]
emailReceiveNotification = emails["emails"][0]["receiveNotification"]

password = keyring.get_password("IP_notification", emailSendNotification)

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(emailSendNotification, password)
#build the body
subject = "[Notification] - External IP"
body = "External IP: %s \nHostname: %s \nHost IP: %s" %(ip_public, hostname, ip_private)
email_message = EmailMessage()
email_message.add_header('Subject', subject)
email_message.add_header('X-Priority', '1')
email_message.set_content(body)

sendmailStatus = smtpObj.sendmail(emailSendNotification, emailReceiveNotification, email_message.as_bytes())
if sendmailStatus != {}:
    print('There was a problem sending email to %s: %s' % (emailReceiveNotification, sendmailStatus))
smtpObj.quit()