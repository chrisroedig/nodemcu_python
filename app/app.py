import time
from machine import Pin

def run():
    print('application runnning')
    p2 = Pin(2, Pin.OUT)
    p2.off()
    while True:
        p2.on()
        time.sleep(1.85)
        p2.off()
        time.sleep(0.05)
        p2.on()
        time.sleep(0.05)
        p2.off()
        time.sleep(0.05)
