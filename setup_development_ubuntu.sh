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


echo "----Checking for existing and (re)create a virtual environment----"
if [ -d "venv" ]; then
    rm -rf venv
fi

virtualenv -p python2.7 --system-site-packages venv
if [ $? != 0 ]; then
    echo "Virutal environment failed"
    exit 59
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
pip install -U cython==0.21.2
if [ $? != 0 ]; then
    echo "FAILURE: cython failed installing"
    WILL_FAIL=1
    FAIL_REASONS="$FAIL_REASONS\nFAILURE: cython failed installing"
fi

echo "--------Setting up pygame----"
pip install hg+http://bitbucket.org/pygame/pygame
if [ $? != 0 ]; then
    echo "FAILURE: pygame failed installing"
    WILL_FAIL=1
    FAIL_REASONS="$FAIL_REASONS\nFAILURE: pygame failed installing"
fi

echo "--------Setting up kivy----"
pip install -U kivy==1.9.0
if [ $? != 0 ]; then
    echo "FAILURE: kivy failed installing"
    WILL_FAIL=1
    FAIL_REASONS="$FAIL_REASONS\nFAILURE: kivy failed installing"
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
