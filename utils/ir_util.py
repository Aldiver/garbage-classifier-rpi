import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c, address=0x4A)  # Set the address to 0x4A
ads.gain = 1  # Adjust gain as needed

# IR sensors
sensor1 = AnalogIn(ads, ADS.P0)  # A0
sensor2 = AnalogIn(ads, ADS.P1)  # A1
sensor3 = AnalogIn(ads, ADS.P2)  # A2

def get_sensor_value(sensor, threshold=0.5):
    return sensor.voltage
