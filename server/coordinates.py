
# 각 grid의 좌표값을 저장하기 위한 클래스
class GridCoordinate:
    x = 0
    y = 0

    def __init__(self, x, y):
        assert x >= 0 and y >= 0, "좌표값은 음수가 될 수 없습니다."
        self.x = x
        self.y = y

gridCoordinates = []  # 각 grid의 현실 위치 (x,y) 를 저장한 리스트
gridCoordinates.append(GridCoordinate(29, 14.4))
gridCoordinates.append(GridCoordinate(33.75, 14.4))
gridCoordinates.append(GridCoordinate(36.9, 14.4))
gridCoordinates.append(GridCoordinate(42.5, 14.4))
gridCoordinates.append(GridCoordinate(47, 14.4))
gridCoordinates.append(GridCoordinate(51.3, 14.4))
gridCoordinates.append(GridCoordinate(54.75, 14.4))


gridCoordinates.append(GridCoordinate(60.5, 12.4))
gridCoordinates.append(GridCoordinate(60.5, 17))
gridCoordinates.append(GridCoordinate(66.25, 14.4))
gridCoordinates.append(GridCoordinate(69.5, 14.4))
gridCoordinates.append(GridCoordinate(74, 14.4))
gridCoordinates.append(GridCoordinate(78.3, 14.4))
gridCoordinates.append(GridCoordinate(82.5, 14.4))

gridCoordinates.append(GridCoordinate(87.2, 14.4))
gridCoordinates.append(GridCoordinate(91.5, 14.4))
gridCoordinates.append(GridCoordinate(96, 14.4))
gridCoordinates.append(GridCoordinate(100.6, 14.4))
gridCoordinates.append(GridCoordinate(104.3, 14.4))
gridCoordinates.append(GridCoordinate(109.5, 14.4))
gridCoordinates.append(GridCoordinate(112.6, 14.4))
gridCoordinates.append(GridCoordinate(119.9, 14.4))
gridCoordinates.append(GridCoordinate(127.6, 17))
gridCoordinates.append(GridCoordinate(133.5, 14.4))
gridCoordinates.append(GridCoordinate(141.7, 14.4))
gridCoordinates.append(GridCoordinate(151, 14.4))
gridCoordinates.append(GridCoordinate(135.15, 21.7))
gridCoordinates.append(GridCoordinate(135.15, 28.2))
