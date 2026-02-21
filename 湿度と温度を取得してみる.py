from machine import Pin
import dht
import time

led = Pin('LED', Pin.OUT)

senser = dht.DHT11(Pin(13))

while True:
    try:
        senser.measure()
        temp = senser.temperature()
        hum = senser.humidity()
        print('温度: {}°C  湿度: {}%'.format(temp, hum))

        if hum > 70:
            led.on()
        else:
            led.off()

    except OSError as e:
        print("センサーの読み取りに失敗しました:", e)

    time.sleep(2)
