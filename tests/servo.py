import time
from adafruit_servokit import ServoKit

# Set up the ServoKit instance with 16 channels (this supports up to 16 servos)
kit = ServoKit(channels=16)

try:
    while True:
        # Move servos to 0 degrees
        print("Moving servos to 0 degrees...")
        kit.servo[0].angle = 0
        kit.servo[4].angle = 0
        kit.servo[8].angle = 0
        time.sleep(1)

        # Move servos to 90 degrees
        print("Moving servos to 90 degrees...")
        kit.servo[0].angle = 90
        kit.servo[4].angle = 90
        kit.servo[8].angle = 90
        time.sleep(1)

        # Move servos to 180 degrees
        print("Moving servos to 180 degrees...")
        kit.servo[0].angle = 180
        kit.servo[4].angle = 180
        kit.servo[8].angle = 180
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped")
