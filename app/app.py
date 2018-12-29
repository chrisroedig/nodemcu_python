import time
from machine import Pin

p2 = Pin(2, Pin.OUT)
def run():
    print('application runnning')
    p2.on()
    while True:
        time.sleep(1)
        blink()

def blink():
    p2.off()
    time.sleep(0.05)
    p2.on()
    time.sleep(0.05)
    p2.off()
    time.sleep(0.05)
    p2.on()
