from CarEngine import CarEngine
from CarThrottle import CarThrottle

import logging
import ujson

log = logging.getLogger("main")


class Car(object):

    def __init__(self, car_conf):

        # TODO: Catch OSError Exception
        json_conf = None
        with open(car_conf, "r") as f:
            json_conf = ujson.loads(f.read())

        # TODO: Check ValueError Exception
        self._left_eng = CarEngine(pin_up=json_conf["left_engine"]["pin_up"],
                                   pin_down=json_conf["left_engine"]["pin_down"])
        self._right_eng = CarEngine(pin_up=json_conf["right_engine"]["pin_up"],
                                    pin_down=json_conf["right_engine"]["pin_down"])
        self._throttle = CarThrottle(pin_pwm=json_conf["throttle"]["pin_pwm"],
                                     pwm_step=json_conf["throttle"]["pwm_step"])

    def forward(self):
        log.debug('[CAR] Proceed to execute action: FORWARD')
        self._left_eng.forward()
        self._right_eng.forward()

    def reverse(self):
        self._left_eng.reverse()
        self._right_eng.reverse()

    def turn_left(self):
        self._left_eng.forward()
        self._right_eng.stop()

    def turn_right(self):
        self._left_eng.stop()
        self._right_eng.forward()

    def stop(self):
        self._left_eng.stop()
        self._right_eng.stop()

    def accelerate(self):
        log.debug('[CAR] Proceed to execute action: ACCELERATE')
        self._throttle.accelerate()

    def decelerate(self):
        self._throttle.decelerate()
