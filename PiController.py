import sys
import cgi
import socket
import RPi.GPIO as GPIO
import time

power= "OFF"

def ProjectorTurn(power, monitor_ip):
    # if len(sys.argv) == 1:
    #   form = cgi.FieldStorage()
    #   monitor_ip = form.getvalue('monitor_ip')
    # else:
    #   monitor_ip = sys.argv[1]
    #   power = sys.argv[2]
    
    #define some constanst to make life easier
    port = 4352
    buffer_size = 1024
    
    if (power == 'ON'):
        command = '%1POWR 1\r'
    elif (power == 'OFF'):
        command = '%1POWR 0\r'
    else:
        command = '%1POWR ?\r'
        print ("Invalid command.")
        print ("Use: IP ON|OFF")
        print ("getting current status of device:")
    
    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new.connect((monitor_ip, port))
    recv_data = new.recv(buffer_size)
    print (recv_data)
    print ("sending: ", command)
    new.send(command)
    recv_data = new.recv(buffer_size)
    print (recv_data)
    new.close()

while True:
    try:
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
        if power == 'OFF':
            GPIO.add_event_detect(10,GPIO.RISING,callback=ProjectorTurn("ON","10.0.0.1")) # Setup event on pin 10 rising edge
        else:
            GPIO.add_event_detect(10,GPIO.RISING,callback=ProjectorTurn("OFF","10.0.0.1")) # Setup event on pin 10 rising edge
    except:
        print("Bedienung Fehlgeschlagen")
        time.sleep(30)


        

    GPIO.cleanup() # Clean up