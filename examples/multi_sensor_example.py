from example_base import GetParentPath
from pingpong import PingPongThread
import keyboard # keyboard==0.13.4
import time

PingPongThreadInstance = PingPongThread(number=1) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

cube_ID = 1 # 큐브 번호

print("여러 센서 데이터를 동시에 읽는 예제")
print("q 키를 눌러 종료할 수 있습니다.")

try:
    while not keyboard.is_pressed("q"): # q가 눌리기 전까지 쓰레드 유지
        if PingPongThreadInstance.play_once_full_connect(): # 연결 되어있는 동안, 한 번만 실행
            # 센서 데이터 수신 활성화
            PingPongThreadInstance.receive_sensor_data(cube_ID, method="periodic", period=0.1)
            
            # 여러 센서 데이터 읽기
            temp = PingPongThreadInstance.get_current_temperature(cube_ID)
            prox = PingPongThreadInstance.get_current_proxy(cube_ID)
            gyro = PingPongThreadInstance.get_current_gyro(cube_ID)
            button = PingPongThreadInstance.get_current_button(cube_ID)
            
            # 결과 출력
            print(f"온도: {temp:.1f}°C | 근접: {prox} | 자이로: {gyro} | 버튼: {button}")
            
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    # 센서 데이터 수신 비활성화
    PingPongThreadInstance.stop_sensor_data(cube_ID)
    # 쓰레드 종료
    PingPongThreadInstance.end()
    print("프로그램 종료")
