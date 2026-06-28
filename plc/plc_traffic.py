# plc_traffic.py — PLC 交通燈控制 (Traffic Light)
# 模擬十字路口紅綠燈時序控制，使用計時器 + 自鎖電路概念

import time

# --- 紅綠燈狀態枚舉 ---
class TrafficLight:
    """單一方向的紅綠燈"""
    RED, GREEN, YELLOW = "RED", "GREEN", "YELLOW"

    def __init__(self, name):
        self.name = name
        self.state = self.RED   # 初始紅燈

    def set_state(self, state):
        self.state = state
        symbol = {"RED": "🔴", "GREEN": "🟢", "YELLOW": "🟡"}
        print(f"  [{self.name}] {symbol.get(state, '?')} {state}")


# --- 十字路口控制器 (模擬 PLC 掃描週期) ---
class TrafficController:
    """
    簡化十字路口時序:
    NS 綠 5s → NS 黃 1s → 全紅 1s → EW 綠 5s → EW 黃 1s → 循環
    """
    def __init__(self):
        self.ns = TrafficLight("North-South")
        self.ew = TrafficLight("East-West")
        self.timer = 0
        self.cycle_step = 0
        # 時序表 (方向, 狀態, 持續秒數)
        self.sequence = [
            ("NS", "GREEN",  5),   # Step 0: NS 綠燈
            ("NS", "YELLOW", 1),   # Step 1: NS 黃燈
            ("ALL", "RED",   1),   # Step 2: 全紅 (清空路口)
            ("EW", "GREEN",  5),   # Step 3: EW 綠燈
            ("EW", "YELLOW", 1),   # Step 4: EW 黃燈
            ("ALL", "RED",   1),   # Step 5: 全紅 → 回到 Step 0
        ]

    def scan(self):
        """每次掃描週期 (1秒) 執行"""
        direction, state, duration = self.sequence[self.cycle_step]

        if self.timer == 0:
            # 切換狀態
            if direction == "ALL":
                self.ns.set_state("RED")
                self.ew.set_state("RED")
            elif direction == "NS":
                self.ns.set_state(state)
                self.ew.set_state("RED")
            elif direction == "EW":
                self.ew.set_state(state)
                self.ns.set_state("RED")

        self.timer += 1
        if self.timer >= duration:
            self.timer = 0
            self.cycle_step = (self.cycle_step + 1) % len(self.sequence)


# --- 示範：跑兩個完整循環 ---
controller = TrafficController()
print("=== PLC Traffic Light Demo (2 cycles) ===\n")

for sec in range(1, 29):   # 一個循環 14s，跑兩次
    print(f"\n--- Second {sec} ---")
    controller.scan()
    time.sleep(1)

print("\n=== 交通燈循環結束 ===")
