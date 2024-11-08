import time
import board
import busio
from adafruit_pca9685 import PCA9685

# Set up I2C bus and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Set frequency to 50Hz for servos

# Helper function to set servo angle
def set_servo_angle(channel, angle):
    # Map angle (0 to 180) to PWM pulse width (servo-specific)
    pulse_min = 1000  # Adjust these values based on servo specifications
    pulse_max = 2000
    pulse_width = pulse_min + (angle / 180.0) * (pulse_max - pulse_min)
    pulse_length = int(pulse_width / 1000000 * pca.frequency * 4096)
    pca.channels[channel].duty_cycle = pulse_length

try:
    while True:
        # Move servos to 0 degrees
        set_servo_angle(0, 0)
        set_servo_angle(4, 0)
        set_servo_angle(8, 0)
        time.sleep(1)

        # Move servos to 90 degrees
        set_servo_angle(0, 90)
        set_servo_angle(4, 90)
        set_servo_angle(8, 90)
        time.sleep(1)

        # Move servos to 180 degrees
        set_servo_angle(0, 180)
        set_servo_angle(4, 180)
        set_servo_angle(8, 180)
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped")
finally:
    pca.deinit()
