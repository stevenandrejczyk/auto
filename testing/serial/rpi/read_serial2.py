import serial
import threading
import time

# create serial connection and wait for Arduino to reset
ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
time.sleep(2)
# lock for synchronizing access to shared variables
lock = threading.Lock()

current_temp = "N/A"
set_temp = "N/A"

# SERIAL READER (updates temp in background)
def reader():
    # declare global variables to modify them inside the thread
    global current_temp

    #read serial input in an infinite loop and update temp
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line.startswith("TEMP:"):
            with lock:
                current_temp = line.split(":")[1]

# RENDER FUNCTION
def render():
    with lock:
        temp = current_temp
        setp = set_temp

    print("\033[2J\033[H", end="")  # clear screen

    print("==== CONTROL PANEL ====")
    print(f"Current Temp : {temp}")
    print(f"Set Temp     : {setp}")
    print("=======================")
    print("Commands:")
    print("  w  -> set temperature")
    print("  ENTER -> refresh")
    print("  q  -> quit")

# MAIN LOOP
def main():
    global set_temp

    # main loop for user input
    while True:
        # render options
        render()
        # get user command
        cmd = input("> ").strip()
        if cmd == "q":
            break
        elif cmd == "w":
            new_set = input("Enter new set temp: ").strip()
            if new_set:
                with lock:
                    set_temp = new_set
                # send new set temp to Arduino
                ser.write(f"SET:{new_set}\n".encode())
        # anything else (including Enter) just refreshes

# RUN
threading.Thread(target=reader, daemon=True).start()
main()