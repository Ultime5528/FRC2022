import wpilib
from utils.subsystembase import SubsystemBase
import ports
import properties


class Intake(SubsystemBase):
    def __init__(self) -> None:
        super().__init__()

        # Motors
        self._intakeMotor = wpilib.PWMVictorSPX(ports.intake_moteur_intake)
        self._transporterMotor = wpilib.PWMVictorSPX(ports.intake_moteur_transporter)
        self.addChild("IntakeMotor", self._intakeMotor)
        self.addChild("TransporterMotor", self._transporterMotor)
        # Sensors
        self._sensorIntake = wpilib.DigitalInput(ports.intake_sensor_bas)
        self._sensorTransporter = wpilib.DigitalInput(ports.intake_sensor_haut)
        self.addChild("SensorIntake", self._sensorIntake)
        self.addChild("SensorTransporter", self._sensorTransporter)

    def activerIntake(self):
        self._intakeMotor.set(properties.values.intake_speed)

    def activerTransporter(self):
        self._transporterMotor.set(properties.values.transporter_speed)

    def stopIntake(self):
        self._intakeMotor.set(0)

    def stopTransporter(self):
        self._transporterMotor.set(0)

    def hasBallIntake(self) -> bool:
        return self._sensorIntake.get()

    def hasBallTransporter(self) -> bool:
        return self._sensorTransporter.get()

    def ejecter(self):
        self._intakeMotor.set(properties.values.intake_reverse_speed)
        self._transporterMotor.set(properties.values.transporter_reverse_speed)

    def periodic(self):
        wpilib.SmartDashboard.putBoolean("Sensor intake", self.hasBallIntake())
        wpilib.SmartDashboard.putBoolean("Sensor transporter", self.hasBallTransporter())
        wpilib.SmartDashboard.putBoolean("Motor intake", self._intakeMotor.get() > 0)
        wpilib.SmartDashboard.putBoolean("Motor transporter", self._transporterMotor.get() > 0)
