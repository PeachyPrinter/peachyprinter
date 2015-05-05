# Kivy Peachy Printer
Kivy Peachy Printer is a kivy frontend to replace the existing tk front end.

API [https://github.com/PeachyPrinter/peachyprintertools]
API python packages are available at [http://software.peachyprinter.com/builds/api/]

This code [https://github.com/PeachyPrinter/kivypeachyprinter]
Complete packages are available at [http://software.peachyprinter.com/]

## Development goals
 - Continuous deployment
 - TDD when possible(UI elements not included)
 - Il8n
 - Simple contained development enviroment
 - Cross platform (Inital goals: Windows, Mac, Centos, )


## Development Requirements
### Ubuntu (Debian)

### Steps (Rough example)
 - sudo apt-get install python-pip git python-dev libsdl1.2-dev python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev mercurial
 - sudo pip install --upgrade virtualenv
 - sudo usermod -a -G dialout username
 - sudo mkdir /opt/git
 - sudo chown username.username /opt/git/
 - sudo chmod 777 /opt/git
 - cd /opt/git
 - git clone https://github.com/PeachyPrinter/kivypeachyprinter.git
 - git clone https://github.com/PeachyPrinter/peachyprintertools.git
 - cd kivypeachyprinter
 - ./setup_development_linux.sh
 - echo "for api dev this links to api checkout"
 - rm -rf venv/lib/python2.7/site-packages/peachyprinter
 - rm -rf venv/local/lib/python2.7/site-packages/peachyprinter
 - ln -s /opt/git/peachyprintertools/src/peachyprinter venv/lib/python2.7/site-packages/peachyprinter


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
####Pre-Script Requirements
 - Kivy from source see http://kivy.org/docs/installation/installation-macosx.html

### Windows Setup
 - kivy [http://kivy.org/#download] or [http://kivy.org/downloads/1.9.0/Kivy-1.9.0-py2.7-win32-x86.exe]
 - Assumed extraction point as c:\kivy_x86 or kivy_amd64
 - Fix the kivy to point at master (I know, i know)
 -- open the kivy_x86 directory in a  terminal windows
 -- move kivy27 kivy27_old
 -- git clone https://github.com/kivy/kivy.git kivy27
 -- close the windows
 -- open a terminal window as an administrator
 -- cd \kivy
 -- kivy-2.7.bat
 -- cd kivy27
 -- make force

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

