import rev
import commands2
import ports
from wpilib import DigitalInput, RobotBase

#import properties
import properties
from utils.sparkmaxsim import SparkMaxSim


class Grimpeur(commands2.SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        self.switch_bas = DigitalInput(ports.digital_switch_grimpeur_bas)
        self.switch_haut = DigitalInput(ports.digital_switch_grimpeur_haut)
        # Motors
        self.bras_droit = rev.CANSparkMax(ports.grimpeur_motor_1, rev.CANSparkMax.MotorType.kBrushless)
        self.bras_gauche = rev.CANSparkMax(ports.grimpeur_motor_2, rev.CANSparkMax.MotorType.kBrushless)
        self.bras_droit.follow(self.bras_gauche, invert=False)

        if RobotBase.isSimulation():
            self.motor_front_left_sim = SparkMaxSim(self.bras_droit)
            self.motor_front_right_sim = SparkMaxSim(self.bras_gauche)

    def simulationPeriodic(self):
        self.motor_front_left_sim.setVelocity(self.bras_gauche.get())
        self.motor_front_right_sim.setVelocity(self.bras_droit.get())

    def monter(self):
        self.bras_gauche.set(properties.vitesse_grimpeur_monter)

    def descend(self):
        self.bras_gauche.set(properties.vitesse_grimpeur_descend)

    def stop(self):
        self.bras_gauche.set(0)
