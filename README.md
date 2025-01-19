# Printer_DLP
## Intro
Adapted from notes from [Mark Wexler](http://wexler.free.fr)

The units we've seen came with outdated firmware. In order to use 180 and 1440 Hz modes, the firmware on the projector needs to be updated. This has to be done on a Windows PC using TI's graphic control tool.

- Connect the projector's USB port to your PC using the supplied cable
- Download and install the graphic control tool
- Download the latest version of the firmware
- Install the firmware using the Firmware/Update Firmware tab of the graphic control tool

To check the version of firmware that you've installed, click the "Get" button in the lower-right corner of the first tab (Information) of graphic control tool.

## Running

If change_mode is true, then you must:
- install the dlpmode.exe program and any required DLLs
- set the dlpmode_exe global variable (below) to the absolute or relative
  path of dlpmode.exe

> Run the *App_test.py* file with the required libraries and the device conected with usb and hdmi ports.

