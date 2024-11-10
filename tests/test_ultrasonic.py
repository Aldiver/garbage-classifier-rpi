from gpiozero import DistanceSensor
from time import sleep

# Define GPIO pins for the TRIG and ECHO of each sensor
sensors = [
    DistanceSensor(echo=5, trigger=17),
    DistanceSensor(echo=6, trigger=27),
    DistanceSensor(echo=13, trigger=22),
]

try:
    while True:
        for i, sensor in enumerate(sensors):
            distance = sensor.distance * 100  # Convert from meters to cm
            print(f"Distance from sensor {i+1}: {round(distance, 2)} cm")
        sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by user")
