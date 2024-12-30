import time
from .connection import ModbusConnection

# REGISTER ADDRESSES FOR MOON SERVO MOTOR
COMMAND_REGISTER = 124
SPEED_REGISTER = 342   # 32-bit register

class MoonServoMotor:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, base_address: int = 0):
        connection: ModbusConnection = ModbusConnection(port=port, baudrate=baudrate, timeout=5, parity='N', stopbits=1, bytesize=8)
        self.client = connection.get_client()
        self.base_address = base_address

    def connect(self):
        if self.client.connect():
            print("Modbus Connection Successful")
            return True
        else:
            raise ConnectionError("Modbus Connection Failed")

    def disconnect(self):
        self.client.close()
        print("Modbus Connection Closed")

    def enable_driver(self):
        command_register = self.base_address + COMMAND_REGISTER
        opcode = 0x009F
        self._write_register(command_register, opcode, "Enable driver")

    def disable_driver(self):
        command_register = self.base_address + COMMAND_REGISTER
        opcode = 0x009E
        self._write_register(command_register, opcode, "Disable driver")

    def start_jogging(self):
        command_register = self.base_address + COMMAND_REGISTER
        opcode = 0x0096
        self._write_register(command_register, opcode, "Start jogging")

    def stop_jogging(self):
        command_register = self.base_address + COMMAND_REGISTER
        opcode = 0x00D8
        self._write_register(command_register, opcode, "Stop jogging")

    def set_speed(self, speed_value, run_time=10):
        speed_register = self.base_address + SPEED_REGISTER
        self._write_32bit_register(speed_register, speed_value, "Set speed")
        time.sleep(run_time)
        self._write_32bit_register(speed_register, 0, "Stop motor after timeout")

    def set_acceleration(self, accel_value):
        accel_register = self.base_address + 338
        self._write_32bit_register(accel_register, accel_value, "Set acceleration")

    def set_deceleration(self, decel_value):
        decel_register = self.base_address + 340
        self._write_32bit_register(decel_register, decel_value, "Set deceleration")

    def _write_register(self, register, value, action):
        try:
            self.client.write_register(register, value)
            print(f"{action} successful.")
        except Exception as e:
            print(f"Error during {action}: {e}")
            raise

    def _write_32bit_register(self, register, value, action):
        try:
            high_word = (value >> 16) & 0xFFFF
            low_word = value & 0xFFFF
            self.client.write_registers(register, [high_word, low_word])
            print(f"{action} successful.")
        except Exception as e:
            print(f"Error during {action}: {e}")
            raise
