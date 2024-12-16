import time
import threading
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial

# Establish a connection to the Modbus device
def connect_modbus():
    try:
        # Configure the serial connection
        ser = serial.Serial(
            port="/dev/ttyUSB0",
            baudrate=115200,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=0.5
        )
        client = modbus_rtu.RtuMaster(ser)
        client.set_timeout(2.0)
        print("Modbus connection successful")
        return client
    except Exception as e:
        print(f"Modbus connection failed: {e}")
        return None

# Enable driver functions
def enable_driver(client):
    command_register = 1124  # Zero-based address
    driver_enable_opcode = 0x009F
    try:
        client.execute(1, cst.WRITE_SINGLE_REGISTER, command_register, output_value=driver_enable_opcode)
        print("Driver enabled.")
    except Exception as e:
        print(f"Error enabling driver: {e}")
    time.sleep(1.5)
def enable_driver1(client):
    command_register = 124
    driver_enable_opcode = 0x009F
    try:
        client.execute(1, cst.WRITE_SINGLE_REGISTER, command_register, output_value=driver_enable_opcode)
        print("Driver1 enabled.")
    except Exception as e:
        print(f"Error enabling driver1: {e}")
    time.sleep(1.5)
# Disable driver functions
def disable_driver(client):
    command_register = 1124
    driver_disable_opcode = 0x009E
    try:
        client.execute(1, cst.WRITE_SINGLE_REGISTER, command_register, output_value=driver_disable_opcode)
        print("Driver disabled.")
    except Exception as e:
        print(f"Error disabling driver: {e}")
    time.sleep(1.5)
def disable_driver1(client):
    command_register = 124
    driver_disable_opcode = 0x009E
    try:
        client.execute(1, cst.WRITE_SINGLE_REGISTER, command_register, output_value=driver_disable_opcode)
        print("Driver1 disabled.")
    except Exception as e:
        print(f"Error disabling driver1: {e}")
    time.sleep(1.5)
# Start and stop jogging
def start_jogging(client):
    command_register = 1124
    start_jogging_opcode = 0x0096
    try:
        client.execute(1, cst.WRITE_SINGLE_REGISTER, command_register, output_value=start_jogging_opcode)
        print("Jogging mode enabled.")
    except Exception as e:
        print(f"Error starting jogging: {e}")
    time.sleep(1.5)
def start_jogging1(client):
    command_register = 124
    start_jogging_opcode = 0x0096
    try:
        client.execute(1, cst.WRITE_SINGLE_REGISTER, command_register, output_value=start_jogging_opcode)
        print("Jogging mode1 enabled.")
    except Exception as e:
        print(f"Error starting jogging1: {e}")
    time.sleep(1.5)
def stop_jogging(client):
    command_register = 1124
    stop_jogging_opcode = 0x00D8
    try:
        client.execute(1, cst.WRITE_SINGLE_REGISTER, command_register, output_value=stop_jogging_opcode)
        print("Jogging mode stopped.")
    except Exception as e:
        print(f"Error stopping jogging: {e}")
    time.sleep(1.5)
def stop_jogging1(client):
    command_register = 124
    stop_jogging_opcode = 0x00D8
    try:
        client.execute(1, cst.WRITE_SINGLE_REGISTER, command_register, output_value=stop_jogging_opcode)
        print("Jogging mode1 stopped.")
    except Exception as e:
        print(f"Error stopping jogging1: {e}")
    time.sleep(1.5)
# Write speed to the motor
def write_speed(client, speed_value, run_time=10):
    speed_register = 1342
    try:
        high_word = (speed_value >> 16) & 0xFFFF
        low_word = speed_value & 0xFFFF
        client.execute(1, cst.WRITE_MULTIPLE_REGISTERS, speed_register, output_value=[high_word, low_word])
        print(f"Motor running at speed value {speed_value}.")
        time.sleep(run_time)
        client.execute(1, cst.WRITE_MULTIPLE_REGISTERS, speed_register, output_value=[0, 0])
        
        #print("Motor stopped.")
        
    except Exception as e:
        print(f"Error writing speed: {e}")
    time.sleep(0.85)
def write_speed1(client, speed_value, run_time=10):
    speed_register = 342
    try:
        high_word = (speed_value >> 16) & 0xFFFF
        low_word = speed_value & 0xFFFF
        client.execute(1, cst.WRITE_MULTIPLE_REGISTERS, speed_register, output_value=[high_word, low_word])
        print(f"Motor1 running at speed value {speed_value}.")
        time.sleep(run_time)
        client.execute(1, cst.WRITE_MULTIPLE_REGISTERS, speed_register, output_value=[0, 0])
        #print("Motor1 stopped.")
        
    except Exception as e:
        print(f"Error writing speed1: {e}")
    time.sleep(0.85)
