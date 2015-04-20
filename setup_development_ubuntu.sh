#!/bin/bash

echo "----Checking for already running Virtual Environment----"
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Deactivitate the existing virtual enviroment before running this script."
    echo "This can be done with the \"deactivate\" command."
    exit 53 
fi

echo "----Checking for Pip----"
command -v pip 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "Pip not available, you should be prompted for install:"
    sudo apt-get install python-pip
    if [ $? != 0 ]; then
        echo "FAILURE: Pip failed installing"
        WILL_FAIL=11
        FAIL_REASONS="$FAIL_REASONS\nFAILURE: Pip failed installing"
    fi
fi

echo "----Checking for virtualenv----"
command -v virtualenv 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "virtualenv not available, you should be prompted for install:"
    sudo apt-get install python-virtualenv
    if [ $? != 0 ]; then
        echo "FAILURE: virtualenv failed installing"
        WILL_FAIL=12
        FAIL_REASONS="$FAIL_REASONS\nFAILURE: virtualenv failed installing"
    fi
fi


echo "----Checking for and create a virtual environment----"
CREATE_VENV="TRUE"
if [ -d "venv" ]; then
    while true; do
    read -p "Do you wish remove and re-install this environment?" yn
    case $yn in
        [Yy]* ) rm -rf venv && CREATE_VENV="TRUE"; break;;
        [Nn]* ) CREATE_VENV="FALSE"; break;;
        * ) echo "Please answer yes or no.";;
    esac
    done
fi
if [ $CREATE_VENV == "TRUE" ]; then
    virtualenv -p python2.7 --system-site-packages venv
    if [ $? != 0 ]; then
        echo "Virutal environment failed"
        exit 59
    fi
fi
source venv/bin/activate
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "FAILURE: Virutal environment creation failed"
    exit 666
fi

echo "----Setting up virtual environment----"
SETUP_TMP="setup_tmp"
WILL_FAIL=0
FAIL_REASONS=""


echo "--------Setting up cython----"
python -c"import cython" 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "cython not available adding"
    pip install -U cython==0.22
    if [ $? != 0 ]; then
        echo "FAILURE: cython failed installing"
        WILL_FAIL=1
        FAIL_REASONS="$FAIL_REASONS\nFAILURE: cython failed installing"
    fi
fi

echo "--------Setting up pygame----"
python -c"import pygame" 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "pygame not available adding"
    pip install -U pygame --allow-externals peachy --allow-unverified peachy
    if [ $? != 0 ]; then
        echo "FAILURE: pygame failed installing"
        WILL_FAIL=1
        FAIL_REASONS="$FAIL_REASONS\nFAILURE: pygame failed installing"
    fi
fi

echo "--------Setting up kivy----"
python -c"import kivy" 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "kivy not available adding"
    pip install -U kivy==1.9.0
    if [ $? != 0 ]; then
        echo "FAILURE: kivy failed installing"
        WILL_FAIL=1
        FAIL_REASONS="$FAIL_REASONS\nFAILURE: kivy failed installing"
    fi
fi

echo "--------Getting Latest API----"
./get_latest_api.sh
if [ $? != 0 ]; then
    echo "FAILURE: Failed Fetching Latest API"
    WILL_FAIL=2
    FAIL_REASONS="$FAIL_REASONS\nFAILURE: Failed Fetching Latest API"
fi

if [ $WILL_FAIL != 0 ]; then
    echo "Enviroment setup failed. Summary:"
    echo -e $FAIL_REASONS
    exit $WILL_FAIL
fi

echo ""
echo "-----------------------------------"
echo "Enviroment setup complete and seemingly successful."
echo "You can start the enviroment with the command\"source venv/bin/activate\""
