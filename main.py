import socket
import uasyncio as asyncio
import machine
import time
import logging

from Car import Car

loop = asyncio.get_event_loop()
log = None
car_actions = None

# TCP Server endpoint
HOST = '0.0.0.0'
PORT = 54321

# Car default global variables
CAR_CONF = 'car.json'


def init_logger():
    global log

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger("main")


@asyncio.coroutine
def handle_car_data(reader, writer):
    global log
    global car_actions

    addr = writer.get_extra_info('peername')
    log.info("[HANDLE_CAR_DATA] Client arrived: {} ".format(addr))

    while 1:
        data = await reader.read()

        message = data.decode()
        if (len(message)) == 0:
            # Socket was closed from the other side
            log.debug("[HANDLE_CAR_DATA] Message received is empty. "
                      "Probably client socket was closed. Aborting coroutine")
            break

        log.debug("[HANDLE_CAR_DATA] Received {} from {}".format(message, addr))

        if message == 'EXIT':
            log.info('[HANDLE_CAR_DATA] EXIT message received. Close the client socket')
            writer.aclose()
            break

        # If the word is not exit, process the words received
        actions = message.split('|')
        for action in actions:
            try:
                log.info('[HANDLE_CAR_DATA] Proceed to execute action {}'.format(action))
                car_actions[action]()
            except KeyError:
                pass

    log.info('[HANDLE_CAR_DATA] Exiting coroutine')
    if message == 'EXIT':
        loop.stop()


def main():
    global car_actions
    init_logger()

    # Initialize the car and stop it from moving
    car = Car(CAR_CONF)
    car.stop()

    # Define the actions that the Car supports
    car_actions = {
        "FORWARD": car.forward,
        "REVERSE": car.reverse,
        "TURN_LEFT": car.turn_left,
        "TURN_RIGHT": car.turn_right,
        "ACCELERATE": car.accelerate,
        "DECELERATE": car.decelerate,
        "STOP": car.stop
    }

    coro = asyncio.start_server(handle_car_data, host=HOST, port=PORT)
    log.info('[HANDLE_DATA] Starting uasyncio event loop')
    loop.create_task(coro)
    loop.run_forever()
    log.info('[HANDLE_DATA] Finishing uasyncio event loop')
    loop.close()

    # Stop the car to avoid crashes ;)
    car.stop()

if __name__ == "__main__":
    main()
