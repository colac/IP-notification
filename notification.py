#https://automatetheboringstuff.com/2e/chapter18/
#https://www.devdungeon.com/content/read-and-send-email-python
import smtplib, json, os, keyring, requests, socket, datetime
from email.message import EmailMessage
import sendMail
currentDirectory = os.getcwd()

def getExternalIP():
    #Read IP in IP-log.json
    with open('%s/IP-current.json' % currentDirectory) as jsonFileIPsRead:
        fileIP = json.load(jsonFileIPsRead)
    #Used to compare external_IP in file and the one retreived from the API.
    oldIP = fileIP["external_IP"]
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
    jsonExternalIP = {
        'external_IP' : external_IP,
        'date' : dateFormatted
        }
    #Write IP in IP-current.json
    with open('%s/IP-current.json' % currentDirectory,'w') as jsonFileIPs:
        json.dump(jsonExternalIP, jsonFileIPs, indent=4)
    #function to compare IPs and define the $body
    if oldIP != external_IP:
        subject = "[Notification] - External IP"
        body = "New External IP: %s \nHostname: %s \nHost IP: %s \nOld External IP: %s" %(external_IP, hostname, ip_private, oldIP)
        sendMail.sendMail(subject, body)
        return external_IP, hostname, ip_private, dateFormatted, oldIP

external_IP, hostname, ip_private, dateFormatted, oldIP = getExternalIP()

#Write the IP and time of execute on .log file
with open('%s/IP-log.log' % currentDirectory, 'a+') as f:
    f.write('IP: '+ external_IP + ' Date: '+ dateFormatted + '\n' )
    f.close()