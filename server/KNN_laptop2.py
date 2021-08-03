import pickle
import socket
import numpy as np
from _thread import *
from collections import defaultdict
import coordinates as coordinate
radioMap=defaultdict(list)
radioMidMap=defaultdict(list)
fingerDistance=defaultdict()

apLength=314  #variable length: rss1,rss2,rss3,rss4,rss5,rss6
rssLength=7 #variable length: rss1=[rsslength개의 rss값]
prev_x,prev_y=-1,-1
count=0
user_count = 0

KNN_flag=True
param_K=1

rsslist=[[0 for i in range(rssLength)] for row in range(apLength)]
midValueList=[]

GUI_FILE_NAME = "draw.txt"

class Laptop:
    def enqueue(self, value, list, length):

        if len(list) < length:
            list.append(value)
        else:
            del list[0]
            list.append(value)

    #set rssList's middle value
    def setMidValue(self,list):

        listCopy=list[:]
        listCopy.sort()
        midValue = listCopy[int(len(listCopy) / 2)]
        midValueList.append(midValue)

    # by 김진아, euclidean distance
    def eucliDis(self,mapRss, userRss):

        temp_sum = 0
        len1 = len(mapRss)

        for i in range(len1):
            temp_sum += np.power(mapRss[i] - userRss[i], 2)
        return np.sqrt(temp_sum)



    def saveFile(self):

        n = input('enter the save')
        if n == 'save':
            with open("radioMap_night.pickle", "wb") as fw:
                pickle.dump(radioMap, fw)
            with open("radioMidMap_night.pickle", "wb") as fw2:
                pickle.dump(radioMidMap, fw2)

def draw(return_mode, return_user_id, return_REALx, return_REALy):
    f = open(GUI_FILE_NAME, 'w')

    data  = str(return_mode) + ":" + str(return_user_id) + ":" + str(return_REALx) + ":" + str(return_REALy)
    f.write(data)
    f.close()

# 화면 좌측 상단이 (0,0) 으로 시작하는 지점이다.
def func(mode, id, REALx, REALy):
    plt.clf()
    plt.imshow(im)

    IMGWIDTH = 1596
    REALWIDTH = 152.8

    IMGHEIGHT = 462
    REALHEIGHT = 44.2

    if mode == MODE_TRILATERATION:
        REALx += TRI_REALx_OFFSET
        REALy += TRI_REALy_OFFSET

    gui_x = REALx * IMGWIDTH / REALWIDTH
    gui_y = REALy * IMGHEIGHT / REALHEIGHT

    if id == 1:
        loc.aGUILocation = [gui_x, gui_y]
        # print("aLocation을 업데이트 합니다.")
        #print(loc.aGUILocation)
    elif id == 2:
        loc.bGUILocation = [gui_x, gui_y]
        # print("bLocation을 업데이트 합니다.")
        #print(loc.bGUILocation)
    else:
        assert False, "잘못된 ID 값입니다."

    plt.plot(loc.aGUILocation[0], loc.aGUILocation[1], 'ro')
    # print("plot:")
    # print(loc.aGUILocation)
    plt.plot(loc.bGUILocation[0], loc.bGUILocation[1], 'bo')
    # print("plot:")
    # print(loc.bGUILocation)

