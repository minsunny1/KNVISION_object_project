import serial   # for 시리얼 통신
import pygame   # for 키보드 방향키 제어
import time     # for 시간 기반 ptz 제어
import sys      # for ptz 제어 종료

ser = serial.Serial(port='COM5', baudrate=9600, timeout=1)  # Serial 통신위한 객체 생성
                                                            # port = 시리얼 통신에 사용하는 포트
                                                            # baudrate = 사용할 통신 속도
                                                            # timeout = 데이터를 읽어오기 위해 기다리는 최대 시간 (초단위)


def move_left():
    pan_left = b'\xFF\x01\x00\x04\x3F\x00\x44'              # pelco - D 프로토콜에서 pan을 left로 이동시키는 패킷
    ser.write(pan_left)                                     # 해당 패킷 전송


def move_right():
    pan_right = b'\xFF\x01\x00\x02\x20\x00\x23'             # pelco - D 프로토콜에서 pan을 right로 이동시키는 패킷
    ser.write(pan_right)                                    # 해당 패킷 전송


def move_up():
    tilt_up = b'\xFF\x01\x00\x08\x00\x3F\x48'               # pelco - D 프로토콜에서 tilt를 위로 이동시키는 패킷
    ser.write(tilt_up)                                      # 해당 패킷 전송


def move_down():
    tilt_down = b'\xFF\x01\x00\x10\x00\x20\x31'             # pelco - D 프로토콜에서 tilt를 아래로 이동시키는 패킷
    ser.write(tilt_down)                                    # 해당 패킷 전송


def stop():
    stop = b'\xFF\x01\x00\x00\x00\x00\x01'                  # pelco - D 프로토콜에서 이동을 정지시키는 패킷
    ser.write(stop)                                         # 헤딩 패킷 전송


def init():
    '''
    PTZ 모터를 초기 위치로 이동 시키는 함수
    초기 PTZ 모터에 전원 연결시 초기 동작으로 인해 가동범위중 LEFT 방향의 끝에 PTZ 모터가 위치함
    -> 좌우로 원활하게 동작할 수 있도록 right 방향으로 일정 방향 이동시킴
    :return: None
    '''
    move_right()
    time.sleep(25)
    stop()



if __name__ == '__main__':
    pygame.init()       # 키보드 방향키 제어가 가능하도록 pygame 객체 초기화
    screen = pygame.display.set_mode((200, 200))    # 키보드 제어를 위한 pygame 화면을 display
                                                    # 해당 화면을 display하지 않으면 키보드 입력시 스트립트에 입력이 반영됨
                                                    # -> 키보드 입력이 제어를 위한 입력으로 사용되지 못함

    init()  # PTZ 모터를 초기 위치로 이동
    while True:
        for event in pygame.event.get():    # 키보드 입력을 받아옴
            if event.type == pygame.KEYDOWN:        # 키보드가 늘렸을 때
                if event.key == pygame.K_UP:            # 누른 값이 up 방향키일 때
                    move_up()                           # PTZ 모터 위로 이동
                elif event.key == pygame.K_DOWN:        # 누른 값이 down 방항키일 떄
                    move_down()                         # PTZ 모터 아래로 이동
                elif event.key == pygame.K_RIGHT:       # 누른 값이 right 방향키일 떄
                    move_right()                        # PTZ 모터 우로 이동
                elif event.key == pygame.K_LEFT:        # 누른 값이 left 방향키일 때
                    move_left()                         # PTZ 모터 좌로 이동
                elif event.key == pygame.K_q:           # 누른 값이 Q일 때
                    ser.close()                         # 시리얼 포트 자원 해제
                    pygame.quit()                       # pygame 자원 해제
                    sys.exit()                          # 프로그램 종료

            elif event.type == pygame.KEYUP:       # 키보드에서 손을 뗐을 떄
                stop()                             # 이동 종료

        time.sleep(0.1) # 키보드 입력을 받은 후 0.1초 대기

ser.close() # 시리얼 포트 자원 해제
