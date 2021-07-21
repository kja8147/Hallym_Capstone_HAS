import glob
import string

def Filter(line):
    address_id = line.find("Address:")
    address = line[address_id+9:]
    return address

dic = {}
index = 0

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

print(dic)
print(len(dic))

list = []
for i in range(len(dic)):
    list.append(0)

#result_data = "3:0:0"
result_data = ""

#sample_mac = '00:40:5A:AF:56:D9'
sample_mac = '60:D0:2C:0D:69:FC'
sample_rss = str(-30)

for i in range(len(dic)):
    key = ""

    if dic.has_key(sample_mac):
	list[dic[sample_mac]] = sample_rss


for i in list:
    result_data += ":"+str(i)

print(result_data)

