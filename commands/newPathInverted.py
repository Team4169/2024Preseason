import commands2

import constants

from .drivedistance import DriveDistance
from .movecommand import MoveCommand
from subsystems.drivesubsystem import DriveSubsystem
from .reset_gyro import ResetGyro
from SnowVeyerCommands.PickUp import pickUp
from SnowVeyerCommands.DropOff import dropOff

#parallel to the angled line and and inch from the intersection across from the hub
class newPathInverted(commands2.SequentialCommandGroup):
    """
    A complex auto command that drives forward, releases a hatch, and then drives backward.
    """

    def __init__(self, drive: DriveSubsystem):
        super().__init__(
            # Drive forward the specified distance
            ResetGyro(drive),
            MoveCommand(-3.75, 0, drive),
            pickUp(2, 0.3),
            MoveCommand(0, -180, drive),
            MoveCommand(-7, -180, drive),
            MoveCommand(0, -220, drive),
            MoveCommand(-1, -220, drive),
            dropOff(2, 0.3),
            MoveCommand(1, -220, drive),
            
            )