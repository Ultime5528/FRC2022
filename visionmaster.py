import threading

from networktables.util import NetworkTables

from visioncargo import cargo_loop
from visionhub import hub_loop

isConnected = threading.Condition()
notified = [False]


def connectionListener(connected, info):
    with isConnected:
        notified[0] = True
        isConnected.notify()


def main():
    NetworkTables.initialize(server="10.55.28.2")
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    # with isConnected:
    #     print("Waiting for connection...")
    #     if not notified[0]:
    #         isConnected.wait()
    # print("Connected!")

    hub_loop_gen = hub_loop()
    # cargo_loop_gen = cargo_loop()

    while True:
        next(hub_loop_gen)
        # next(cargo_loop_gen)


if __name__ == '__main__':
    main()
