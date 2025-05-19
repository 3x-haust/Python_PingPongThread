from example_base import GetParentPath
from pingpong import PingPongThread
import keyboard # keyboard==0.13.4
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 그래프 초기화
plt.style.use('seaborn')
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title('온도 센서 모니터링')
ax.set_xlabel('시간 (초)')
ax.set_ylabel('온도 (°C)')
ax.grid(True)

# 데이터 저장용 리스트
times = []
temperatures = []
start_time = time.time()

# PingPong 쓰레드 시작
PingPongThreadInstance = PingPongThread(number=1) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

cube_ID = 1 # 큐브 번호

# 그래프 업데이트 함수
def update(frame):
    if not keyboard.is_pressed("q") and PingPongThreadInstance.play_once_full_connect():
        PingPongThreadInstance.receive_sensor_data(cube_ID, method="periodic", period=0.1)
        temp = PingPongThreadInstance.get_current_temperature(cube_ID)
        current_time = time.time() - start_time
        
        times.append(current_time)
        temperatures.append(temp)
        
        # 최근 30초 데이터만 표시
        if len(times) > 300:
            times.pop(0)
            temperatures.pop(0)
        
        ax.clear()
        ax.plot(times, temperatures, 'b-')
        ax.set_title(f'온도 센서 모니터링 (현재: {temp:.1f}°C)')
        ax.set_xlabel('시간 (초)')
        ax.set_ylabel('온도 (°C)')
        ax.grid(True)
        
        # Y축 범위를 동적으로 조정
        if temperatures:
            min_temp = min(temperatures) - 2
            max_temp = max(temperatures) + 2
            ax.set_ylim(min_temp, max_temp)
        
        # X축 범위를 동적으로 조정
        if times:
            if times[-1] > 30:
                ax.set_xlim(times[-1] - 30, times[-1])
            else:
                ax.set_xlim(0, 30)
    
    return ax,

try:
    # 애니메이션 시작
    ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    PingPongThreadInstance.end() # 쓰레드 종료
    print("프로그램 종료")
