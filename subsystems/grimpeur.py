import rev
import wpilib
import wpiutil

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
        self._motor_primaire.restoreFactoryDefaults()
        self._motor_primaire.setInverted(True)
        self._encoder_primaire = self._motor_primaire.getEncoder()

        self._motor_primaire_follower = rev.CANSparkMax(ports.grimpeur_moteur_principal_gauche,
                                                        rev.CANSparkMax.MotorType.kBrushless)
        self._motor_primaire_follower.restoreFactoryDefaults()
        self._motor_primaire_follower.follow(self._motor_primaire, invert=True)

        self._motor_secondaire = rev.CANSparkMax(ports.grimpeur_moteur_secondaire,
                                                 rev.CANSparkMax.MotorType.kBrushless)
        self._motor_secondaire.restoreFactoryDefaults()
        self._motor_secondaire.setInverted(True)
        self._encoder_secondaire = self._motor_secondaire.getEncoder()

        if RobotBase.isSimulation():
            self._motor_primaire_sim = SparkMaxSim(self._motor_primaire_follower)
            self._motor_primaire_follower_sim = SparkMaxSim(self._motor_primaire)
            self._motor_secondaire_sim = SparkMaxSim(self._motor_secondaire)

    def periodic(self) -> None:
        wpilib.SmartDashboard.putNumber("Encodeur Primaire", self.getPositionPrincipale())
        wpilib.SmartDashboard.putNumber("Encodeur Secondaire", self.getPositionSecondaire())

    def simulationPeriodic(self):
        self._motor_primaire_sim.setVelocity(self._motor_primaire.get())
        self._motor_primaire_follower_sim.setVelocity(self._motor_primaire_follower.get())
        self._motor_secondaire_sim.setVelocity(self._motor_secondaire.get())

    def monter(self):
        self._motor_primaire.set(properties.values.grimpeur_vitesse_monter)

    def descend(self):
        self._motor_primaire.set(properties.values.grimpeur_vitesse_descend)

    def monter_secondaire(self):
        self._motor_secondaire.set(properties.values.grimpeur_vitesse_monter_secondaire)

    def descend_secondaire(self):
        self._motor_secondaire.set(properties.values.grimpeur_vitesse_descend_secondaire)

    def stop(self):
        self._motor_primaire.set(0)
        self._motor_secondaire.set(0)

    def getPositionSecondaire(self):
        return self._encoder_secondaire.getPosition()

    def getSwitchBas(self):
        return not self._switch_bas.get()

    def getSwitchBasSecondaire(self) -> bool:
        return self._switch_bas_secondaire.get()

    def getSwitchHautSecondaire(self) -> bool:
        return self._switch_haut_secondaire.get()

    def getPositionPrincipale(self):
        return self._encoder_primaire.getPosition()

    def resetEncoder(self):
        self._encoder_primaire.setPosition(0)

    # def initSendable(self, builder: wpiutil.SendableBuilder) -> None:
    #     super(Grimpeur, self).initSendable(builder)
    #     builder.addDoubleProperty("Encoder Secondaire", self.getPositionSecondaire, None)
