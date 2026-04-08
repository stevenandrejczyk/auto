import serial
import time

def read_serial_from_arduino(port='/dev/ttyACM0', baudrate=9600, timeout=1):
    ser = None

    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Arduino reset delay

        print(f"Connected to {port} at {baudrate} baud")

        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()

            if line:
                print(f"Received: {line}")

    except serial.SerialException as e:
        print(f"Serial error: {e}")

    except KeyboardInterrupt:
        print("\nStopped by user")

    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial connection closed")


if __name__ == "__main__":
    read_serial_from_arduino()