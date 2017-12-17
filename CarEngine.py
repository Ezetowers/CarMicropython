import machine


class CarEngine(object):

    def __init__(self, pin_up, pin_down):
        self._pin_up = machine.Pin(pin_up, machine.Pin.OUT)
        self._pin_down = machine.Pin(pin_down, machine.Pin.OUT)

        # default values
        self.stop()

    def forward(self):
        self._pin_up.value(1)
        self._pin_down.value(0)

    def reverse(self):
        self._pin_up.value(0)
        self._pin_down.value(1)

    def stop(self):
        self._pin_up.value(0)
        self._pin_down.value(0)
