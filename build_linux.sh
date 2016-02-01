#!/bin/bash

params=`getopt -o :hrnpcisj -l build_runner,install_dep,remove-venv,no_setup,pull,clean,help,setup_only --name "$0" -- "$@"`
eval set -- "$params"

DEBIAN_DEP="python-pip python-dev libsmpeg-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev git"
REDHAT_DEP="gcc python-pip python-devel python-distutils-extra python-enchant python-distutils-extra python-enchant freeglut PyOpenGL SDL_ttf-devel SDL_mixer-devel pygame pygame-devel khrplatform-devel mesa-libGLES mesa-libGLES-devel gstreamer-plugins-good gstreamer gstreamer-python mtdev-devel git"

RS="\033[0m"    # reset
FRED="\033[31m" # foreground red
FGRN="\033[32m" # foreground green

function remove_venv ()
{
  echo "------------------------------------"
  echo "Removing Virtual Environment"
  echo "------------------------------------"
  rm -rf venv
  echo -e "${FGRN}Complete${RS}"
  echo""
}

function clean ()
{
  read -p "Are you sure? " -n 1 -r
  echo ""
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    git reset --hard HEAD
    git clean -e api.source
  fi
}

function clean_workspace ()
{
  echo "------------------------------------"
  echo "Cleaning workspace"
  echo "------------------------------------"

  rm -rf src/build
  rm -rf *.deb
  rm -f src/VERSION.py
  rm -f version.properties 
  echo -e "${FGRN}Complete${RS}"
  echo""
}

function enable_venv ()
{
  echo "------------------------------------"
  echo "Upgrading / Starting Virtual Environment"
  echo "------------------------------------"
  if [ ! -f venv/bin/activate ]; then
    virtualenv --system-site-packages -p python2.7 venv
    if [ $? != 0 ]; then
      echo "${FRED}FAILED Setting up virtual enviroment${RS}"
      EXIT_CODE=59
      failed_exit
    fi
  fi
  source venv/bin/activate
  echo -e "${FGRN}Complete${RS}"
  echo""
}

function setup_venv ()
{
  echo "------------------------------------"
  echo "Setting up virtual env"
  echo "------------------------------------"
  echo "--------Setting up cython----"
  pip install -I -U cython==0.23
  if [ $? != 0 ]; then
      echo "${FRED}FAILURE: cython failed installing${RS}"
      EXIT_CODE=666
      failed_exit
  fi

  echo "--------Setting up kivy----"
  pip install -I -U git+https://github.com/kivy/kivy.git@master
  if [ $? != 0 ]; then
    echo "${FRED}FAILURE: kivy failed installing${RS}"
    EXIT_CODE=666
    failed_exit
  fi
  
  yum -h > /dev/null
  if [ $? == 0 ]; then
    sudo pip install -I pygments
  fi

  if [ -f api.source ]; then
    api_source=`cat api.source`
  else
    api_source=https://github.com/PeachyPrinter/peachyprintertools/releases/download/1.0.0.905/PeachyPrinterToolsAPI-1.0.0.905.tar.gz
  fi

  pip install -I --upgrade $api_source
  if [ $? != 0 ]; then
    echo -e "${FRED}FAILED TO UPDATE${RS}"
    EXIT_CODE=59
    failed_exit
  fi

  echo -e "${FGRN}Complete${RS}"
  echo""
}

function find_version_number ()
{
  echo "------------------------------------"
  echo "Extracting Git Revision Number"
  echo "------------------------------------"

  SEMANTIC=`cat symantic.version`

  function trim() { echo $1; }

  if [ -z $GIT_HOME ]; then
    if [ -f "/usr/local/bin/git" ]; then
      export GIT_HOME=/usr/local/bin/git
    elif [ -f "/usr/bin/git" ]; then
      export GIT_HOME=/usr/bin/git
    elif [ -f "/bin/git" ]; then
      export GIT_HOME=/bin/git
    else
      ${FRED}GIT Could not be located${RS}
      EXIT_CODE=55
      failed_exit
    fi
  fi

  git status
  if [ $? == 0 ]; then
    export GIT_REV_COUNT_RAW=`$GIT_HOME log --pretty=oneline | wc -l`
    export GIT_REV_COUNT=`trim $GIT_REV_COUNT_RAW`
    export GIT_REV=`$GIT_HOME rev-parse HEAD`
    VERSION=$SEMANTIC.$TAG$GIT_REV_COUNT
  else
    export GIT_REV_COUNT='release'
    export GIT_REV='release'
    VERSION=$SEMANTIC.r
  fi
  echo "Version: $VERSION"
  echo "# THIS IS A GENERATED FILE " > version.properties
  echo "version='$VERSION'" >> version.properties
  echo "revision='$GIT_REV'" >> version.properties
  echo "Git Revision Number is $GIT_REV_COUNT"
  cp version.properties src/VERSION.py
  echo ""
}

