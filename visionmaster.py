from visionhub import hub_loop
from visioncargo import cargo_loop


def main():
    hub_loop_gen = hub_loop()
    cargo_loop_gen = cargo_loop()

    while True:
        next(hub_loop_gen)
        next(cargo_loop_gen)


if __name__ == '__main__':
    main()
