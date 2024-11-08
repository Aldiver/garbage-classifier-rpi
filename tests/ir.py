import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Set up I2C bus and ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x4A)

# Configure ADS1115 with default gain (adjust if needed)
ads.gain = 1

# Create single-ended input on channels A0, A1, and A2
sensor1 = AnalogIn(ads, ADS.P0)  # A0
sensor2 = AnalogIn(ads, ADS.P1)  # A1
sensor3 = AnalogIn(ads, ADS.P2)  # A2

# Function to read sensor data
def read_sensors():
    # Read each sensor's voltage and print values
    print("Sensor 1 Voltage (A0): {:.2f} V".format(sensor1.voltage))
    print("Sensor 2 Voltage (A1): {:.2f} V".format(sensor2.voltage))
    print("Sensor 3 Voltage (A2): {:.2f} V".format(sensor3.voltage))
    print("-" * 30)

try:
    # Continuously read and print sensor data
    while True:
        read_sensors()
        time.sleep(1)  # Adjust delay as needed
except KeyboardInterrupt:
    print("Exiting program")
