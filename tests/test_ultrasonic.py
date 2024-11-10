from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Specify the pigpio factory for more accurate readings
factory = PiGPIOFactory()

# Define the sensors using pigpio as the factory
sensors = [
    DistanceSensor(echo=5, trigger=17, pin_factory=factory),
    DistanceSensor(echo=6, trigger=27, pin_factory=factory),
    DistanceSensor(echo=13, trigger=22, pin_factory=factory),
]

try:
    while True:
        for i, sensor in enumerate(sensors):
            distance = sensor.distance * 100  # Convert from meters to cm
            print(f"Distance from sensor {i+1}: {round(distance, 2)} cm")
        sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by user")
