from machine import Pin
import time

led = Pin('LED', Pin.OUT)
buzzer = Pin(15, Pin.OUT)

def tone_change(frequency, duration):
    period = 1 / frequency
    half_period = period / 2
    cycles = int(frequency * duration)

    for _ in range(cycles):
        buzzer.on()
        time.sleep(half_period)
        buzzer.off()
        time.sleep(half_period)

while True:
    led.on()
    tone_change(1000, 0.5)
    time.sleep(1)
    led.off()
    tone_change(500, 0.5)
    time.sleep(1)

