class Base:
    motor = None

    right_angle = None

    def __init__(self, motor):
        self.motor = motor

        self.right_angle = self.motor.count_per_rot / 4

        self.motor.stop_action = 'brake'
        self.motor.ramp_down_sp = 1000
        self.motor.ramp_up_sp = 0
        self.motor.position = 0

    def turn(self, k=1):
        k %= 4

        if k == 0:
            return

        new_position = self.motor.position
        step = self.right_angle
        new_position -= (new_position + step / 2) % step - step / 2
        new_position += k * step

        over_turn = 0.1 * self.right_angle

        self.motor.run_to_abs_pos(speed_sp = 1000, position_sp=new_position + over_turn)
        self.motor.wait_while('running', timeout=1000)

        self.motor.run_to_abs_pos(speed_sp = 500, position_sp=new_position)
        self.motor.wait_while('running', timeout=1000)

        self.motor.stop()

    def semi_turn(self, adjust=0, k=1):
        new_position = self.motor.position
        step = self.right_angle / 2
        new_position -= (new_position + step / 2) % step - step / 2
        new_position += k * step + adjust

        self.motor.run_to_abs_pos(speed_sp = 150, position_sp=new_position)
        self.motor.wait_while('running', timeout=100)
        self.motor.stop()

    def shake(self):
        over_turn = 0.3 * self.right_angle

        self.motor.run_to_rel_pos(speed_sp = 1000, position_sp=over_turn)
        self.motor.wait_while('running', timeout=1000)

        self.motor.run_to_rel_pos(speed_sp = 1000, position_sp=-over_turn)
        self.motor.wait_while('running', timeout=1000)
        self.motor.stop()
