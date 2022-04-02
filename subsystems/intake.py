import wpilib

import ports
import properties
from utils.subsystembase import SubsystemBase


class Intake(SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        # Motors
        self._motor_intake = wpilib.PWMVictorSPX(ports.intake_moteur_intake)
        self._motor_intake.setInverted(True)
        self._motor_convoyeur = wpilib.PWMVictorSPX(ports.intake_moteur_transporter)
        self._motor_convoyeur.setInverted(True)
        self.addChild("Motor Intake", self._motor_intake)
        self.addChild("Motor Convoyeur", self._motor_convoyeur)

        # Sensors
        self._ultrasonic_bas = wpilib.AnalogPotentiometer(ports.intake_ultrasonic_bas)
        self._ultrasonic_haut = wpilib.AnalogPotentiometer(ports.intake_ultrasonic_haut)
        self.addChild("Ultrason bas", self._ultrasonic_bas)
        self.addChild("Ultrason haut", self._ultrasonic_haut)

    def activerIntake(self):
        self._motor_intake.set(properties.values.intake_speed)

    def stopIntake(self):
        self._motor_intake.set(0)

    def activerConvoyeurLent(self):
        self._motor_convoyeur.set(properties.values.intake_convoyeur_speed_lent)

    def activerConvoyeurRapide(self):
        self._motor_convoyeur.set(properties.values.intake_convoyeur_speed_rapide)

    def stopConvoyeur(self):
        self._motor_convoyeur.set(0)

    def hasBallIntake(self) -> bool:
        return self._ultrasonic_bas.get() < properties.values.intake_ultrason_bas_threshold

    def hasBallConvoyeur(self) -> bool:
        return self._ultrasonic_haut.get() < properties.values.intake_ultrason_haut_threshold

    def ballCount(self) -> int:
        if self.hasBallConvoyeur():
            if self.hasBallIntake():
                return 2
            return 1
        return 0

    def ejecter(self):
        self._motor_intake.set(properties.values.intake_reverse_speed)

    def getIntakeSpeed(self):
        return self._motor_intake.get()

    def periodic(self):
        wpilib.SmartDashboard.putBoolean("Sensor intake", self.hasBallIntake())
        wpilib.SmartDashboard.putBoolean("Sensor transporter", self.hasBallConvoyeur())
        wpilib.SmartDashboard.putBoolean("Motor intake", self._motor_intake.get() > 0)
        wpilib.SmartDashboard.putBoolean("Motor transporter", self._motor_convoyeur.get() > 0)
