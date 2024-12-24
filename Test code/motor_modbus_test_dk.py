from pymodbus.client import ModbusSerialClient
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s [Line: %(lineno)d]')
logger = logging.getLogger(__name__)

# Modbus client configuration
client = ModbusSerialClient(port='/dev/ttyUSB0', baudrate=115200, timeout=0.1, parity='N', stopbits=1, bytesize=8)

# Motor-specific base addresses
MOTOR_CONFIG = {
    1: {"command_register": 124, "speed_register": 342, "accel_register": 338, "decel_register": 340},
    2: {"command_register": 1124, "speed_register": 1342, "accel_register": 1338, "decel_register": 1340},
}

# Connect to Modbus
def connect_modbus():
    if client.connect():
        logger.info("Modbus Connection Successful")
        return True
    else:
        logger.error("Modbus Connection Failed")
        return False

# Enable driver
def enable_driver(motor_id):
    command_register = MOTOR_CONFIG[motor_id]["command_register"]
    driver_enable_opcode = 0x009F
    try:
        client.write_register(command_register, driver_enable_opcode)
        logger.info(f"Motor {motor_id}: Driver enabled.")
        time.sleep(0.5)
    except Exception as e:
        logger.error(f"Motor {motor_id}: Error enabling driver - {e}")

# Disable driver
def disable_driver(motor_id):
    command_register = MOTOR_CONFIG[motor_id]["command_register"]
    driver_disable_opcode = 0x009E
    try:
        client.write_register(command_register, driver_disable_opcode)
        logger.info(f"Motor {motor_id}: Driver disabled.")
        time.sleep(0.5)
    except Exception as e:
        logger.error(f"Motor {motor_id}: Error disabling driver - {e}")

# Start jogging
def start_jogging(motor_id):
    command_register = MOTOR_CONFIG[motor_id]["command_register"]
    start_jogging_opcode = 0x0096
    try:
        client.write_register(command_register, start_jogging_opcode)
        logger.info(f"Motor {motor_id}: Jogging mode enabled.")
        time.sleep(0.1)
    except Exception as e:
        logger.error(f"Motor {motor_id}: Error starting jogging - {e}")

# Stop jogging
def stop_jogging(motor_id):
    command_register = MOTOR_CONFIG[motor_id]["command_register"]
    stop_jogging_opcode = 0x00D8
    try:
        client.write_register(command_register, stop_jogging_opcode)
        logger.info(f"Motor {motor_id}: Jogging mode stopped.")
        time.sleep(0.5)
    except Exception as e:
        logger.error(f"Motor {motor_id}: Error stopping jogging - {e}")

# Write speed
def write_speed(motor_id, speed_value, run_time=10):
    speed_register = MOTOR_CONFIG[motor_id]["speed_register"]
    try:
        high_word = (speed_value >> 16) & 0xFFFF
        low_word = speed_value & 0xFFFF
        client.write_registers(speed_register, [high_word, low_word])
        logger.info(f"Motor {motor_id}: Running at speed value {speed_value}.")
        time.sleep(run_time)
        client.write_registers(speed_register, [0, 0])  # Stop motor
        logger.info(f"Motor {motor_id}: Stopped after {run_time} seconds.")
    except Exception as e:
        logger.error(f"Motor {motor_id}: Error writing speed - {e}")

# Write acceleration
def write_acceleration(motor_id, accel_value):
    accel_register = MOTOR_CONFIG[motor_id]["accel_register"]
    try:
        if 1 <= accel_value <= 30000:
            high_word = (accel_value >> 16) & 0xFFFF
            low_word = accel_value & 0xFFFF
            client.write_registers(accel_register, [high_word, low_word])
            logger.info(f"Motor {motor_id}: Acceleration set to {accel_value}.")
        else:
            logger.warning(f"Motor {motor_id}: Acceleration value {accel_value} is out of range (1-30000).")
    except Exception as e:
        logger.error(f"Motor {motor_id}: Error writing acceleration - {e}")

# Write deceleration
def write_deceleration(motor_id, decel_value):
    decel_register = MOTOR_CONFIG[motor_id]["decel_register"]
    try:
        if 1 <= decel_value <= 30000:
            high_word = (decel_value >> 16) & 0xFFFF
            low_word = decel_value & 0xFFFF
            client.write_registers(decel_register, [high_word, low_word])
            logger.info(f"Motor {motor_id}: Deceleration set to {decel_value}.")
        else:
            logger.warning(f"Motor {motor_id}: Deceleration value {decel_value} is out of range (1-30000).")
    except Exception as e:
        logger.error(f"Motor {motor_id}: Error writing deceleration - {e}")
