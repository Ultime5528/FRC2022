from pyfrc.test_support.controller import TestController as Controller

from commands.grimpeur.bougerprimaire import BougerPrimaire
from robot import Robot
from tests.conftest import basic_subsystem_tests, basic_command_tests


def test_grimpeur_primaire(control: Controller, robot: Robot):
    with control.run_robot():
        basic_subsystem_tests(robot.grimpeur_primaire)
        basic_command_tests(BougerPrimaire.to_max(robot.grimpeur_primaire))
        basic_command_tests(BougerPrimaire.to_clip(robot.grimpeur_primaire))
        # TODO Add all commands
