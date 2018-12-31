import math
import time

class Uniform():
    def __init__(self, **kwargs):
        self.pixel_count = kwargs.get('pixel_count', 32)
        self.colors = kwargs.get('colors', [(0,0,0,0), (255,255,255,255)])
        self.gradient_steps = kwargs.get('gradient_steps', 100)
        self.color_cache = None
        self.current_mix = 0.0
        self.neopixel = kwargs.get('neopixel')
        self.build_color_cache()

    def __getitem__(self, key):
        if type(key) == int:
            return self.pixels(key)
        return self.pixels(key.start, key.stop)
    def assign_to_all(self):
        self.assign_to(0, self.pixel_count)

    def assign_to(self, start_pix, end_pix):
        for i in range(start_pix, end_pix):
            p = self.pixel(i)
            self.neopixel.buf[4*i : 4*(i+1)] = bytearray(p)

    def pixel(self, index):
        return self.fixed_color(self.current_mix)

    def pixels(self, start, stop=None):
        if stop is None:
            return self.fixed_color(self.current_mix)
        return [self.fixed_color(self.current_mix)] * (stop-start)

    def fixed_color(self, mix):
        return self.color_cache[min(int(round(mix*self.gradient_steps)),self.gradient_steps-1)]

    def calc_gradient_color(self, gradient_pos):
        n = len(self.colors)
        a_color = self.colors[max(0,int(math.floor(n*gradient_pos))-1)]
        b_color = self.colors[min((n-1),int(math.ceil(n*gradient_pos))-1)]
        mix = n*gradient_pos - math.floor(n*gradient_pos)
        return tuple(self.calc_mixed_color(a_color, b_color, mix))

    def calc_mixed_color(self, a_color, b_color, mix):
        color = [0] * len(a_color)
        for i, c in enumerate(color):
            color[i] = int(a_color[i] * (1.0-mix) + b_color[i] * mix)
        return color

    def build_color_cache(self):
        ccache = []
        for i in range(self.gradient_steps):
            m = i / float(self.gradient_steps)
            ccache.append(self.calc_gradient_color(m))
        self.color_cache = tuple(ccache)

class Wave(Uniform):
    def __init__(self, **kwargs):
        Uniform.__init__(self,**kwargs)
        self.speed = kwargs.get('speed', .25)
        self.period = kwargs.get('period', None)
        if self.period is None:
            self.period = math.pi
        self.phase_steps = 100
        self.phase_pitch = float(self.phase_steps)/(2.0*math.pi)
        self.phase = 0.0
        self.time = float(time.time())
        self.mod_depth = .5
        if time.__name__ == 'utime':
            self.time_fn = lambda : time.ticks_ms() / 1000.0
        else:
            self.time_fn = time.time
        self.setup()

    def setup(self):
        self.theta = [ float(i) / self.period for i in range(self.pixel_count)]
        self.amp = [
            0.5 + self.mod_depth * math.sin(float(i)/self.phase_pitch)
            for i in range(self.phase_steps)
        ]
    def pixel(self, pixel_id):
        phase_id = int((self.phase + self.theta[pixel_id])*self.phase_pitch) % self.phase_steps
        col = self.fixed_color(self.amp[phase_id])
        return col

    def pixels(self, start, stop=None):
        if stop is None:
            return self.pixel(start)
        return [self.pixel(i) for i in range(start, stop)]

    def update_time_phase(self):
        t = float(self.time_fn())
        dt = t - self.time
        self.time = t
        self.phase = self.phase + dt * self.speed
