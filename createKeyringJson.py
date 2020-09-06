#This script creates the keyring user+password and the JSON file with the emails used
#Install library: pip install keyring
import keyring, json, getpass, os, sys

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
currentDirectory = os.getcwd()
with open('%s/emailsNotifications.json' % currentDirectory,'w') as jsonFile:
    json.dump(json_obj, jsonFile)