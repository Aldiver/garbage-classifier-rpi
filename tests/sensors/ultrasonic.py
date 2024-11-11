import RPi.GPIO as GPIO
import time

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for the TRIG and ECHO of each sensor
sensors = [
    {"TRIG": 17, "ECHO": 5},
    {"TRIG": 27, "ECHO": 6},
    {"TRIG": 22, "ECHO": 13},
]

# Set up each sensor
for sensor in sensors:
    GPIO.setup(sensor["TRIG"], GPIO.OUT)
    GPIO.setup(sensor["ECHO"], GPIO.IN)

def measure_distance(sensor):
    # Set TRIG high and then low
    GPIO.output(sensor["TRIG"], True)
    time.sleep(0.00001)
    GPIO.output(sensor["TRIG"], False)

    # Measure ECHO pulse duration
    start_time = time.time()
    while GPIO.input(sensor["ECHO"]) == 0:
        start_time = time.time()
    while GPIO.input(sensor["ECHO"]) == 1:
        stop_time = time.time()

    # Calculate distance based on pulse duration
    pulse_duration = stop_time - start_time
    distance = pulse_duration * 17150  # Speed of sound is ~34300 cm/s, divided by 2 for round-trip
    return round(distance, 2)

try:
    while True:
        for i, sensor in enumerate(sensors):
            distance = measure_distance(sensor)
            print(f"Distance from sensor {i+1}: {distance} cm")
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
