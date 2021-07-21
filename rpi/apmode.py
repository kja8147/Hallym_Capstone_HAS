import commands
import sys
import time
import string
import re
import os
import socket

class RssMeasure:
    def __init__(self, UserX=None, UserY=None, UserZ=None):
        self.UserX = UserX
        self.UserY = UserY

        self.rpi01 = "0"
        self.rpi02 = "0"
        self.rpi03 = "0"
        self.rpi04 = "0"
        self.rpi05 = "Tx"

    def Rssi(self, commandStr):
        failcheck, result = commands.getstatusoutput(commandStr)
        self.originStr = result
        return failcheck

    def RssFilter(self):
        strResults = ""
        target = "Address:"
        index = -1

        mystr = self.originStr.strip()

        mystr = mystr.replace("--","")
        mystr = mystr.replace("Encryption key:on", "")
        mystr = mystr.replace("Quality=", "")
        mystr = mystr.replace('"', "")
        mystr = " ".join(mystr.split())

        while True:
           index = mystr.find(target, index+1)
           if index == -1:
                break
           strResults += mystr[index-5:index+110]+'\n'

	        strResult = strResults.split('\n')
	        strResults = ""
           for i in strResult:
                address_rst = i.find("Address:")
                level_rst = i.find("level=")
                dbm_rst = i.find("dBm")

                dbm = i[level_rst+6:dbm_rst-1]
                address = i[address_rst+9:address_rst+26]

		        #print(address, dbm)

		if dbm != '' and address!='':
			#rpi01(192.168.5.1)
			if address == "DC:A6:32:9E:C8:4F" or address == "88:36:6C:FF:69:DD":
				self.rpi01 = dbm
			#rpi02(192.168.6.1)
			elif address=="DC:A6:32:9E:6A:7D" or address== "88:36:6C:FF:50:A3":
				self.rpi02 = dbm
			#rpi03(192.168.7.1)
			elif address=="DC:A6:32:AF:6D:42" or address== "88:36:6C:FF:59:EC":
				self.rpi03 = dbm
			#rpi04(192.168.8.1)
			elif address=="DC:A6:32:71:11:23" or address== "88:36:6C:FF:6A:28":
				self.rpi04 = dbm
			#rpi05(192.168.9.1)
			elif address=="DC:A6:32:71:13:B4" or address== "88:36:6C:FF:59:D0":
				self.rpi05 = dbm

#소켓 생성
if __name__ == '__main__':
    myCommand = 'sudo iwlist wlan0 scan | grep -E -A 5 "Address:"'
    HOST = '10.50.234.145'
    PORT = 9999

    #if len(sys.argv) <= 1:
	#print "Lack is parameters"
	#sys.exit(0)
    #type = sys.argv[1]

# 3 prev work
# 2 upload from ap
# 1 localization

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('set')
    client_socket.connect((HOST, PORT))
    print('connect')

    dic = {}
    index = 0

    while True:
	try:
		type = int(input('Input Type : '))
		x, y, z, i = 0, 0, 0, 0

		if type == 2:
			while True:
				o = RssMeasure(str(x), str(y), str(z))

		        	failcheck = o.Rssi(myCommand)

       	 			if failcheck :
            				print("Error")
					continue

       	 			temp_data = o.RssFilter()

                    data = str(type)+":0:0"
                    data += ":"+o.rpi01+":"+o.rpi02+":"+o.rpi03+":"+o.rpi04+":"+o.rpi05
                    print(data)

                    client_socket.send(data)

        except KeyboardInterrupt:
       	    break

        except Exception as e:
            print e
            break

    client_socket.close()
