import commands2


def basic_subsystem_tests(subsystem: commands2.SubsystemBase):
    assert "frc2::" not in subsystem.getName()
    subsystem.periodic()
    subsystem.simulationPeriodic()
    # TODO Call all methods once?


def basic_command_tests(command: commands2.CommandBase):
    assert "frc2::" not in command.getName()
    command.initialize()
    command.execute()
    assert isinstance(command.isFinished(), bool)
    command.end(False)
    command.end(True)
