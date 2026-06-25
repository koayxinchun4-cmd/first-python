
import time

import os

print("=== PLC TIMER WITH BUZZER ===")

sec = int(input("Set timer (seconds): "))

print(f"Timer set: {sec}s")

print("Counting down...")

for i in range(sec, 0, -1):

    print(f"  T{sec}: {i}s remaining")

    time.sleep(1)

# Buzzer ON

print("\n>>> OUTPUT ON <<<")

for _ in range(3):

    os.system("play -nq synth 0.3 sine 800 2>/dev/null || termux-vibrate -d 200")

    time.sleep(0.2)

print("=== CYCLE COMPLETE ===")

