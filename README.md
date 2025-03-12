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


# DLP Printer Software for Biomaterials

## Introduction
The DLP printer software was developed to facilitate the control and configuration of a DLP4710 projector for printing biomaterials. This innovative system integrates a Raspberry Pi, a PC, and the DLP projector to create a seamless workflow for creating precise 3D printed models. The software architecture is designed to optimize both server-based control and user-friendly graphical interfaces. It ensures the adaptability needed for handling biomaterials while maintaining precise execution of tasks like slicing, projecting, and motor control.

## Methods and Materials

### Hardware Components:
- **Raspberry Pi**: For server and hardware control (motors and projector).
- **PC**: For GUI application.
- **Texas Instruments DLP4710 projector**: For 3D model projection.

### Software Modules:
- **Server Module**: A Flask application running on the Raspberry Pi, enabling motor control and DLP projector operation through defined API endpoints.
- **GUI Module**: Designed for the PC, allowing users to:
  - Load STL files.
  - Configure biomaterial parameters.
  - Set slicing parameters and printing sequences.
  - Adjust projector settings.
  - Send configurations to the Raspberry Pi for execution.

## Scripts and Results

### File Architecture:
```plaintext
├── files/
│   └── img/
├── templates/
│   ├── daemons/
│   ├── GUI/
│   ├── midleware/
│   ├── models/
│   ├── resources/
│   └── static/
├── .venv/
├── app_gui.py
├── app_api.py
└── wsgi.py
```

- **Files Folder**: Stores images and other files used or created during operations.
- **Templates Folder**: Contains the primary scripts for both modules.
  - **Daemons**: Manages thread-like tasks such as slicing solids, projecting images, and motor control.
  - **GUI**: Builds the graphical interface, handling tasks like STL file loading, biomaterial setup, and slicing parameters configuration.
  - **Middleware**: Manages server-client and server-actuator interactions.
  - **Models**: Contains Flask server models for managing API data structures.
  - **Resources**: Defines API endpoints.
  - **Static**: Stores constants for the entire project.
- **Other Files**:
  - `app_gui.py` and `app_api.py`: Main scripts for the GUI and API functionalities.
  - `wsgi.py`: Handles the deployment process for the Flask application.

### Results:
- The software successfully enables:
  - Slicing and projection of 3D models.
  - Sequential layer-by-layer control for biomaterial printing.
  - Intuitive GUI-based interactions, making it accessible to both novice and experienced users.
- The modular design ensures scalability and adaptability for future improvements, such as incorporating additional biomaterial types or expanding hardware capabilities.

