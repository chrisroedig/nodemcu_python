import time
import machine
import neopixel
from support import led_patterns


np = neopixel.NeoPixel(machine.Pin(4), 32, bpp=4)
colors1 = [
    (0, 0, 125, 0),
    (0, 0, 60, 0),
    (0, 0, 20, 0),
    (0, 0, 05, 0)
    ]
wave1 = led_patterns.Wave(pixel_count=32, colors=colors1, neopixel=np, period=2.0, speed=1.0)
colors2 = [
    (80, 0, 0, 0),
    (40, 0, 0, 0),
    (10, 0, 0, 0),
    (05, 0, 0, 0)
    ]
wave2 = led_patterns.Wave(pixel_count=32, colors=colors2, neopixel=np, period=2.0, speed=-2.0)


def run():
    print('application running')
    while True:
        step(True)

def step(print_time=False):
    t = time.ticks_ms()
    wave1.assign_to(0, 16)
    wave2.assign_to(16, 31)
    wave1.update_time_phase()
    wave2.update_time_phase()
    np.write()
