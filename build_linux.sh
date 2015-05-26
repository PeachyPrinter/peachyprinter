#!/bin/bash

params=`getopt -o :hrnpc -l remove-venv,no_setup,pull,clean,help --name "$0" -- "$@"`
eval set -- "$params"

RS="\033[0m"    # reset
FRED="\033[31m" # foreground red
FGRN="\033[32m" # foreground green


function help ()
{
  echo "Peachy Printer Build Script"
  echo "-h | --help             Displayes this message and exits"
  echo "-r | --remove-venv      Removes Virtual Environment"
  echo "-i | --ignore           Ignores enviroment setup"
  echo "-p | --pull             Pulls from git before running setup"
  echo "-c | --clean            Performs a git reset and clean"
}

function remove_venv ()
{
  echo "------------------------------------"
  echo "Removing Virtual Environment"
  echo "------------------------------------"
  rm -rf venv
}

function clean ()
{
  git reset --hard HEAD
  git clean -e api.source
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

while true
do
  case "$1" in
    -h | --help )          help ; exit 0 ;;
    -r | --remove-venv )   remove_venv ; shift ;;
    -n | --no_setup )      no_setup="1" ; shift ;;
    -p | --pull )          update ; shift ;;
    -c | --clean )         clean ; shift ;;
    -- )                   shift ; break ;;
    * )                    echo "Unexpected entry: $1" ; help ; exit 1 ;;
  esac
done


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

clean_workspace
enable_venv
if [ "${no_setup}" != "1" ]; then
  $$$$$$$$
find_version_number
run_tests

echo "----Checking for Pip----"
command -v pip 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "Pip not available"
fi

source venv/bin/activate
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "FAILURE: Virutal environment creation failed"
    exit 666
fi

echo "----Setting up virtual environment----"
SETUP_TMP="setup_tmp"

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

echo "--------Getting Latest API----"
./get_latest_api.sh
if [ $? != 0 ]; then
    echo "FAILURE: Failed Fetching Latest API"
    exit 667
fi



echo "------------------------------------"
echo "Building Deistribution"
echo "------------------------------------"

echo -e "${FRED}NOT COMPLETE- MORE CODES BE NEEDED${RS}"
exit 1