import matplotlib.pyplot as plt
import currentlocation as loc
import time
import threading

#written by 김보라_2020
GUI_FILE_NAME = "draw.txt"

im = plt.imread("MapDisplay.png")
#implot = plt.imshow(im)
plt.imshow(im)

MODE_FINGERPRINT = 1
MODE_KNN = 2
MODE_TRILATERATION = 3

"""
삼변측량을 하면, 지정된 영역 내에서의 위치를 알려 주니까,
해당 영역의 (0,0)에 해당하는 현실 위치를 다시 더해줘야
전체 지도 내에서의 위치를 알 수 있다.
이 때 더해주는 값이 아래와 같다.
"""
TRI_REALx_OFFSET = 14.7
TRI_REALy_OFFSET = 5.7
cnt = 0

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
        print(loc.aGUILocation)
    elif id == 2:
        loc.bGUILocation = [gui_x, gui_y]
        # print("bLocation을 업데이트 합니다.")
        print(loc.bGUILocation)
    else:
        assert False, "잘못된 ID 값입니다."

    plt.plot(loc.aGUILocation[0], loc.aGUILocation[1], 'ro', alpha=0.75)
    # print("plot:")
    # print(loc.aGUILocation)
    plt.plot(loc.bGUILocation[0], loc.bGUILocation[1], 'bo', alpha=0.75)
    # print("plot:")
    # print(loc.bGUILocation)

def GUI():
    global cnt
    GUI_FILE_NAME = "draw.txt"

    time.sleep(4)
    while True:
        f = open(GUI_FILE_NAME, 'r')
        line = f.readline()
        line = line.strip()
        data = str(line).split(':')
        mode = int(data[0])
        user_id = int(data[1])
        REALx = float(data[2])
        REALy = float(data[3])
        f.close()

        func(mode, user_id, REALx, REALy)

        if cnt != 0:
            print('show block')
            plt.show(block=False)
        time.sleep(0.2)
        cnt += 1

func(1, 1, 0, 0)
func(1, 2, 0, 0)

t = threading.Thread(target=GUI)
t.start()

#while True:
#    try:
plt.show()
#        time.sleep(1)

#    except KeyboardInterrupt:
#        break
#    except Exception as e:
#        print(e)
#        break

#print('end')
"""

func(1, 1, 29, 14.4)
print("1번 좌표 업데이트")

func(1, 2, 60.5, 17)
print("2번 좌표 업데이트")

func(1, 1, 39, 14.4)
print("1번 좌표 업데이트")

func(1, 1, 35, 14.5)
print("1번 좌표 업데이트")

func(1, 1, 32, 18.4)
print("1번 좌표 업데이트")

func(3, 2, 0, 0)
print("2번 좌표 업데이트")

"""