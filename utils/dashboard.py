import commands2
import wpilib


def put_command_on_dashboard(sub_table: str, cmd: commands2.CommandBase, name=None):
    if sub_table:
        sub_table += "/"
    else:
        sub_table = ""

    if name is None:
        name = cmd.getName()

    wpilib.SmartDashboard.putData(sub_table + name, cmd)
