# Kivy Peachy Printer
Kivy Peachy Printer is a kivy frontend to replace the existing tk front end.

API [https://github.com/PeachyPrinter/peachyprintertools]
API python packages are available at [http://software.peachyprinter.com/builds/api/]

This code [https://github.com/PeachyPrinter/kivypeachyprinter]
Complete packages are available at [http://software.peachyprinter.com/]

## Development Requirements
<!-- ### Ubuntu (Debian)
via apt
 - python-pip
 - python-virtualenv

You can prepare your enviroment using the following command:
```sh
sudo apt-get install python-pip python-virtualenv
``` -->

### Centos (RedHat)
<!-- via yum
 - python-pip
 - python-virtualenv

 You can prepare your enviroment using the following command:
```sh
sudo rpm -iUvh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
sudo yum -y update
sudo yum -y install python-pip
sudo yum -y install python-virtualenv
``` -->

### Mac OSX
<!--  - pip
 - virtualenv -->

### Windows
via (oh yeah there is no package manager in windows)
 - kivy [http://kivy.org/#download]

##Getting Started
###Creating a development environment
This development process assumes the use of python virtual environments we have made a couple of handy helper scripts to setup these enviroments.
 - Start by running the setup development enviroment script for your OS. This will setup a virtual enviroment and load the required dependancies into it.

###Building the software package

###Running the software
Once the virtual environment is started running the software an be done via the command *python src/peachyprintertools.py*
 - "-c"  - will out put the log info to the console
 - "-d"  - will add the development mode features
 - "-l LEVEL" - will select the log level valid levels: DEBUG INFO WARNING ERROR  note:DEBUG is so verbose printing will probibily get ruined by delays

###Known issues

###Scripts
 - build*  - These create an installable package
 - setup_devleopment*  - These create a python virtual environment and install required dependancies (Note some may need to be installed on the system)
 - get_latest_api  - This will update a currently active virtual envirionment with the lastest version of the api code 

