#!/bin/bash

params=`getopt -o :hc? -l clean,help --name "$0" -- "$@"`
eval set -- "$params"

RS="\033[0m"    # reset
FRED="\033[31m" # foreground red
FGRN="\033[32m" # foreground green


function help ()
{
  echo "Peachy Printer Build Script"
  echo "-h | --help             Displayes this message and exits"
  echo "-c | --clean            Removes Virtual Environment"
  echo "-i | --ignore           Ignores enviroment setup"
}

function clean ()
{
  echo "------------------------------------"
  echo "Removing Virtual Environment"
  echo "------------------------------------"
  rm -rf venv
}

while true
do
  case "$1" in
    -h | --help )    help ; exit 0 ;;
    -c | --clean )   clean ; shift ;;
    -i | --ignore )  ignore="1" ; shift ;;
    -- )             shift ; break ;;
    * )              echo "Unexpected entry: $1" ; help ; exit 1 ;;
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

echo "------------------------------------"
echo "Cleaning workspace"
echo "------------------------------------"

rm -rf src/build
rm -rf *.deb
rm -f src/VERSION.py
rm -f version.properties 
echo -e "${FGRN}Complete${RS}"
echo""

if [ "${ignore}" != "1" ]; then
  echo "------------------------------------"
  echo "Upgrading / Starting Virtual Environment"
  echo "------------------------------------"
  source setup_development_linux.sh
  if [ $? != 0 ]; then
    echo -e "${red}FAILED Setting up Enviroment${NC}"
    exit 90
  fi
else
  echo "------------------------------------"
  echo "Starting Virtual Environment"
  echo "------------------------------------"
  if [ -f venv/bin/activate ]; then
    source venv/bin/activate
  else
    echo -e "${FRED}Missing virtual enviroment try running with --clean${RS}"
    exit 91
  fi
fi
echo -e "${FGRN}Complete${RS}"
echo""

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

echo "------------------------------------"
echo "Building Deistribution"
echo "------------------------------------"

echo -e "${FRED}NOT COMPLETE- MORE CODES BE NEEDED${RS}"
exit 1