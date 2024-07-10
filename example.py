import re
import sys

print ("-- Client-server application --")

IP_server   = str(sys.argv[1])
server_port = str(sys.argv[2])
flag_1      = str(sys.argv[3])
flag_2      = str(sys.argv[4])
flag_3      = str(sys.argv[5])
file_log    = str(sys.argv[6])

# message = input ("write a message: ")
# print (message)
# spec_num = []
# spec_num = re.split(' ', message)
# print ("1: ", spec_num)
print ("arg: " + IP_server + ' ' + server_port + ' ' + flag_1 + ' ' + flag_2 + ' ' + flag_3 + ' ' + file_log)






