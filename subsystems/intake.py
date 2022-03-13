import wpilib
from utils.subsystembase import SubsystemBase
import ports
import properties


class Intake(SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        # Motors
        self._motor_intake = wpilib.PWMVictorSPX(ports.intake_moteur_intake)
        self._motor_convoyeur = wpilib.PWMVictorSPX(ports.intake_moteur_transporter)
        self.addChild("Motor Intake", self._motor_intake)
        self.addChild("Motor Convoyeur", self._motor_convoyeur)

        # Sensors
        self._ultrasonic_bas = wpilib.AnalogPotentiometer(ports.intake_ultrasonic_bas, )
        self._ultrasonic_haut = wpilib.AnalogPotentiometer(ports.intake_ultrasonic_haut)
        self.addChild("Ultrason bas", self._ultrasonic_bas)
        self.addChild("Ultrason haut", self._ultrasonic_haut)

    def activerIntake(self):
        self._motor_intake.set(properties.values.intake_speed)

    def activerTransporter(self):
        self._motor_convoyeur.set(properties.values.transporter_speed)

    def stopIntake(self):
        self._motor_intake.set(0)

    def stopTransporter(self):
        self._motor_convoyeur.set(0)

    def hasBallIntake(self) -> bool:
        return self._ultrasonic_bas.get() > properties.values.intake_ultrason_bas_threshold

    def hasBallTransporter(self) -> bool:
        return self._ultrasonic_bas.get() > properties.values.intake_ultrason_haut_threshold

    def ejecter(self):
        self._motor_intake.set(properties.values.intake_reverse_speed)
        self._motor_convoyeur.set(properties.values.transporter_reverse_speed)

    def periodic(self):
        wpilib.SmartDashboard.putBoolean("Sensor intake", self.hasBallIntake())
        wpilib.SmartDashboard.putBoolean("Sensor transporter", self.hasBallTransporter())
        wpilib.SmartDashboard.putBoolean("Motor intake", self._motor_intake.get() > 0)
        wpilib.SmartDashboard.putBoolean("Motor transporter", self._motor_convoyeur.get() > 0)
