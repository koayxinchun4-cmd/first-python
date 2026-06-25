
import time

import os

import threading

# === PLC 狀態 ===

relay       = False

motor       = False

timer_done  = False

relay_delay = False

timer_thread = None

timer_stop = False

def beep(n=3):

    for _ in range(n):

        os.system("play -nq synth 0.3 sine 800 2>/dev/null || termux-vibrate -d 200")

        time.sleep(0.2)

def timer_5s():

    global timer_done, timer_stop, relay_delay

    timer_done = False

    timer_stop = False

    for i in range(50, 0, -1):

        if timer_stop:

            return

        time.sleep(0.1)

    timer_done = True

    relay_delay = True

    beep(1)

def show_state():

    print(f"\n{'='*35}")

    print(f" 160.00 RELAY  : {'ON ' if relay else 'OFF'}")

    print(f" 160.01 DELAY  : {'ON ' if relay_delay else 'OFF'}")

    g = "GREEN ON" if (relay and not relay_delay and not motor) else "OFF"

    r = "RED ON" if relay else "OFF"

    y = "YELL ON" if (relay and motor) else "OFF"

    b = "BUZZ ON" if relay_delay else "OFF"

    m = "MOTOR ON" if motor else "OFF"

    t = "DONE" if timer_done else ("RUN..." if timer_thread and timer_thread.is_alive() else "IDLE")

    print(f" Q:100.00 GREEN : {g}")

    print(f" Q:100.01 RED   : {r}")

    print(f" Q:100.03 YELL  : {y}")

    print(f" Q:100.05 BUZZ  : {b}")

    print(f" Q:100.07 MOTOR : {m}")

    print(f" T000 TIMER     : {t}")

    print(f"{'='*35}")

    print(" [Enter] START  [1] S1  [2] S2  [s] STOP  [i] IMM  [q] QUIT")

    print(" > ", end="")

def start_timer():

    global timer_thread, timer_stop

    if timer_thread and timer_thread.is_alive():

        timer_stop = True

        timer_thread.join()

    timer_stop = False

    timer_thread = threading.Thread(target=timer_5s, daemon=True)

    timer_thread.start()

# === 主迴圈 ===

print("=== OMRON CX-PROGRAMMER SIM ===")

print("Traffic Light + Motor + Buzzer\n")

while True:

    show_state()

    key = input().strip().lower()

    # START

    if key == "":

        relay = True

        timer_done = False

        relay_delay = False

        motor = False

        print(">>> START — relay ON, RED ON")

    # S1

    elif key == "1":

        if relay:

            motor = True

            relay_delay = False

            timer_done = False

            print(">>> S1 — MOTOR ON, YELLOW ON")

        else:

            print("System OFF. Press Enter first.")

    # S2

    elif key == "2":

        if relay:

            motor = False

            print(">>> S2 — MOTOR OFF, 5s timer start")

            start_timer()

        else:

            print("System OFF.")

    # STOP

    elif key == "s":

        relay = False

        motor = False

        timer_done = False

        relay_delay = False

        timer_stop = True

        print(">>> STOP — ALL RESET")

    # IMMEDIATELY

    elif key == "i":

        relay = False

        motor = False

        timer_done = False

        relay_delay = False

        timer_stop = True

        print(">>> IMM — ALL RESET")

    elif key == "q":

        timer_stop = True

        print("=== SIM END ===")

        break

