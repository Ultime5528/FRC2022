import rev
import wpilib
from wpilib import DigitalInput, RobotBase

import ports
import properties
from utils.sparkmaxsim import SparkMaxSim
from utils.subsystembase import SubsystemBase


class GrimpeurSecondaire(SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self._switch_bas_secondaire = DigitalInput(ports.grimpeur_secondaire_switch_bas)
        self._switch_haut_secondaire = DigitalInput(ports.grimpeur_secondaire_switch_haut)

        self.addChild("SwitchBasSecondaire", self._switch_bas_secondaire)
        self.addChild("SwitchHautSecondaire", self._switch_haut_secondaire)

        # Motors

        self._motor_secondaire = rev.CANSparkMax(ports.grimpeur_moteur_secondaire,
                                                 rev.CANSparkMax.MotorType.kBrushless)
        self._motor_secondaire.restoreFactoryDefaults()
        self._motor_secondaire.setInverted(True)
        self._motor_secondaire.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self._encoder_secondaire = self._motor_secondaire.getEncoder()

        if RobotBase.isSimulation():
            self._motor_secondaire_sim = SparkMaxSim(self._motor_secondaire)

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("Encodeur Secondaire", self.getPosition())

    def simulationPeriodic(self):
        self._motor_secondaire_sim.setVelocity(self._motor_secondaire.get())

    def set_moteur(self, speed: float):
        self._motor_secondaire.set(speed)

    def monter(self):
        self._motor_secondaire.set(properties.values.grimpeur_secondaire_vitesse_monter)

    def descendre(self):
        self._motor_secondaire.set(properties.values.grimpeur_secondaire_vitesse_descendre)

    def stop(self):
        self._motor_secondaire.set(0)

    def getPosition(self):
        return self._encoder_secondaire.getPosition()

    def getSwitchBas(self) -> bool:
        return self._switch_bas_secondaire.get()

    def getSwitchHaut(self) -> bool:
        return self._switch_haut_secondaire.get()

    def reset_encoder(self):
        self._encoder_secondaire.setPosition(0)
