# Hallym_Capstone_HAS
[2020_1_capstone_ HAS(하스) 중간보고서.pdf](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853309/2020_1_capstone_.HAS.pdf)

빅데이터 캡스톤 - 자동 측위 및 식별 시스템 기반의 실내 위치추적 기술 개발

<img src = "https://user-images.githubusercontent.com/48000920/126438440-093d46c4-b016-403d-88a1-59d161f5cf5c.png" width="50%" height="50%">

# 개요
   * ns-3 시뮬레이터와 라즈베리파이를 통해 실내 위치 추적 기술을 개발한다. 
  
   * 최종 목표는 한림대학교 공학관의 실내 위치 추적을 하는 것으로, 최종 구현 결과물의 정확도와 안정성을 높이기 위해 RSS(Received Signal Strength)기반의 fingerprint 기법을 이용한다.

# 팀 구성 및 역할분담
  * 지도교수 : 김태운 교수님
  * 홍연경 : 팀장 / Raspberry Pi 실내 통신환경 구축 / GUI 프로그램 구현
  * 김윤하 : 예산관리 / Rasberry Pi 실내 통신환경 구축 / 데이터 수집 및 분석
  * 김진아 : NS-3 시뮬레이션 무선 네트워크 환경 구축 / 데이터 수집 및 분석 / 핑거프린트 알고리즘 구현
  * 김보라 : 깃헙관리 / NS-3 시뮬레이션 무선 네트워크 환경 데이터 분석 / 삼변측량 알고리즘 구현

# 개발 도구
  * python
  * Raspberry Pi
  * ns-3

# 개발 목표
  * 자동 측위 및 식별 시스템 기반의 실내 위치추적 기술 개발한다.
  * 복잡한 내부 구조 및 시설물로 인해 GPS 정확도가 현저히 떨어지는 실내 환경에서 높은 정확도의 측위 기술 및 객체(예: 사람, 사물 등) 인식 기술을 개발한다.
  * 오픈소스 소프트웨어인 ns-3를 사용하여 시뮬레이션 환경에서 측위 알고리즘을 구현하고 알고리즘 성능을 개선한다.
  * 라즈베리 파이를 이용해 실내 환경에서 높은 정확도의 측위 시스템을 구현한다.
  * 객체의 위치를 실시간으로 나타내는 GUI프로그램을 개발한다.
  
# 활용방안
  * 구현한 공학관 위치추적 프로그램은 강의실 찾기 서비스 /전자출결 출석 후 수업 미참여(일명 출튀) 학생 구분 서비스 등에 활용 가능
  * gps를 이용한 건물 내의 길 찾기 서비스
  * 건물 내의 비상구를 쉽게 알 수 있는 긴급구조용 위치 서비스
  * 실내 공간 정보 검색, 실내 로봇 응용, 실내 공간 관리, 실내 공간 기반 게임 등 실내 환경에 다양한 서비스를 제공

# 프로젝트 구성도

<img src = "https://user-images.githubusercontent.com/48000920/126439285-e2d58b73-e45a-4fbe-a47c-da13747d8b9e.png" width="70%" height="70%">

# NS-3

  1. [ns-3 설치방법 설명서](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853178/ns-3.pdf)
  2. 거리에 따른 RSS 수집
  
    - RPI 단말기가 동일한 tx power로 데이터신호를 전송하도록 설정
    - 두대의 RPI 장비는 일정간격으로 상대발 단말기로 부터 전송한 신호의 RSS신호를 저장
    - 두대의 RPi 장비간 거리가 멀어짐에 따라 RSS 값이 작아지는 것을 확인
    - 거리를 x축으로, 거리에 따른 RSS값을 y축으로 그래프 표현
  
  <img src = "https://user-images.githubusercontent.com/48000920/126439824-fcc1e344-25af-4c39-8cde-f4cf9e047e15.png" width="70%" height="70%">

  <img src = "https://user-images.githubusercontent.com/48000920/126439841-1cdba6d9-fb32-4129-9856-2bb02178cd6c.png" width="70%" height="70%">
  
  3. Scenario -1
    
    -사각형 영역. 각각의 모서리에 1개의 노드 배치. 화면 중앙에 노드 1개 배치
    -5개의 노드가 모두 주기적으로 broadcasting
    -하나의 노드가 broadcasting 하면, 다른 4개 노드는 해당 노드의 ID값 (id, ip, mac 등, 해당 노드를 유일하게 구분할 수 있는 어떤 데이터든 관계 없음) 및 RSS값을 log/trace에 기록
    
  4. Scenario -2 : 화면 중앙에 있는 노드를 이동, 이 외의 조건은 Scenario-1과 동일
  
  5. 결과 : NS-3를 통해 fingerprint를 통한 위치 추적이 가능함을 확인

