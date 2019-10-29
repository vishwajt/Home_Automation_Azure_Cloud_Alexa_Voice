import RPi.GPIO as GPIO
import time
from pubnub import Pubnub

pub_key = "Your Azure Device Public Key"
sub_key = "Your Azure Device Subscription Key"
 
LIGHT1 = 18           #define pin of RPi on which you want to take output
 
def init():
    global pubnub
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LIGHT,GPIO.OUT)
    GPIO.output(LIGHT, False)
    pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key)
    pubnub.subscribe(channels='alexaTrigger', callback=callback, error=callback, reconnect=reconnect, disconnect=disconnect)
 
def control_alexa(controlCommand):      
    if(controlCommand.has_key("trigger")):
        if(controlCommand["trigger"] == "light" and controlCommand["status"] == 1):
            GPIO.output(LIGHT, True) 
            print "light is on"
        else:
            GPIO.output(LIGHT, False) 
            print "light is off"
    else:
        pass
 
def callback(message, channel):        #this function waits for the message from the aleatrigger channel
    if(message.has_key("requester")):
        control_alexa(message)
    else:
        pass
 
def error(message):                    #if there is error in the channel,print the  error
    print("ERROR : " + str(message))

def reconnect(message):                #responds if server connects with pubnub
    print("RECONNECTED")
 
def disconnect(message):               #responds if server disconnects with pubnub
    print("DISCONNECTED")

if __name__ == '__main__':
 init()
