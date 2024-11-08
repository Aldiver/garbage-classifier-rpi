import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1  # Adjust gain as needed

# IR sensors
sensor1 = AnalogIn(ads, ADS.P0)  # A0
sensor2 = AnalogIn(ads, ADS.P1)  # A1
sensor3 = AnalogIn(ads, ADS.P2)  # A2

def is_object_close(sensor, threshold=0.3):
    """Returns True if an object is close, based on voltage."""
    voltage = sensor.voltage
    return voltage >= threshold  # Adjust threshold based on sensor's output for 1ft proximity
