from pymodbus.client import ModbusSerialClient
import time
import threading

# Configuration for Modbus Client
client = ModbusSerialClient(port='COM3', baudrate=115200, timeout=5, parity='N', stopbits=1, bytesize=8)


def connect_modbus():
    if client.connect():
        print("Modbus Connection Successful")
        return True
    else:
        print("Modbus Connection Failed")
        return False
    
def enable_driver1():
    command_register = 124  # 40125 - 40001 = 124 (Zero-based address)
    driver_enable_opcode = 0x009F  # Start Jogging (CJ) opcode
    try:
        client.write_register(command_register, driver_enable_opcode)
        print("Driver enabled.")
        time.sleep(0.5)  # Short delay to observe jogging
    except Exception as e:
        print(f"Error enabling jogging: {e}")

def enable_driver():
    command_register = 1124  # 40125 - 40001 = 124 (Zero-based address)
    driver_enable_opcode = 0x009F  # Start Jogging (CJ) opcode
    try:
        client.write_register(command_register, driver_enable_opcode)
        print("Driver enabled.")
        time.sleep(0.5)  # Short delay to observe jogging
    except Exception as e:
        print(f"Error enabling jogging: {e}")

def disable_driver1():
    command_register = 124  # 40125 - 40001 = 124 (Zero-based address)
    driver_disable_opcode = 0x009E  # Start Jogging (CJ) opcode
    try:
        client.write_register(command_register, driver_disable_opcode)
        print("Driver disabled.")
        time.sleep(0.5)  # Short delay to observe jogging
    except Exception as e:
        print(f"Error disabling jogging: {e}")

def disable_driver():
    command_register = 1124  # 40125 - 40001 = 124 (Zero-based address)
    driver_disable_opcode = 0x009E  # Start Jogging (CJ) opcode
    try:
        client.write_register(command_register, driver_disable_opcode)
        print("Driver disabled.")
        time.sleep(0.5)  # Short delay to observe jogging
    except Exception as e:
        print(f"Error disabling jogging: {e}")

# Function to enable jogging
def start_jogging():
    command_register = 1124  # 40125 - 40001 = 124 (Zero-based address)
    start_jogging_opcode = 0x0096  # Start Jogging (CJ) opcode
    try:
        client.write_register(command_register, start_jogging_opcode)
        print("Jogging mode enabled.")
        time.sleep(0.1)  # Short delay to observe jogging
    except Exception as e:
        print(f"Error Starting jogging: {e}")

def start_jogging1():
    command_register = 124  # 40125 - 40001 = 124 (Zero-based address)
    start_jogging_opcode = 0x0096  # Start Jogging (CJ) opcode
    try:
        client.write_register(command_register, start_jogging_opcode)
        print("Jogging mode enabled.")
        time.sleep(0.1)  # Short delay to observe jogging
    except Exception as e:
        print(f"Error Starting jogging: {e}")


# Function to stop jogging
def stop_jogging():
    command_register = 1124  # 40125 - 40001 = 124 (Zero-based address)
    stop_jogging_opcode = 0x00D8  # Stop Jogging (SJ) opcode
    try:
        client.write_register(command_register, stop_jogging_opcode)
        print("Jogging mode stopped.")
        time.sleep(0.5)  # Short delay to observe stopping
    except Exception as e:
        print(f"Error stopping jogging: {e}")

def stop_jogging1():
    command_register = 124  # 40125 - 40001 = 124 (Zero-based address)
    stop_jogging_opcode = 0x00D8  # Stop Jogging (SJ) opcode
    try:
        client.write_register(command_register, stop_jogging_opcode)
        print("Jogging mode stopped.")
        time.sleep(0.5)  # Short delay to observe stopping
    except Exception as e:
        print(f"Error stopping jogging: {e}")

def write_speed(speed_value, run_time=10):
    speed_register = 1342  # Zero-based address for 40343

    try:
        # Convert the 32-bit speed value to two 16-bit registers (high and low)
        high_word = (speed_value >> 16) & 0xFFFF  # Extract high 16 bits
        low_word = speed_value & 0xFFFF  # Extract low 16 bits

        # Write the 32-bit value as two consecutive 16-bit registers
        client.write_registers(speed_register, [high_word, low_word])

        print(f"Motor running at speed value {speed_value}.")

        # Run the motor for the specified time
        time.sleep(run_time)

        # Stop the motor by setting speed to 0
        high_word = 0
        low_word = 0
        client.write_registers(speed_register, [high_word, low_word])

        print("Motor stopped after 10 seconds.")
    except Exception as e:
        print(f"Error writing to speed register {speed_register}: {e}")

