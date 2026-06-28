# plc_buzzer.py — PLC 蜂鳴器控制 (有聲輸出模擬)
# 用 print("\a") 或文字模擬 PLC 控制蜂鳴器 ON/OFF

import time
import sys

# --- 蜂鳴器類別 (模擬 PLC 輸出線圈) ---
class Buzzer:
    """PLC 控制的蜂鳴器輸出"""
    def __init__(self):
        self.output = False       # 線圈狀態
        self.beep_count = 0       # 響的次數
        self.mode = "off"         # off / continuous / pulse

    def scan(self, input_signal, mode="continuous"):
        """
        每次掃描週期檢查輸入信號
        input_signal: 輸入接點 (緊急按鈕/傳感器觸發)
        mode: "continuous"=持續響, "pulse"=間歇響
        """
        if input_signal:
            self.output = True
            self.mode = mode
            if mode == "pulse":
                self.beep_count += 1
                print(f"\a  [BEEP #{self.beep_count}] 蜂鳴器響!")
                time.sleep(0.3)
                print("   [SILENCE] 停止")
                time.sleep(0.3)
            else:
                print("\a  [BUZZING...] 蜂鳴器持續響!")
        else:
            self.output = False
            self.mode = "off"

        return self.output


# --- 示範 ---
buzzer = Buzzer()
print("=== PLC Buzzer Control Demo ===\n")

# 模擬傳感器觸發 (緊急停止按鈕)
triggers = [False, True, True, True, False]
for i, trig in enumerate(triggers):
    print(f"\n--- Scan {i+1} ---")
    buzzer.scan(trig, mode="pulse")
    time.sleep(0.5)

print("\n=== 系統恢復正常 ===")
buzzer.scan(False)
print(f"蜂鳴器狀態: {'ON' if buzzer.output else 'OFF'}")
