from machine import Pin, I2C
import dht
import time
import ntptime
import network
import urequests
import json
from libs.bmp180 import BMP180
import config

# --- センサー初期化 ---
led = Pin('LED', Pin.OUT)
dht11 = dht.DHT11(Pin(13))
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=100000)
bmp = BMP180(i2c)
bmp.oversample_sett = 3

prev_pressure = None


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("WiFi接続中...")
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("WiFi接続完了:", wlan.ifconfig()[0])


def send_to_discord(message):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = json.dumps({"content": message}).encode("utf-8")
    led.off()
    try:
        res = urequests.post(config.DISCORD_WEBHOOK_URL, headers=headers, data=data)
        print("Discord レスポンス:", res.status_code)
        if res.status_code not in (200, 204):
            print("レスポンス本文:", res.text)
        res.close()
    except Exception as e:
        print("Discord送信失敗:", e)
    led.on()


def now_jst():
    t = time.localtime(time.time() + 9 * 3600)
    return "--- {}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5])


# --- WiFi接続・NTP同期・LED ON ---
connect_wifi()
ntptime.host = "ntp.nict.jp"
ntptime.settime()
led.on()
print("センサーデータ送信開始")

while True:
    lines = [now_jst()]

    # DHT11 読み取り（温度・湿度）
    try:
        dht11.measure()
        lines.append("🌡 DHT11温度: {}°C  💧 湿度: {}%".format(
            dht11.temperature(), dht11.humidity()))
    except OSError as e:
        lines.append("⚠️ DHT11読み取り失敗: {}".format(e))

    # BMP180 読み取り（温度・気圧・気圧変化量）
    try:
        bmp.blocking_read()
        pressure = bmp.pressure / 100  # hPa
        if prev_pressure is None:
            delta_str = "--"
        else:
            delta = pressure - prev_pressure
            delta_str = "{:+.2f}hPa".format(delta)
        prev_pressure = pressure
        lines.append("🌡 BMP180温度: {:.1f}°C  🌬 気圧: {:.2f}hPa  (変化: {})".format(
            bmp.temperature, pressure, delta_str))
    except Exception as e:
        lines.append("⚠️ BMP180読み取り失敗: {}".format(e))

    message = "\n".join(lines)
    print(message)
    send_to_discord(message)

    time.sleep(300)
