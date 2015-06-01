#!/bin/bash

params=`getopt -o :hrnpcis -l install_dep,remove-venv,no_setup,pull,clean,help,setup_only --name "$0" -- "$@"`
eval set -- "$params"

DEBIAN_DEP="python-pip python-dev libsmpeg-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev"
CENTOS_DEP="python-pip python-devel python-distutils-extra python-enchant freeglut SDL_image SDL_image-devel SDL_ttf-devel SDL_mixer-devel khrplatform-devel mesa-libGLES mesa-libGLES-devel gstreamer-plugins-good gstreamer gstreamer-devel gstreamer-python mtdev-devel"

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
    virtualenv -p python2.7 venv
    if [ $? != 0 ]; then
      echo "${red}FAILED Setting up Enviroment${NC}"
      exit 59
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
  pip install -U cython==0.21.2
  if [ $? != 0 ]; then
      echo "FAILURE: cython failed installing"
      exit 666
  fi

  echo "--------Setting up kivy----"
  pip install -U kivy==1.9.0
  if [ $? != 0 ]; then
    echo "FAILURE: kivy failed installing"
    exit 666
  fi

  if [ -f api.source ]; then
    api_source=`cat api.source`
  else
    api_source=http://software.peachyprinter.com/builds/api/latest.tar.gz
  fi

  pip install --upgrade $api_source
  if [ $? != 0 ]; then
    echo -e "${FRED}FAILED TO UPDATE${RS}"
    exit 59
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
      echo "Could not find git."
      exit 1
    fi
  fi

  export GIT_REV_COUNT_RAW=`$GIT_HOME log --pretty=oneline | wc -l`
  export GIT_REV_COUNT=`trim $GIT_REV_COUNT_RAW`
  export GIT_REV=`$GIT_HOME rev-parse HEAD`

  VERSION=$SEMANTIC.$TAG$GIT_REV_COUNT
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
          echo -e "${red}FAILED Running tests${NC}"
          exit 91
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
    sudo pip install --upgrade virtualenv
    return
  fi
  yum -h > /dev/null
  if [ $? == 0 ]; then
    echo "${FGRN}YUM detected using YUM${RS}"
    echo "Assumes the EPEL repos are available"
    echo "You will be prompted to elevate permissions"

    sudo yum install $CENTOS_DEP
    sudo pip install --upgrade virtualenv
    return
  fi
  echo "${FRED}APT or YUM not found aborting${RS}"
  exit 12
}

function build ()
{
  echo "------------------------------------"
  echo "Building Deistribution"
  echo "------------------------------------"

  echo -e "${FRED}NOT COMPLETE- MORE CODES BE NEEDED${RS}"
  exit 1
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
      exit 89 
  fi
  echo -e "${FGRN}Complete${RS}"
  echo""
}

function help ()
{
  echo "Peachy Printer Build Script"
  echo "-h | --help             Displayes this message and exits"
  echo "-r | --remove-venv      Removes Virtual Environment"
  echo "-n | --no_setup         Ignores enviroment setup"
  echo "-p | --pull             Pulls from git before running setup"
  echo "-c | --clean            Performs a git reset and clean"
  echo "-i | --install_dep      Install the linux dependancies (sudo required)"
  echo "-s | --setup_only       Setups the enviroment only and does not package"
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
    -s | --setup_only )    setup_only="1" ; shift ;;
    -- )                   shift ; break ;;
    * )                    echo "Unexpected entry: $1" ; help ; exit 1 ;;
  esac
done

ensure_no_active_venv
clean_workspace
enable_venv
if [ "${no_setup}" != "1" ]; then
  setup_venv
fi
if [ "${setup_only}" != "1" ]; then
  find_version_number
  run_tests
  build
fi