# RPi
  * [wavemon, iwconfig을 사용해 RSS값 측정](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853207/wavemon.iwconfig.RSS.pdf)
  * [실내에서 sender/receiver간 거리에 따른 RSS값 변화 측정 그래프](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853208/RSS.xlsx)

  ![image](https://user-images.githubusercontent.com/48000920/126440450-368dd795-8199-4794-ae39-2b8f48f256c3.png)

  * [위치측정을 위해 Rpi를 AP모드로 변경](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853209/AP.pdf)

# 실내 위치 측정 기법

  * 삼변측량
    
    > 삼각측량과 이름이 비슷하지만, 삼각측량은 거리와 각도를 가지고 위치를 추적하고, 삼변측량은 거리만 가지고 위치 추적. 3개 이상의 신호발생기에서 발생하는 신호강도(rss)를 이용하여 각각의 신호발생기 교차범위의 위치가 사용자의 위치라는 이론. fingerprint에 비해 정확한 위치 측정 가능하지만, ap위치가 변하거나 지형지물에 따라 신호강도가 달라져 예외사항이 발생한다.

  * fingerprint (적용방법)
  
    >사전에 격자형태로 신호세기를 저장한 뒤, 사용자가 자신주변의 신호를 모아 위치를 요청하면 서버는 기록된 신호세기와 요청 신호세기를 비교하여 위치를 측정하는 형태. fingerprint를 수행하기위해서는 사전수집단계, 측위단계 2단계 필요. 사전수집단계에서 데이터 미리 측정해야 한다는 점과 실내환경이 변경되면 전파맵의 보정이 필요하다는 점이 특징이다.

# Radio map 확보
  * 테스트 공간이 되는 공학관 1층 실내 내부의 공간을 다수의 grid로 분할하고, 각 grid의 셀에서 측정한 ap들의 rss값을 저장하는 Radio Map을 확보한다.

# AP 수집단계
  
  * ap 수집 위치

  ![image](https://user-images.githubusercontent.com/48000920/126440796-340a0f5c-f707-4ba4-9092-9df43bc39670.png)
  ![image](https://user-images.githubusercontent.com/48000920/126440821-faa54c5d-bc70-4fa0-849f-ae221a914d0b.png)
  ![image](https://user-images.githubusercontent.com/48000920/126440851-7770e438-1529-4378-a4d5-2fa396ac944d.png)
  
  * 라즈베리파이에서 ap를 수집할 위치를 고려하여 해당 위치에서 ap의 MAC address정보를 획득하여 파일 형태로 저장한다. 파일 중 한 개의 내부 상태는 다음과 같다.                               
  <img src = "https://user-images.githubusercontent.com/48000920/126440970-3e302250-c10b-4159-862f-1de3b43b2211.png" width="30%" height="30%">
  
# 공학관 도면  

  <img src = "https://user-images.githubusercontent.com/48000920/126441676-c36bbbcb-d744-4632-9dea-db0d645ebb3c.png" width="70%" height="70%">
  
  위의 도면을 아래의 사진과 같이 나누었다.
  <img src = "https://user-images.githubusercontent.com/48000920/126441860-e66740c5-751f-4963-8b0e-4bdf68a8220a.png" width="70%" height="70%">
  
# 사전 작업 모드
  * 사용자 라즈베리파이는 특정 그리드에서 주변의 AP를 읽어 5번 서버에게 전송한다.
  * TYPE:그리드X좌표:그리드Y좌표:rss값... 형태로 서버에 전송을 하며 서버에서는 TYPE이 3이면 사전작업모드이고 해당 그리드 좌표에서 받은 5번의 데이터 중에서 middle값을 실제 라디오 맵으로 선택한다. 서버가 받은 내용은 다음과 같다.
    <img src = "https://user-images.githubusercontent.com/48000920/126442011-0fd046db-0b19-4e7c-9251-39c22ac8f4e4.png" width="70%" height="70%">
  * 그리드는 (1.0) ~ (28.0)으로 총 28개의 그리드로 나누었고 (28.0)에서 5번의 수집을 끝내면 편의성을 위해 파일로 저장시킨다.
  
# 실시간 위치 측정
  * 사용자 라즈베리파이는 TYPE 1로 변경하여 서버에게 실시간으로 전송한다.
  * 서버로 TYPE이 1이므로 위치 측정을 위해 저장된 파일을 불러와 비교하며 해당 rss값과 모든 grid의 rss값을 비교하여 가장 작은 유클리디안 거리를 가지는 grid를 찾아낸다.
  * 서버는 해당 grid를 사용자의 위치라고 예측한다.
  * 라즈베리파이는 다음과 같이 iwlist를 이용하여 MAC Address와 RSS값을 찾는다.
  * 서버에게 보내는 형태는 다음과 같다
  <img src = "https://user-images.githubusercontent.com/48000920/126442169-73aad20e-da1d-40c1-a2e3-7ae112513a6d.png" width="70%" height="70%">
  
# GUI 표시
  * 사용자(라즈베리파이)로부터 받은 데이터(rss list)가 gird로 설정한 (16, 0)에서 가장 작은 값을 가지므로 사용자의 위치가 (16, 0) grid인 곳에 빨간색 점을 찍는다.
  * matplotlib.pyplot 모듈을 이용하여 GUI를 표시한다.

# 결과
<img src = "https://user-images.githubusercontent.com/48000920/126442286-6e25550f-6907-4d2e-90af-6a2f62b4d850.png" width="70%" height="70%">
<img src = "https://user-images.githubusercontent.com/48000920/126442304-404d731b-eb14-49ec-9660-bd6541b18f9f.png" width="70%" height="70%">

# 시연영상
  
  1. 공학관 내부의 RSS 데이터 수집 및 Radio map 생성 - https://youtu.be/WFhvA-IQb90
  2. 유저가 1일때 시연 동영상 - https://youtu.be/KHb8cxlXIGA
  3. 유저가 2일때 시연 동영상 - https://youtu.be/umETXmIHcN8

# 보고서
  * [중간보고서](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853310/2020_1_capstone_.HAS.pdf)
  * [최종보고서](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853311/2020-1.-.HAS.pdf)

# 회의록
  * [2020-1학기 캡스톤디자인 200317 회의록](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853328/2020-1.200317.pdf)
  * [2020-1학기 캡스톤디자인 200324 회의록](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853330/2020-1.200324.pdf)
  * [2020-1학기 캡스톤디자인 200331 회의록](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853332/2020-1.200331.pdf)
  * [2020-1학기 캡스톤디자인 200407 회의록](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853333/2020-1.200407.pdf)
  * [2020-1학기 캡스톤디자인 200414 회의록](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853334/2020-1.200414.pdf)
  * [2020-1학기 캡스톤디자인 200421 회의록](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853335/2020-1.200421.pdf)
  * [2020-1학기 캡스톤디자인 200428 회의록](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853336/2020-1.200428.pdf)
  * [2020-1학기 캡스톤디자인 200512 회의록](https://drive.google.com/file/d/1tFszON3l0FZqbq4PcgkeHNDcu8kwllhQ/view?usp=sharing)
  * [2020-1학기 캡스톤디자인 200519 회의록](https://github.com/kja8147/Hallym_Capstone_HAS/files/6853337/2020-1.200519.pdf)

