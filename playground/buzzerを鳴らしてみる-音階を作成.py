from machine import Pin
import time

buzzer = Pin(15, Pin.OUT)

NOTE = {
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349,
    'G4': 392, 'A4': 440, 'B4': 494, 'C5': 523,
    'REST': 0  # 休符
}

def tone(frequency, duration):
    if frequency == 0:  # 休符
        time.sleep(duration)
        return
    period = 1 / frequency
    half_period = period / 2
    cycles = int(frequency * duration)
    for _ in range(cycles):
        buzzer.on()
        time.sleep(half_period)
        buzzer.off()
        time.sleep(half_period)

kaeru = [
    ('C4', 0.3), ('D4', 0.3), ('E4', 0.3), ('F4', 0.3),
    ('E4', 0.3), ('D4', 0.3), ('C4', 0.6),
]

for note, duration in kaeru:
    tone(NOTE[note], duration)
    time.sleep(0.05)

buzzer.off()
# 正直音を聞いても違いがよくわからんかった