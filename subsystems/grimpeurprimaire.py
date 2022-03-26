import rev
import wpilib
from wpilib.simulation import DIOSim

import ports
from wpilib import DigitalInput, RobotBase
from utils.subsystembase import SubsystemBase
import properties
from utils.sparkmaxsim import SparkMaxSim


class GrimpeurPrimaire(SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self._switch_bas = DigitalInput(ports.grimpeur_switch_principal_bas)
        self.addChild("SwitchBas", self._switch_bas)

        # Motors
        self._motor_primaire = rev.CANSparkMax(ports.grimpeur_moteur_principal_droit,
                                               rev.CANSparkMax.MotorType.kBrushless)
        self._motor_primaire.restoreFactoryDefaults()
        self._motor_primaire.setInverted(True)
        self._motor_primaire.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self._encoder_primaire = self._motor_primaire.getEncoder()

        self._motor_primaire_follower = rev.CANSparkMax(ports.grimpeur_moteur_principal_gauche,
                                                        rev.CANSparkMax.MotorType.kBrushless)
        self._motor_primaire_follower.restoreFactoryDefaults()
        self._motor_primaire_follower.follow(self._motor_primaire, invert=True)
        self._motor_primaire_follower.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)

        if RobotBase.isSimulation():
            self._motor_primaire_sim = SparkMaxSim(self._motor_primaire)
            self._switch_bas_sim = DIOSim(self._switch_bas)

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("Encodeur Primaire", self.getPosition())

    def simulationPeriodic(self):
        self._motor_primaire_sim.setVelocity(self._motor_primaire.get())
        self._motor_primaire_sim.setPosition(self._motor_primaire_sim.getPosition() + self._motor_primaire.get())
        if self._motor_primaire_sim.getPosition() <= 0:
            self._switch_bas_sim.setValue(False)
        else:
            self._switch_bas_sim.setValue(True)

    def set_moteur(self, speed: float):
        self._motor_primaire.set(speed)

    def monter(self):
        self._motor_primaire.set(properties.values.grimpeur_primaire_vitesse_monter)

    def descendre(self):
        self._motor_primaire.set(properties.values.grimpeur_primaire_vitesse_descendre)

    def stop(self):
        self._motor_primaire.set(0)

    def getSwitchBas(self):
        return not self._switch_bas.get()

    def getPosition(self):
        return self._encoder_primaire.getPosition()

    def reset_encoder(self):
        self._encoder_primaire.setPosition(0)
