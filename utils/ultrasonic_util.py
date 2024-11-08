import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

sensors = [
    {"TRIG": 17, "ECHO": 5},
    {"TRIG": 27, "ECHO": 6},
    {"TRIG": 22, "ECHO": 13},
]

for sensor in sensors:
    GPIO.setup(sensor["TRIG"], GPIO.OUT)
    GPIO.setup(sensor["ECHO"], GPIO.IN)

def get_distance(sensor):
    GPIO.output(sensor["TRIG"], True)
    time.sleep(0.00001)
    GPIO.output(sensor["TRIG"], False)

    start_time = time.time()
    while GPIO.input(sensor["ECHO"]) == 0:
        start_time = time.time()
    while GPIO.input(sensor["ECHO"]) == 1:
        stop_time = time.time()

    pulse_duration = stop_time - start_time
    distance = pulse_duration * 17150
    return round(distance, 2)

def calculate_bin_level(distance, max_distance=91.44):  # 3 feet in cm
    return max(0, min(100, (1 - distance / max_distance) * 100))
