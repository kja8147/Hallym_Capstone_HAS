import commands
import sys
import time
import string
import re
import os
import socket
import glob

def Filter(line):
    address_id = line.find("Address:")
    address = line[address_id+9:]
    return address

class RssMeasure:
    def __init__(self, UserX=None, UserY=None, UserZ=None):
        self.UserX = UserX
        self.UserY = UserY
        self.UserZ = UserZ

    def Rssi(self, commandStr):
        failcheck, result = commands.getstatusoutput(commandStr)
        self.originStr = result
        return failcheck

    def RssFilter(self):
		global dic
		list = [0 for _ in range(len(dic))]

        strResults = ""
        target = "Address:"
        index = -1

		rpi01, rpi02, rpi03, rpi04, rpi05 = "0", "0", "0", "0", "0"

        mystr = self.originStr.strip()
		mystr = mystr.replace("--","")
        mystr = mystr.replace("Encryption key:on", "")
		mystr = mystr.replace("Quality=", "")
		mystr = mystr.replace('"', "")
        mystr = " ".join(mystr.split())

		#print(mystr)

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
			if dic.has_key(address):
				list[dic[address]] = dbm
			elif address == "DC:A6:32:9E:C8:4F" or address == "88:36:6C:FF:69:DD":
                                rpi01 = dbm
                        #rpi02(192.168.6.1)
                        elif address=="DC:A6:32:9E:6A:7D" or address== "88:36:6C:FF:50:A3":
                                rpi02 = dbm
                        #rpi03(192.168.7.1)
                        elif address=="DC:A6:32:AF:6D:42" or address== "88:36:6C:FF:59:EC":
                                rpi03 = dbm
                        #rpi04(192.168.8.1)
                        elif address=="DC:A6:32:71:11:23" or address== "88:36:6C:FF:6A:28":
                                rpi04 = dbm
                        #rpi05(192.168.9.1)
                        elif address=="DC:A6:32:71:13:B4" or address== "88:36:6C:FF:59:D0":
                                rpi05 = dbm

		return_data = ":"+rpi01+":"+rpi02+":"+rpi03+":"+rpi04+":"+rpi05

		for temp in list:
			return_data += ":"+str(temp)

	return return_data

if __name__ == '__main__':
    myCommand = 'sudo iwlist wlan0 scan | grep -E -A 5 "Address:"'
    HOST = '10.50.231.173'
    #HOST = '10.50.245.211'
    PORT = 9999

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

		if type <= 0:
			break

		if type == 4:
			file_list = glob.glob('*.txt')
			print(file_list)

			for file_name in file_list:
			    print(file_name)
			    f = open(file_name, 'r')

			    while True:
			        line = f.readline()
			        if not line: break
			        address = Filter(line.strip())

			        #print(line, address)
			        if not dic.has_key(address):
			            dic[address] = index
			            index = index+1
				    #print(address, index)
			    f.close()

			#print(len(dic))

		if type == 1 or type == 3:
			if type == 3:
				x = int(input('Input User X : '))
				if x <= -1:
					break

				y = int(input('Input User Y : '))
				#z = int(input('Input User Z : '))

			while i < 5:
				o = RssMeasure(str(x), str(y), str(z))

		        	failcheck = o.Rssi(myCommand)

       	 			if failcheck :
            				print("Error")
					time.sleep(3)
					continue

       	 			temp_data = o.RssFilter()

				data = str(type)+":"+o.UserX+":"+o.UserY
				data += temp_data
				print(data)

				client_socket.send(data)
				time.sleep(3)
				if type == 1:
					continue

				i = i+1
		else:
			continue
        except KeyboardInterrupt:
       	    break

        except Exception as e:
            print e
            break

    client_socket.close()