# Reading 32-bit registers
def read_32bit_registers(client, register_address_motor1, register_address_motor2):
    try:
        zero_based_address_motor1 = register_address_motor1 - 40001
        zero_based_address_motor2 = register_address_motor2 - 40001
        while reading_active:
            result_motor1 = client.execute(1, cst.READ_HOLDING_REGISTERS, zero_based_address_motor1, 2)
            high_word_motor1, low_word_motor1 = result_motor1
            value_motor1 = (high_word_motor1 << 16) | low_word_motor1
            print(f"Motor1 register value: {value_motor1}")
            time.sleep(0.43)
            result_motor2 = client.execute(1, cst.READ_HOLDING_REGISTERS, zero_based_address_motor2, 2)
            high_word_motor2, low_word_motor2 = result_motor2
            value_motor2 = (high_word_motor2 << 16) | low_word_motor2
            print(f"Motor2 register value: {value_motor2}")
            
            time.sleep(0.43)
    except Exception as e:
        print(f"Error reading 32-bit registers: {e}")
    time.sleep(0.1)    

# Reset encoder
def reset_encoder(client):
    command_register = 1124
    reset_opcode = 0x0098
    try:
        client.execute(1, cst.WRITE_SINGLE_REGISTER, command_register, output_value=reset_opcode)
        print("Encoder reset.")
    except Exception as e:
        print(f"Error resetting encoder: {e}")
    time.sleep(1)
def reset_encoder1(client):
    command_register = 124
    reset_opcode = 0x0098
    try:
        client.execute(1, cst.WRITE_SINGLE_REGISTER, command_register, output_value=reset_opcode)
        print("Encoder1 reset.")
    except Exception as e:
        print(f"Error resetting encoder1: {e}")
    time.sleep(1)
# Main program
if __name__ == "__main__":
    client = connect_modbus()
    if client:
        enable_driver(client)
        enable_driver1(client)
        reset_encoder(client)
        reset_encoder1(client)
        start_jogging(client)
        start_jogging1(client)

        reading_active = True

        # Threads for writing speed and reading registers
        speed_thread_left = threading.Thread(target=write_speed, args=(client, 5000, 10))
        speed_thread_right = threading.Thread(target=write_speed1, args=(client, 5000, 10))
        time.sleep(0.43)
        read_thread = threading.Thread(target=read_32bit_registers, args=(client, 40011, 41011))

        # Start threads
        speed_thread_left.start()
        speed_thread_right.start()
        read_thread.start()
        
        # Wait for speed threads to finish
        speed_thread_left.join()
        speed_thread_right.join()
        time.sleep(0.5)
        
        # Stop reading after speed threads complete
        reading_active = False
        read_thread.join(timeout=1)
        
        # Stop jogging and disable driver
        stop_jogging(client)
        stop_jogging1(client)
        disable_driver(client)
        disable_driver1(client)

        client.close()


##############################################################################3
########################### OUTPUT ###################################################
# nuc@nuc:~/catkin_ws_1/src$ /bin/python3 "/home/nuc/Downloads/Motor Encoder Data ubantu.py"
# Modbus connection successful
# Driver enabled.
# Driver1 enabled.
# Encoder reset.
# Encoder1 reset.
# Jogging mode enabled.
# Jogging mode1 enabled.
# Motor running at speed value 5000.
# Motor1 running at speed value 5000.
# Motor1 register value: 21
# Motor2 register value: 75992
# Motor1 register value: 165644
# Motor2 register value: 262697
# Motor1 register value: 352260
# Motor2 register value: 449278
# Motor1 register value: 538893
# Motor2 register value: 635768
# Motor1 register value: 725478
# Motor2 register value: 822428
# Motor1 register value: 911983
# Motor2 register value: 1008935
# Motor1 register value: 1098589
# Motor2 register value: 1195681
# Motor1 register value: 1285331
# Motor2 register value: 1382264
# Motor1 register value: 1471827
# Motor2 register value: 1568714
# Motor1 register value: 1658408
# Motor2 register value: 1755418
# Motor1 register value: 1844977
# Motor2 register value: 1941878
# Motor1 register value: 2031646
# Motor2 register value: 2088310
# Motor1 register value: 2088323
# Motor2 register value: 2088339
# Jogging mode stopped.
# Jogging mode1 stopped.
# Driver disabled.
# Driver1 disabled.
# nuc@nuc:~/catkin_ws_1/src$ 