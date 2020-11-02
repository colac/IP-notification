import os, time, socket
import sendMail

#get script directory to open .json files on sendMail.py
currentDirectory = os.path.dirname(os.path.realpath(__file__))

#Maximum temperature to set the trigger
maxTemp = 30

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return float(temp.replace("temp=","").replace("'C",""))

if ( measure_temp() >= maxTemp ):
        hostname = socket.gethostname()
        temperature = measure_temp()
        #print ("Temp higher than: %sºC\nCurrent Temp: %sºC" %(maxTemp, temperature))
        subject = "[Notification] - High Temps on RaspberryPie"
        body = "Temperature: %sºC\nHostname: %s" %(temperature, hostname)
        sendMail.sendMail(subject, body, currentDirectory)