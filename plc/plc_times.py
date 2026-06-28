# plc_times.py — PLC 計時器 (Timer) 概念練習
# 模擬 PLC 中的 TON (Timer On-Delay) 計時器

import time

# --- TON 計時器類別 (模擬 PLC 掃描週期) ---
class TON:
    """Timer On-Delay: 輸入 ON 後延遲 preset 秒才輸出 ON"""
    def __init__(self, preset):
        self.preset = preset      # 預設時間 (秒)
        self.accumulated = 0      # 累計時間 (ET)
        self.input = False        # 輸入接點 (IN)
        self.output = False       # 輸出線圈 (Q)
        self.last_scan = time.time()

    def scan(self, input_signal):
        """每次掃描週期呼叫一次，模擬 PLC 掃描"""
        now = time.time()
        elapsed = now - self.last_scan
        self.last_scan = now

        self.input = input_signal

        if self.input:
            self.accumulated += elapsed
            if self.accumulated >= self.preset:
                self.accumulated = self.preset
                self.output = True
        else:
            self.accumulated = 0
            self.output = False

        return self.output


# --- 示範：5 秒延遲計時器 ---
timer = TON(preset=5)
print("=== TON Timer Demo (preset=5s) ===\n")

scans = [True]*3 + [True]*3   # 模擬 6 次掃描 (每次約 1 秒)
for i, signal in enumerate(scans):
    result = timer.scan(signal)
    print(f"Scan {i+1} | IN={signal} | ET={timer.accumulated:.1f}s | Q={result}")
    time.sleep(1)

print("\n計時器 OFF (IN=False)")
timer.scan(False)
print(f"IN=False | ET={timer.accumulated:.1f}s | Q={timer.output}")
