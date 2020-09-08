#This script creates:
# The keyring user+password
# The JSON file with the emails used, emailsNotifications.json
# The JSON file with the current external IP, IP-current.json
#Install library: pip install keyring
import keyring, json, getpass, os, sys, smtplib, requests, datetime, socket
from keyring import get_keyring
get_keyring()
currentDirectory = os.getcwd()
def getExternalIP():
    currentDirectory = os.getcwd()
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
    return (external_IP, hostname, ip_private)

getExternalIP()

argList = ["-d", "-debug", "d", "debug"]

#Used for debuggin the creation of emailsNotifications.json
#If no argument is given, the script executes as normal
if len(sys.argv) == 1:
    emailToReceive = input("Type the email to receive notifications: ")
#Ask user email and password
    emailToSend = input("Type the email to be used to send notifications: ")
    password = getpass.getpass(prompt="Password: ", stream=None)
#Create credentials on keyring
    keyring.set_password("IP_notification", emailToSend, password)
    #print(keyring.get_password("IP_notification", email))
#Create json object to be used in emailsNotifications.json
    json_obj = {}
    json_obj['emails'] = []
    json_obj['emails'].append({
        'sendNotification' : emailToSend,
        'receiveNotification' : emailToReceive
        })
#If the argument provided is in the list argList, the file emailsNotifications.json is created with dummy emails
elif sys.argv[1] in argList:
    arg = sys.argv[1]
    print("The argument is '%s'" % arg)
    json_obj = {}
    json_obj['emails'] = []
    json_obj['emails'].append({
        'sendNotification' : "emailToSend@email.com",
        'receiveNotification' : "emailToReceive@email.com"
        })
else:
    print("Either pass argument d/-d/debug/-debug or simply execute without arguments!")
    sys.exit()

#Write the object to file.
with open('%s/emailsNotifications.json' % currentDirectory,'w') as jsonFile:
    json.dump(json_obj, jsonFile)
