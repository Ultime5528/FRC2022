from visionhub import hub_loop
from visioncargo import cargo_loop

hub_loop = hub_loop()
cargo_loop = cargo_loop()

while True:
    next(hub_loop)
    next(cargo_loop)