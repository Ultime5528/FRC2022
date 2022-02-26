#!/usr/bin/env python3
import wpilib
import commands2
from commands2.button import JoystickButton

from commands.descendresecondaire import DescendreSecondaire
from commands.monterintake import MonterIntake
from commands.monterprimaire import MonterPrimaire
from commands.descendprimaire import DescendPrimaire
from subsystems.visiontargets import VisionTargets
from subsystems.intake import Intake
from subsystems.basepilotable import BasePilotable
from commands.prendreballon import PrendreBallon
from subsystems.shooter import Shooter
from subsystems.grimpeur import Grimpeur

from commands.piloter import Piloter
from commands.viserhub import ViserHub
from commands.shoot import Shoot


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        wpilib.CameraServer.launch("visionhub.py:main")

        self.stick = wpilib.Joystick(0)

        self.intake = Intake()
        self.base_pilotable = BasePilotable()
        self.vision_targets = VisionTargets()
        self.shooter = Shooter()
        self.grimpeur = Grimpeur()
        self.base_pilotable.setDefaultCommand(Piloter(self.base_pilotable, self.stick))

        JoystickButton(self.stick, 3).whenHeld(PrendreBallon(self.intake))
        JoystickButton(self.stick, 4).whenPressed(ViserHub(self.base_pilotable, self.vision_targets))
        wpilib.SmartDashboard.putData("Shoot", Shoot(self.shooter, self.stick, 3000, 3000))
        wpilib.SmartDashboard.putData("grimper", MonterPrimaire(self.grimpeur))
        wpilib.SmartDashboard.putData("descendre", DescendPrimaire(self.grimpeur))
        wpilib.SmartDashboard.putData("descendre secondaire", DescendreSecondaire(self.grimpeur))
        wpilib.SmartDashboard.putData("monter intake", MonterIntake(self.grimpeur))


if __name__ == "__main__":
    wpilib.run(Robot)
