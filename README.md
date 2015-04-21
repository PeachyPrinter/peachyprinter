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
<!-- ### Ubuntu (Debian)
sudo apt-get install python-pip git python-dev libsdl1.2-dev python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev
sudo mkdir /opt/git
sudo chown peachy.peachy /opt/git/
sudo chmod 777 /opt/git
cd /opt/git
git clone https://github.com/PeachyPrinter/kivypeachyprinter.git
git clone https://github.com/PeachyPrinter/peachyprintertools.git
cd kivypeachyprinter
./setup_development_ubuntu.sh
./get_latest_api.sh
echo "for api dev this links to api checkout"
rm -rf venv/lib/python2.7/site-packages/peachyprinter
ln -s /opt/git/peachyprintertools/src/peachyprinter venv/lib/python2.7/site-packages/peachyprinter
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
To setup up your enviroment it helps to have a package manager such as "Homebrew" [http://brew.sh/]
####Pre-Script Requirements
 - python2.7
 - xcode
 - pip
 - virtualenv
 - mercurial  ('brew install mercurial')   -- Needed for pygame
 - sdl   ('brew install sdl sdl_image sdl_mixer sdl_ttf portmidi') -- Needed for pygame
 - Xquartz  a X11 interface for mac [http://xquartz.macosforge.org/landing/] -- Needed for pygame


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

