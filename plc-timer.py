
import time

print("=== PLC TIMER (TON) ===")

sec = int(input("Set timer (seconds): "))

print(f"Timer set: {sec}s")

print("Counting down...")

for i in range(sec, 0, -1):

    print(f"  T{sec}: {i}s remaining")

    time.sleep(1)

print("\n>>> OUTPUT ON <<<")

