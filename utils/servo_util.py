import time
from adafruit_servokit import ServoKit

# Set up the ServoKit instance with 16 channels (this supports up to 16 servos)
kit = ServoKit(channels=16)

# Helper function to set servo angle using ServoKit
def set_servo_angle(channel, angle):
    # Use ServoKit to set the servo angle
    kit.servo[channel].angle = angle
    print(f"Servo {channel} set to {angle} degrees")

def move_servo(channel, angle):
    set_servo_angle(channel, angle)
