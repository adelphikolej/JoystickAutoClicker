JOYSTICK AUTOCLICKER — WINDOWS STARTER APP
==========================================

BUILD A WINDOWS EXE
-------------------
1. Install Python 3.10 or newer from https://www.python.org/downloads/
   During setup, enable "Add Python to PATH".
2. Extract this ZIP into a normal folder.
3. Double-click BUILD_EXE.bat.
4. Wait for the build to finish.
5. The executable should be created at:
      dist\JoystickAutoClicker.exe

The build script needs internet access to install Python packages.

WHAT IT DOES
------------
- Select A, B, X, Y, START, SELECT/BACK, LB, RB, and D-pad directions.
- Choose an interval from 100 ms to 5 seconds.
- Start or stop repeated presses.
- Run continuously or stop after 10 or 100 presses.
- Sends inputs through a virtual Xbox 360 controller.

IMPORTANT LIMITATION
--------------------
This starter app creates a VIRTUAL Xbox 360 controller. It does not remotely press
buttons on a physical controller. Games that support XInput/virtual Xbox controllers
may receive the virtual button presses. Some games or anti-cheat systems may block
virtual controllers. Use only where permitted by the game's rules.

VIRTUAL CONTROLLER DRIVER
-------------------------
The virtual controller driver must be installed separately on the target Windows PC.
The original ViGEmBus project is archived, so check compatibility and use only a
trusted, compatible release. The driver is not bundled in the EXE.

TROUBLESHOOTING
---------------
- If the EXE build fails, check Python is installed and internet is available.
- If virtual controller creation fails, check whether the driver is installed and
  compatible, then restart Windows if the installer asks.
- The STOP button ends the loop and releases the selected virtual button.
- Start with a slow interval while testing.

This project has not been tested against your specific controller/game. Review code
before running it. PyInstaller output is built for the OS on which it is run.
