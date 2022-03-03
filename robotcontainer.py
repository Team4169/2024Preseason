import wpilib
from wpilib.interfaces import GenericHID

import commands2
import commands2.button

import constants

from commands.complexauto import ComplexAuto
from commands.drivedistance import DriveDistance
from commands.defaultdrive import DefaultDrive
from commands.halvedrivespeed import HalveDriveSpeed
from commands.lucautocommand import LucAutoCommand
from commands.lucautocommandInverted import LucAutoCommand2
from commands.newPath import newPath

from subsystems.drivesubsystem import DriveSubsystem


class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:

        # The driver's controller
        self.driverController = wpilib.XboxController(constants.kDriverControllerPort)
        # self.driverController = wpilib.Joystick(constants.kDriverControllerPort)

        # The robot's subsystems
        self.drive = DriveSubsystem()

        # Autonomous routines

        # A simple auto routine that drives forward a specified distance, and then stops.
        self.simpleAuto = DriveDistance(
            constants.kAutoDriveDistanceInches, constants.kAutoDriveSpeed, self.drive
        )

        # A complex auto routine that drives forward, and then drives backward.
        self.complexAuto = ComplexAuto(self.drive)

        # A complex auto routine that drives forward, and then drives backward.
        self.lucAutoCommand = LucAutoCommand(self.drive)
        self.lucAutoCommand2 = LucAutoCommand2(self.drive)
        #simpler auto routine that drives to the second ball and places 2 into the smaller hub
        self.newPath = newPath(self.drive)

        # Chooser
        self.chooser = wpilib.SendableChooser()

        # Add commands to the autonomous command chooser
        # self.chooser.setDefaultOption("Complex Auto", self.complexAuto)
        # self.chooser.addOption("Simple Auto", self.simpleAuto)
        self.chooser.addOption("Luc Auto", self.lucAutoCommand)
        self.chooser.addOption("Luc Auto2", self.lucAutoCommand2)
        self.chooser.addOption("TestMode", self.newPath)

        # Put the chooser on the dashboard
        wpilib.SmartDashboard.putData("Autonomous", self.chooser)

        self.configureButtonBindings()

        # set up default drive command
        self.drive.setDefaultCommand(
            DefaultDrive(
                self.drive,
                lambda: -self.driverController.getRightY(),
                lambda: self.driverController.getLeftY(),
            )
        )

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

        commands2.button.JoystickButton(self.driverController, 3).whenHeld(
            HalveDriveSpeed(self.drive)
        )

    def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()