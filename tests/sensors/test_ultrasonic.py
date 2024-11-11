from gpiozero import DistanceSensor
import time

# Define the pins for the sensor
sensor_1 = DistanceSensor(echo=5, trigger=17)
sensor_2 = DistanceSensor(echo=6, trigger=27)
sensor_3 = DistanceSensor(echo=13, trigger=22)

# Use a list to manage sensors
sensors = [sensor_1, sensor_2, sensor_3]

# Measure distance continuously
try:
    while True:
        for i, sensor in enumerate(sensors):
            distance = sensor.distance * 100  # Convert to cm
            print(f"Distance from sensor {i+1}: {distance:.2f} cm")
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by user")