#start loaction tracking
def tracking(data,addr,user_count):

    global prev_x,prev_y,rsslist,midValueList,count

    fingerPrintRss = data[8::]
    #save radioMap
    if data[0]==3:

        cur_x, cur_y = data[1], data[2]

        if cur_x == prev_x and cur_y == prev_y: #when loaction fixed
            pass
        else:   #when loaction changed
            rsslist = [[0 for i in range(rssLength)] for row in range(309)] #reset rsslist

        for i in range(len(fingerPrintRss)):
            q.enqueue(fingerPrintRss[i], rsslist[i], rssLength)
        for value in radioMap[cur_x,cur_y]:
            q.setMidValue(value)

        #save rss at rsslist
        radioMap[cur_x, cur_y] = rsslist
        radioMidMap[cur_x, cur_y] = midValueList

        print(count)

        if cur_x == 28 and cur_y == 0:
            if count ==4:
                q.saveFile()
            count= count+1

        prev_x, prev_y = cur_x, cur_y
        midValueList = []

    #track location
    elif data[0]==1:
        # by 김진아, fingerprint 
        if(KNN_flag ==False):
            with open("radioMap_night.pickle", "rb") as fr:
                radioMap_result = pickle.load(fr)

            with open("radioMidMap_night.pickle", "rb") as fr2:
                radioMidMap_result = pickle.load(fr2)

            print(radioMap_result)
            print(radioMidMap_result)
            
            # values를 통한 거리값 저장
            for keys, values in radioMidMap_result.items():

                fingerDistance[keys] = q.eucliDis(values, fingerPrintRss)

            print('DisList:', fingerDistance)

            min_result = min(fingerDistance.values())

            # 결과값 출력
            for key, values in fingerDistance.items():
                # print('dis:',key,values)
                if values == min_result:
                    print('result:', addr, key, values)
                    
        #knn mode
        else:
            print('knn mode')

            with open("radioMap_night.pickle", "rb") as fr:
                radioMap_result = pickle.load(fr)

            with open("radioMidMap_night.pickle", "rb") as fr2:
                radioMidMap_result = pickle.load(fr2)

            print(radioMap_result)
            print(radioMidMap_result)

            for keys, values in radioMidMap_result.items():
                print('values:, ',len(values),values)
                print('finger',len(fingerPrintRss),fingerPrintRss)
                fingerDistance[keys] = q.eucliDis(values, fingerPrintRss)

            print('DisList:', fingerDistance)

            k_euc_dist=[]
            k_euc_dist_coordinate=[]

            for i in range(param_K):

                min_result = min(fingerDistance.values())
                k_euc_dist.append(min_result)
                for key, values in fingerDistance.items():
                # print('dis:',key,values)
                    if values == min_result:
                        print('result:', addr, key, values)
                        k_euc_dist_coordinate.append(coordinate.gridCoordinates[key[0]-1])
                        fingerDistance[key]=999


            userLocationX = 0
            userLocationY = 0

            if param_K == 1:
                # K = 1 이면, fingerprint 랑 같다
                userLocationX = k_euc_dist_coordinate[0].x
                userLocationY = k_euc_dist_coordinate[0].y
            else:
                # 여기 나오는 내용은, 지난번 카톡으로 전달한 KNN 수식을
                # 코드로 구현한 것임
                denominator = 0  # 분모에 들어갈, 가중치값의 합
                weights = []  # 분자에 들어갈 가중치값
                for i in range(param_K):
                    denominator += (1.0 / k_euc_dist[i])
                    weights.append(1.0 / k_euc_dist[i])
                # 이제는 사용자 위치를 예측
                for i in range(param_K):
                    userLocationX += ((1.0/denominator) * weights[i] * k_euc_dist_coordinate[i].x)
                    userLocationY += ((1.0/denominator) * weights[i] * k_euc_dist_coordinate[i].y)

            print('X : ',userLocationX,'Y: ',userLocationY)

            #user_id_temp = "1"
            print("좌표 업데이트")
            draw(1, user_count, userLocationX, userLocationY)

    elif data[0]==2:
        print('ap들이 보내는거',data)


def socket_threaded(client_socket,addr,user_count):
    print('connected by: ',addr[0],':',addr[1])

    while True:
        try:
            recv_data=client_socket.recv(1024)
            recv_data=recv_data.decode()

            if not recv_data:
                print('not data')
                return 0
            else:
                print(recv_data)
                data=recv_data.split(':')
                print('data length: ',len(data))

                if len(data) ==317:

                    if int(data[0]) != 2:
                        data=list(map(int,data))
                    tracking(data,addr[0],user_count)
                else:
                    print('317사이즈가 아닙니다.')
                    continue

        except ConnectionResetError as e:
            print(e)
            break

    client_socket.close()

if __name__=="__main__":

    host = ''
    port = 9999

    q = Laptop()

    #socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(7)

    while True:

        user_count+=1
        client_socket, addr = server_socket.accept()
        print('client socket:',addr, user_count)
        start_new_thread(socket_threaded, (client_socket, addr, user_count))

    server_socket.close()
