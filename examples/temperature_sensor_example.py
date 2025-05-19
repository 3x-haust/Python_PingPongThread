from pingpong import PingPongThread
import time
import keyboard

pingpong = PingPongThread(number=1, group_id=4)
pingpong.start()
pingpong.wait_until_full_connect()

cube_ID = 1

pingpong.run_motor(cube_ID, 30)

pingpong.receive_sensor_data(cube_ID=cube_ID, method="periodic", period=0.5)
while not pingpong.get_current_button(cube_ID) == 1: 
    temp = pingpong.get_current_temperature(cube_ID)
    print(f"Current temperature: {temp}°C")
    time.sleep(0.5)
pingpong.stop_sensor_data(cube_ID)
print("Sensor data stopped.")
pingpong.end()