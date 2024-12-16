######################################################################################################################################
################################################### using this code WE control the robot through the teleop function ##################
##########################################################################################################################################


#!/usr/bin/env python3

import time
import threading
from modbus_tk import modbus_rtu
from modbus_tk.defines import READ_HOLDING_REGISTERS, WRITE_MULTIPLE_REGISTERS, WRITE_SINGLE_REGISTER
import serial
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray

class MotorController:
    def __init__(self):
        self.linear_velocity = 0
        self.angular_velocity = 0
        self.is_command_active = False

        self.left_encoder_ticks = 0
        self.right_encoder_ticks = 0
        self.prev_left_encoder_ticks = 0
        self.prev_right_encoder_ticks = 0

        self.reading_active = False
        self.lock = threading.Lock()
        self.modbus_master = self.initialize_modbus()

        # ROS Publisher for encoder values
        self.encoder_pub = rospy.Publisher('encoder_ticks', Int32MultiArray, queue_size=10)
        
    def initialize_modbus(self):
        try:
            serial_port = serial.Serial(
                port="/dev/ttyUSB0",
                baudrate=115200,
                bytesize=8,
                parity="N",
                stopbits=1,
                timeout=0.001
            )
            modbus_master = modbus_rtu.RtuMaster(serial_port)
            modbus_master.set_timeout(1)
            modbus_master.set_verbose(True)
            rospy.loginfo("Modbus connection established successfully.")
            return modbus_master
        except Exception as e:
            rospy.logerr(f"Error initializing Modbus connection: {e}")
            exit(1)

    def enable_driver(self, slave_id=1):
        self._write_register(slave_id, 124, 0x009F)
        self._write_register(slave_id, 1124, 0x009F)
        rospy.loginfo("Driver enabled.")

    def disable_driver(self, slave_id=1):
        self._write_register(slave_id, 124, 0x009E)
        self._write_register(slave_id, 1124, 0x009E)
        rospy.loginfo("Driver disabled.")

    def encoder_zero(self, slave_id=1):
        self._write_register(slave_id, 124, 0x0098)
        self._write_register(slave_id, 1124, 0x0098)
        rospy.loginfo("Encoders zeroed.")

    def start_jogging(self, slave_id=1):
        self._write_register(slave_id, 124, 0x0096)
        self._write_register(slave_id, 1124, 0x0096)
        rospy.loginfo("Jogging mode enabled.")

    def stop_jogging(self, slave_id=1):
        self._write_register(slave_id, 124, 0x00D8)
        self._write_register(slave_id, 1124, 0x00D8)
        rospy.loginfo("Jogging mode stopped.")

    def _write_register(self, slave_id, register, value):
        try:
            self.modbus_master.execute(slave_id, WRITE_SINGLE_REGISTER, register, output_value=value)
            time.sleep(0.1)
        except Exception as e:
            rospy.logerr(f"Error writing to register {register}: {e}")

    def map_velocity_to_motor_speed(self, linear_vel, angular_vel, max_linear_speed=1.0, max_motor_speed=4000):
        left_speed = int((linear_vel - angular_vel * 0.5) * (max_motor_speed / max_linear_speed)) * -1
        right_speed = int((linear_vel + angular_vel * 0.5) * (max_motor_speed / max_linear_speed))
        return left_speed, right_speed

    def write_synchronized_speed(self, left_speed, right_speed, slave_id=1):
        speed_registers = {1: 342, 2: 1342}
        try:
            left_high_word = (left_speed >> 16) & 0xFFFF
            left_low_word = left_speed & 0xFFFF
            right_high_word = (right_speed >> 16) & 0xFFFF
            right_low_word = right_speed & 0xFFFF

            self.modbus_master.execute(slave_id, WRITE_MULTIPLE_REGISTERS, speed_registers[1], 
                                        output_value=[left_high_word, left_low_word])
            self.modbus_master.execute(slave_id, WRITE_MULTIPLE_REGISTERS, speed_registers[2], 
                                        output_value=[right_high_word, right_low_word])
        except Exception as e:
            rospy.logerr(f"Error writing synchronized speeds: {e}")

    def read_32bit_registers(self, register_address_motor1, register_address_motor2, slave_id=1):
        with self.lock:
            if not self.reading_active:
                return
            try:
                result_motor1 = self.modbus_master.execute(slave_id, READ_HOLDING_REGISTERS, register_address_motor1 - 40001, 2)
                result_motor2 = self.modbus_master.execute(slave_id, READ_HOLDING_REGISTERS, register_address_motor2 - 40001, 2)

                high_motor1, low_motor1 = result_motor1
                high_motor2, low_motor2 = result_motor2

                value_motor1 = (high_motor1 << 16) | low_motor1
                value_motor2 = (high_motor2 << 16) | low_motor2

                # Log the values
                rospy.loginfo(f"Motor1: {value_motor1}, Motor2: {value_motor2}")

                # Publish the encoder values
                encoder_msg = Int32MultiArray()
                encoder_msg.data = [value_motor1, value_motor2]
                self.encoder_pub.publish(encoder_msg)
                print(f"Left motor encoder ticks: {value_motor1}, Right motor encoder ticks: {65535 - value_motor2}")
            except Exception as e:
                rospy.logerr(f"Error reading 32-bit registers: {e}")

    def callback(self, msg):
        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z
        self.is_command_active = abs(self.linear_velocity) > 0 or abs(self.angular_velocity) > 0

    def driver_callback(self, event):
        if self.is_command_active:
            left_speed, right_speed = self.map_velocity_to_motor_speed(self.linear_velocity, self.angular_velocity)
            self.write_synchronized_speed(left_speed, right_speed)
        else:
            self.write_synchronized_speed(0, 0)

    def start(self):
        rospy.init_node('motor_driver', anonymous=True)

        rospy.Subscriber("cmd_vel", Twist, self.callback)

        rospy.Timer(rospy.Duration(0.010), self.driver_callback)

        self.enable_driver()
        self.encoder_zero()
        self.start_jogging()

        self.reading_active = True
        read_thread = threading.Thread(target=self.read_32bit_registers, args=(40011, 41011))
        read_thread.start()

        rospy.spin()

        self.reading_active = False
        read_thread.join()
        self.stop_jogging()
        self.disable_driver()

if __name__ == "__main__":
    try:
        motor_controller = MotorController()
        motor_controller.start()
    except Exception as e:
        rospy.logerr(f"An error occurred: {e}")

