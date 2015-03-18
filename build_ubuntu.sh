#!/bin/bash

red='\033[0;31m'
NC='\033[0m'

echo "------------------------------------"
echo "Checking for already running Virtual Environment"
echo "------------------------------------"

if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Deactivitate the existing virtual enviroment before running this script."
    echo "This can be done with the \"deactivate\" command."
    exit 89 
fi

echo "------------------------------------"
echo "Cleaning workspace"
echo "------------------------------------"

# TODO JT 2014-02-13 - Should clean the workspace
rm -rf src/build
rm -rf *.deb
rm -f src/VERSION.py
rm -f version.properties 
rm -rf venv

echo "------------------------------------"
echo "Create Virtual Environment"
echo "------------------------------------"

source setup_development_ubuntu.sh
if [ $? != 0 ]; then
        echo -e "${red}FAILED Setting up Enviroment${NC}"
        exit 90
fi

echo "------------------------------------"
echo "Load Virtual Environment"
echo "------------------------------------"

source venv/bin/activate

echo "------------------------------------"
echo "Install Latest API"
echo "------------------------------------"

source get_latest_api.sh
if [ $? != 0 ]; then
        echo -e "${red}FAILED Installing LatestAPI${NC}"
        exit 91
fi

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

echo "------------------------------------"
echo "Running Tests"
echo "------------------------------------"

python test/test-all.py
if [ $? != 0 ]; then
        echo -e "${red}FAILED Running tests${NC}"
        exit 91
fi

echo "NOT COMPLETE- MORE CODES BE NEEDED"
exit 1