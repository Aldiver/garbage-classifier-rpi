import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Define the sensors and their TRIG/ECHO pins
ultrasonic_sensors = [
    {"TRIG": 17, "ECHO": 5},
    {"TRIG": 27, "ECHO": 6},
    {"TRIG": 22, "ECHO": 13},
]

# Set up each sensor
for sensor in ultrasonic_sensors:
    GPIO.setup(sensor["TRIG"], GPIO.OUT)
    GPIO.setup(sensor["ECHO"], GPIO.IN)

def get_distance(sensor):
    # Send trigger pulse
    GPIO.output(sensor["TRIG"], True)
    time.sleep(0.00001)  # 10us pulse
    GPIO.output(sensor["TRIG"], False)

    # Measure pulse duration
    start_time = time.time()
    while GPIO.input(sensor["ECHO"]) == 0:
        start_time = time.time()
    while GPIO.input(sensor["ECHO"]) == 1:
        stop_time = time.time()

    # Calculate distance based on pulse duration
    pulse_duration = stop_time - start_time
    distance = pulse_duration * 17150  # Speed of sound ~34300 cm/s, divided by 2 for round-trip
    return round(distance, 2)

# Function to calculate bin level based on the distance measurement
def calculate_bin_level(distance, max_distance=35):  # Max distance set to 35 cm
    return max(0, min(100, (1 - distance / max_distance) * 100))
