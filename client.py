import socket	
import sys	

try:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error:
	print 'Failed to create socket'
	sys.exit()
	
print 'Socket Created'

host = '127.0.0.1';

port = 8888;

try:
	remote_ip = socket.gethostbyname( host )

except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()

s.connect((remote_ip , port))

print 'Socket Connected to ' + host + ' on ip ' + remote_ip

reply = s.recv(4096)

print reply

message = raw_input("Enter Message to send(Enter 0 to escape):")
while message != '0':
	
	try :
		s.sendall(message)
	except socket.error:
		print 'Send failed'
		sys.exit()
	print 'Message send successfully'
	
	reply = s.recv(4096)
	print reply
	
	message = raw_input("Enter Message to send(Enter 0 to escape):")
s.close()