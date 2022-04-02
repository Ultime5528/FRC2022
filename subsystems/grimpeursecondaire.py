import rev
import wpilib
from wpilib import DigitalInput, RobotBase
from wpilib.simulation import DIOSim

import ports
import properties
from utils.sparkmaxsim import SparkMaxSim
from utils.sparkmaxutil import configure_leader
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
        configure_leader(self._motor_secondaire, "brake", inverted=True)
        self._encoder_secondaire = self._motor_secondaire.getEncoder()

        if RobotBase.isSimulation():
            self._motor_secondaire_sim = SparkMaxSim(self._motor_secondaire)
            self._switch_bas_sim = DIOSim(self._switch_bas_secondaire)
            self._switch_haut_sim = DIOSim(self._switch_haut_secondaire)

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("Encodeur Secondaire", self.getPosition())

    def simulationPeriodic(self):
        self._motor_secondaire_sim.setVelocity(self._motor_secondaire.get())
        self._motor_secondaire_sim.setPosition(self._motor_secondaire_sim.getPosition() + self._motor_secondaire.get())

        if self._motor_secondaire_sim.getPosition() <= 0:
            self._switch_bas_sim.setValue(True)
        else:
            self._switch_bas_sim.setValue(False)

        if self._motor_secondaire_sim.getPosition() >= properties.values.grimpeur_secondaire_hauteur_max:
            self._switch_haut_sim.setValue(True)
        else:
            self._switch_haut_sim.setValue(False)

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
