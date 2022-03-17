import rev
import commands2
import ports
from wpilib import DigitalInput, RobotBase
from utils.subsystembase import SubsystemBase
import properties
from utils.sparkmaxsim import SparkMaxSim


class Grimpeur(SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self._switch_bas = DigitalInput(ports.grimpeur_switch_principal_bas)

        self._switch_bas_secondaire = DigitalInput(ports.grimpeur_switch_secondaire_bas)
        self._switch_haut_secondaire = DigitalInput(ports.grimpeur_switch_secondaire_haut)

        self.addChild("SwitchBas", self._switch_bas)
        self.addChild("SwitchBasSecondaire", self._switch_bas_secondaire)
        self.addChild("SwitchHautSecondaire", self._switch_haut_secondaire)

        # Motors

        self._motor_primaire = rev.CANSparkMax(ports.grimpeur_moteur_principal_droit,
                                               rev.CANSparkMax.MotorType.kBrushless)
        self._encoder_primaire = self._motor_primaire.getEncoder()
        self._motor_primaire_follower = rev.CANSparkMax(ports.grimpeur_moteur_principal_gauche,
                                                        rev.CANSparkMax.MotorType.kBrushless)
        self._motor_primaire_follower.follow(self._motor_primaire, invert=False)

        self._motor_secondaire = rev.CANSparkMax(ports.grimpeur_moteur_secondaire,
                                                 rev.CANSparkMax.MotorType.kBrushless)
        self._encoder_secondaire = self._motor_secondaire.getEncoder()

        if RobotBase.isSimulation():
            self._motor_primaire_sim = SparkMaxSim(self._motor_primaire_follower)
            self._motor_primaire_follower_sim = SparkMaxSim(self._motor_primaire)
            self._motor_secondaire_sim = SparkMaxSim(self._motor_secondaire)

    def simulationPeriodic(self):
        self._motor_primaire_sim.setVelocity(self._motor_primaire.get())
        self._motor_primaire_follower_sim.setVelocity(self._motor_primaire_follower.get())
        self._motor_secondaire_sim.setVelocity(self._motor_secondaire.get())

    def monter(self):
        self._motor_primaire.set(properties.values.grimpeur_vitesse_monter)

    def descend(self):
        self._motor_primaire.set(properties.values.vitesse_grimpeur_descend)

    def monter_secondaire(self):
        self._motor_secondaire.set(properties.values.grimpeur_vitesse_monter_secondaire)

    def descend_secondaire(self):
        self._motor_secondaire.set(properties.values.vitesse_grimpeur_descend_secondaire)

    def stop(self):
        self._motor_primaire.set(0)
        self._motor_secondaire.set(0)

    def getPositionSecondaire(self):
        return self._encoder_secondaire.getPosition()

    def getPositionPrincipale(self):
        return self._encoder_primaire.getPosition()

    def resetEncoder(self):
        self._motor_primaire.restoreFactoryDefaults()
