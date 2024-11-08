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

# Function to convert voltage to distance using polynomial formula
def voltage_to_distance(voltage):
    # Apply the polynomial conversion formula
    dist = (16.2537 * voltage**4 - 129.893 * voltage**3 +
            382.268 * voltage**2 - 512.611 * voltage + 301.439)
    return dist

# Function to read sensor data and convert to distance
def read_sensors():
    # Read each sensor's voltage
    voltage1 = sensor1.voltage
    voltage2 = sensor2.voltage
    voltage3 = sensor3.voltage

    # Convert voltage to distance
    distance1 = voltage_to_distance(voltage1)
    distance2 = voltage_to_distance(voltage2)
    distance3 = voltage_to_distance(voltage3)

    # Print distance values
    print("Sensor 1 Distance (A0): {:.2f} m".format(distance1))
    print("Sensor 2 Distance (A1): {:.2f} m".format(distance2))
    print("Sensor 3 Distance (A2): {:.2f} m".format(distance3))
    print("-" * 30)

try:
    # Continuously read and print sensor data
    while True:
        read_sensors()
        time.sleep(1)  # Adjust delay as needed
except KeyboardInterrupt:
    print("Exiting program")
