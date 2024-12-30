import time
from moon_servo.motor import MoonServoMotor
from moon_servo import MoonServoMotor

# Initialize the motor with the desired parameters
motor1 = MoonServoMotor(port='/dev/ttyUSB0', baudrate=115200, base_address=0)
motor2 = MoonServoMotor(port='/dev/ttyUSB0', baudrate=115200, base_address=1000)

# Connect to the motor
motor1.connect()
motor2.connect()

# Control motor
motor1.enable_driver()
motor1.set_speed(5000)
motor1.start_jogging()
time.sleep(5)
motor1.stop_jogging()
motor1.disable_driver()

# Close connection
motor1.disconnect()
