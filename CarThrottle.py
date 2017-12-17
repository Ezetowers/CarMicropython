import machine


class CarThrottle(object):
    DEFAULT_FREQ = 500
    DEFAULT_PWM_STEP = 100
    PWM_MAX_VALUE = 1023
    PWM_MIN_VALUE = 0

    def __init__(self, pin_pwm, pwm_step=DEFAULT_PWM_STEP):
        self._pin_pwm = machine.PWM(machine.Pin(pin_pwm))

        # default values
        self._pin_pwm.freq(CarThrottle.DEFAULT_FREQ)
        self._pwm_value = 0
        self._pwm_step = pwm_step
        self._pin_pwm.duty(self._pwm_value)

    def accelerate(self):
        self._pwm_value += self._pwm_step

        if self._pwm_value > CarThrottle.PWM_MAX_VALUE:
            self._pwm_value = CarThrottle.PWM_MAX_VALUE

        self._pin_pwm.duty(self._pwm_value)

    def decelerate(self):
        self._pwm_value -= self._pwm_step

        if self._pwm_value < CarThrottle.PWM_MIN_VALUE:
            self._pwm_value = CarThrottle.PWM_MIN_VALUE

        self._pin_pwm.duty(self._pwm_value)