function run_tests ()
{
  echo "------------------------------------"
  echo "Running Tests"
  echo "------------------------------------"

  python test/test-all.py
  if [ $? != 0 ]; then
          echo -e "${FRED}FAILED Running tests${RS}"
          EXIT_CODE=91
          failed_exit
  fi
  echo -e "${FGRN}Complete${RS}"
  echo""
}

function dependancies ()
{
  apt-get -h > /dev/null
  if [ $? == 0 ]; then
    echo "${FGRN}APT detected using APT${RS}"
    echo "You will be prompted to elevate permissions"
    sudo apt-get install $DEBIAN_DEP
    sudo pip install -I --upgrade virtualenv
    return
  fi
  yum -h > /dev/null
  if [ $? == 0 ]; then
    echo "${FGRN}YUM detected using YUM${RS}"
    echo "Assumes the EPEL repos are available"
    echo "You will be prompted to elevate permissions"
    sudo yum install $REDHAT_DEP
    sudo pip install -I --upgrade virtualenv
    return
  fi
  echo "${FRED}APT or YUM not found aborting${RS}"
  EXIT_CODE=12
  failed_exit
}

function build ()
{
  echo "------------------------------------"
  echo "Building Deistribution"
  echo "------------------------------------"

  echo -e "${FRED}NOT COMPLETE- MORE CODES BE NEEDED${RS}"
  EXIT_CODE=1
  failed_exit
}

function update ()
{
  echo "------------------------------------"
  echo "Getting latest "
  echo "------------------------------------"

  git pull
  if [ $? != 0 ]; then
    echo -e "${FRED}Pull failed${RS}"
    exit 134
  fi
}

function ensure_no_active_venv ()
{
  echo "------------------------------------"
  echo "Checking for already running Virtual Environment"
  echo "------------------------------------"

  if [[ "$VIRTUAL_ENV" != "" ]]; then
      echo "Deactivitate the existing virtual enviroment before running this script."
      echo "This can be done with the \"deactivate\" command."
      EXIT_CODE=89 
      failed_exit
  fi
  echo -e "${FGRN}Complete${RS}"
  echo""
}

function build_runner () {
  echo "------------------------------------"
  echo "Creating Rules and Runner Script"
  echo "------------------------------------"

  if [ ! -f /etc/udev/rules.d/99-peachy.rules ]; then
    echo "You will be prompted to elevate permissions"
    echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="16d0", ATTR{idProduct}=="0af3", MODE="0666"' > 99-peachy.rules
    sudo cp 99-peachy.rules /etc/udev/rules.d/99-peachy.rules
    echo "Added rules you may be required to login again"
  fi
  echo "source venv/bin/activate" > run.sh
  echo "python src/main.py -tl INFO" >> run.sh
  chmod +x run.sh

  echo -e "${FGRN}Complete${RS}"
}

function help ()
{
  echo "Peachy Printer Build Script"
  echo "Recommened Usage: build_linux.sh -ijk"
  echo "-h | --help             Displayes this message and exits"
  echo "-r | --remove-venv      Removes Virtual Environment"
  echo "-n | --no_setup         Ignores enviroment setup"
  echo "-p | --pull             Pulls from git before running setup"
  echo "-c | --clean            Performs a git reset and clean"
  echo "-i | --install_dep      Install the linux dependancies (sudo required)"
  echo "-s | --setup_only       Setups the enviroment only and does not package"
  echo "-j | --build_runner     Creates the rules and files required to run peachy printer(sudo required)"
}

function failed_exit()
{
  popd
  exit $EXIT_CODE
}

while true
do
  case "$1" in
    -h | --help )          help ; exit 0 ;;
    -r | --remove-venv )   remove_venv ; shift ;;
    -n | --no_setup )      no_setup="1" ; shift ;;
    -p | --pull )          update ; shift ;;
    -c | --clean )         clean ; shift ;;
    -i | --install_dep )   dependancies ; shift ;;
    -j | --build_runner )  build_runner ; shift ;;
    -s | --setup_only )    setup_only="1" ; shift ;;
    -k | --kivy_source )   build_kivy="1" ; shift ;;
    -- )                   shift ; break ;;
    * )                    echo "Unexpected entry: $1" ; help ; exit 1 ;;
  esac
done

pushd .
cd "$(dirname "$0")"
ensure_no_active_venv
clean_workspace
enable_venv
if [ "${no_setup}" != "1" ]; then
  ./run_tests
  setup_venv
fi
if [ "${build_kivy}" == "1" ]; then
  build_kivy_source
fi
if [ "${setup_only}" != "1" ]; then
  find_version_number
  run_tests
  build
fi
popd
