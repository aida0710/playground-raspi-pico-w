from machine import Pin, I2C
import time
from libs.bmp180 import BMP180

# https://github.com/micropython-IMU/micropython-bmp180
# https://awesome-micropython.com/

led = Pin('LED', Pin.OUT)

# I2Cの初期化 (Raspberry Pi Pico の場合)
# SDA: GP0, SCL: GP1 を使用
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=100000)

# BMP180センサーの初期化
bmp = BMP180(i2c)

# オーバーサンプリング設定 (0-3, 高いほど精度が上がるが時間がかかる)
bmp.oversample_sett = 3

# 基準気圧の設定 (海面気圧 hPa → Pa)
bmp.baseline = 101325.0

print("BMP180 センサー読み取り開始")
print("-" * 40)

while True:
    # センサーデータの読み取り
    bmp.blocking_read()

    temp = bmp.temperature      # 温度 (℃)
    pressure = bmp.pressure     # 気圧 (Pa)
    altitude = bmp.altitude     # 高度 (m)

    print(f"温度: {temp:.1f} ℃")
    print(f"気圧: {pressure/100:.2f} hPa")
    print(f"高度: {altitude:.1f} m")
    print("-" * 40)

    # LEDを点滅させて動作確認
    led.toggle()

    time.sleep(2)