def write_speed1(speed_value, run_time=10):
    speed_register = 342  # Zero-based address for 40343

    try:
        # Convert the 32-bit speed value to two 16-bit registers (high and low)
        high_word = (speed_value >> 16) & 0xFFFF  # Extract high 16 bits
        low_word = speed_value & 0xFFFF  # Extract low 16 bits

        # Write the 32-bit value as two consecutive 16-bit registers
        client.write_registers(speed_register, [high_word, low_word])

        print(f"Motor running at speed value {speed_value}.")

        # Run the motor for the specified time
        time.sleep(run_time)

        # Stop the motor by setting speed to 0
        high_word = 0
        low_word = 0
        client.write_registers(speed_register, [high_word, low_word])

        print("Motor stopped after 10 seconds.")
    except Exception as e:
        print(f"Error writing to speed register {speed_register}: {e}")

reading_active = True  # Global flag to control reading

def read_32bit_registers_for_two_motors(register_address_motor1, register_address_motor2):
    global reading_active  # Declare as global
    try:
        zero_based_address_motor1 = register_address_motor1 - 40001  # Register address
        zero_based_address_motor2 = register_address_motor2 - 40001
        
        while reading_active:  # Check the flag in the loop
            # Read motor 1 registers
            result_motor1 = client.read_holding_registers(zero_based_address_motor1, 2)
            if result_motor1.isError():
                print(f"Error reading 32-bit register for motor 1 at address {register_address_motor1}")
            else:
                high_word_motor1 = result_motor1.registers[0]
                low_word_motor1 = result_motor1.registers[1]
                value_32bit_motor1 = (high_word_motor1 << 16) | low_word_motor1
                print(f"Value at register for motor 1 {register_address_motor1}: {value_32bit_motor1}")
            
            # Read motor 2 registers
            result_motor2 = client.read_holding_registers(zero_based_address_motor2, 2)
            if result_motor2.isError():
                print(f"Error reading 32-bit register for motor 2 at address {register_address_motor2}")
            else:
                high_word_motor2 = result_motor2.registers[0]
                low_word_motor2 = result_motor2.registers[1]
                value_32bit_motor2 = (high_word_motor2 << 16) | low_word_motor2
                print(f"Value at register for motor 2 {register_address_motor2}: {value_32bit_motor2}")

            time.sleep(1)  # Delay between reads
    except Exception as e:
        print(f"Error reading 32-bit registers for motors: {e}")



def reset_encoder():
    """Reset the encoder value to zero using the 0x0098 opcode."""
    command_register = 1124  # Zero-based address for 40125
    reset_opcode = 0x0098  # Reset encoder opcode
    try:
        client.write_register(command_register, reset_opcode)
        print("Encoder value reset to zero.")
        time.sleep(0.5)  # Wait for the reset operation to take effect
    except Exception as e:
        print(f"Error resetting encoder: {e}")

def reset_encoder1():
    """Reset the encoder value to zero using the 0x0098 opcode."""
    command_register = 124  # Zero-based address for 40125
    reset_opcode = 0x0098  # Reset encoder opcode
    try:
        client.write_register(command_register, reset_opcode)
        print("Encoder value reset to zero.")
        time.sleep(0.5)  # Wait for the reset operation to take effect
    except Exception as e:
        print(f"Error resetting encoder: {e}")



if connect_modbus():
    enable_driver()
    enable_driver1()
    reset_encoder()
    reset_encoder1()
    start_jogging()
    start_jogging1()

    # Create threads
    speed_thread_left = threading.Thread(target=write_speed, args=(5000, 10))
    speed_thread_right = threading.Thread(target=write_speed1, args=(5000, 10))

    read_thread = threading.Thread(target=read_32bit_registers_for_two_motors, args=(40011, 41011))

    # Start both threads
    speed_thread_left.start()
    speed_thread_right.start()

    read_thread.start()

    # Wait for the speed thread to complete
    speed_thread_left.join()
    speed_thread_right.join()
    print("Speed writing complete. Stopping read thread.")

    # Stop reading after speed completes
   

    # Clean up
    stop_jogging()
    
    stop_jogging1()
    reading_active = False  # Signal to stop the read thread
    read_thread.join(timeout=1)
    disable_driver()
    disable_driver1()
    client.close()

#####################################################################################
