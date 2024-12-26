import time
from moon_servo.connection import ModbusConnection
from moon_servo.motor import MoonServoMotor
from moon_servo import MoonServoMotor

# Initialize the motor with the desired parameters
motor = MoonServoMotor(port='/dev/ttyUSB0', baudrate=115200, base_address=0)

# Connect to the motor
motor.connect()

# Create motor instance
motor1 = MoonServoMotor(connection, base_address=0)  # Base address for motor 1

# Control motor
motor1.enable_driver()
motor1.set_speed(5000)
motor1.start_jogging()
time.sleep(5)
motor1.stop_jogging()
motor1.disable_driver()

# Close connection
motor.disconnect()
