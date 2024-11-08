import board
import busio
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Set frequency to 50Hz for servos

def set_servo_angle(channel, angle):
    pulse_min = 1000
    pulse_max = 2000
    pulse_width = pulse_min + (angle / 180.0) * (pulse_max - pulse_min)
    pulse_length = int(pulse_width / 1000000 * pca.frequency * 4096)
    pca.channels[channel].duty_cycle = pulse_length

def move_servo(channel, angle):
    set_servo_angle(channel, angle)
