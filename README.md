# Peachy Printer
Peachy Printer is a kivy frontend to replace the existing tk front end.

API [https://github.com/PeachyPrinter/peachyprintertools]

This code [https://github.com/PeachyPrinter/peachyprinter]

## Installing
#### Windows / Mac
Visit peachyprinter.com and click the get started link for installation binaries

#### Linux
The Linux version needs to be run from source and the comptuer must meet the following:

- amd64 platform
- darwin like linux (all testing done with ubuntu) _Other operating systems may work as well if dependancies can be met but are not yet supported_

There is a handy script to help you get started. Once you have the code:
1. download the source from the download zip link on this page
2. unzip the file
3. open a terminal window and go to the directory you just unziped.
4. type  **./build_linux.sh -i -j** and hit enter to run 
 - The -i flag will install the requirements via apt.
 - The -j flag adds a line to allow access to the usb port. and creates a run.sh script.
5. Once that process is complete type **./run.sh**  and hit enter to start the software.

## Known issues
 - Occasionally crashes on close in windows 10
 - Configuration can have problems if printers are swapped while software is running
 - Virtual machines will not work as the usb driver abstractions cannot keep up
 - Font on some ubuntu machines is odd.

## Development
### Development goals
 - Continuous deployment
 - TDD when possible(UI elements not included)
 - Il8n
 - Simple contained development enviroment
 - Cross platform (Inital goals: Windows, Mac, Centos, )

### Linux steps (Rough example)
run build_linux.sh -h for details

### Windows Development Setup
#### Requirements
    http://aka.ms/vcpython27
    python 64 or 32  (scripts assume location of python c:\Python27_32 or c:\Python27_64)
    install pip
    install virtualenv


###Creating a development environment
This development process assumes the use of python virtual environments we have made a couple of handy helper scripts to setup these enviroments.
 - Start by running the setup development enviroment script for your OS. This will setup a virtual enviroment and load the required dependancies into it.

### Running the software
Once the virtual environment is started running the software an be done via the command *python src/peachyprintertools.py*
 - "-c"  - will out put the log info to the console
 - "-d"  - will add the development mode features
 - "-l LEVEL" - will select the log level valid levels: DEBUG INFO WARNING ERROR  note:DEBUG is so verbose printing will probibily get ruined by delays

### Scripts
 - build*  - These create an installable package
 - setup_devleopment*  - These create a python virtual environment and install required dependancies (Note some may need to be installed on the system)
 - get_latest_api  - This will update a currently active virtual envirionment with the lastest version of the api code

## Contibutors
Nicolas Rubio - Posisition icon - source: https://www.iconfinder.com/icons/311123/coordinates_gps_locate_location_map_position_icon

## Release Notes
January 25th  2016 :: 1.0.x Initial public release of peachy printer ui for peachy printer tools.
