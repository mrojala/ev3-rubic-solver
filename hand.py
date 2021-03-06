class Hand:
    motor = None
    sensor = None
    degree = None

    def __init__(self, motor, sensor):
        self.motor = motor
        self.sensor = sensor
        self.sensor.mode = 'RGB-RAW'

        self.degree = self.motor.count_per_rot / 360

        self.reset()

    def reset(self):
        self.motor.ramp_down_sp = 0
        self.motor.ramp_up_sp = 0

        self.motor.stop_action = 'coast'
        self.motor.run_timed(time_sp=2000, speed_sp=-300)
        self.motor.wait_while('running')
        self.motor.stop()
        self.motor.position = 0

        self.rest()

        self.motor.ramp_down_sp = 300
        self.motor.ramp_up_sp = 500

    def run_to_position(self, position, speed, stop_action, slow_ramp=False):
        if slow_ramp:
            self.motor.ramp_down_sp = 5000
            self.motor.ramp_up_sp = 5000
        else:
            self.motor.ramp_down_sp = 300
            self.motor.ramp_up_sp = 500

        self.motor.stop_action = stop_action
        self.motor.run_to_abs_pos(speed_sp=speed, position_sp=position * self.degree)
        self.motor.wait_while('running', timeout=1000)
        self.motor.stop()

    def hold(self):
        self.run_to_position(-5, -1000, 'hold')

    def push(self):
        self.run_to_position(310, 500, 'brake')
        self.motor.wait_while('running', timeout=300)
        self.run_to_position(310, 500, 'brake')
        self.motor.wait_while('running', timeout=100)
        self.motor.stop()

    def rest(self):
        self.run_to_position(140, 1000, 'brake')
        self.motor.wait_while('running', timeout=500)
        self.motor.stop()

    def get_rgb(self):
        return self.sensor.raw

    def measure_position(self, position):
        self.run_to_position(position, 100, 'brake', False)
        return self.get_rgb()

    def measure_center(self, adjust=0):
        return self.measure_position(221 + adjust)

    def measure_corner(self, adjust=0):
        return self.measure_position(203 + adjust)

    def measure_side(self, adjust=0):
        return self.measure_position(212 + adjust)
