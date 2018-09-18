import sys
import cgi
import socket
 
if len(sys.argv) == 1:
  form = cgi.FieldStorage()
  monitor_ip = form.getvalue('monitor_ip')
else:
  monitor_ip = sys.argv[1]
  power = sys.argv[2]
 
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