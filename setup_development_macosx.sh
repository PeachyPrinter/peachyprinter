#!/bin/bash

echo "TODO - not done yet"
exit 666


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
    sudo easy_install pip
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
    sudo pip install virtualenv
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
    virtualenv venv
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
export CFLAGS=-Qunused-arguments
export CPPFLAGS=-Qunused-arguments

echo "--------Setting up numpy----"
python -c"import numpy" 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "Numpy not available adding"
    pip install -U --force numpy
    if [ $? != 0 ]; then
        echo "FAILURE: Numpy failed installing"
        WILL_FAIL=1
        FAIL_REASONS="$FAIL_REASONS\nFAILURE: Numpy failed installing"
    fi
fi

echo "--------Setting up cx_Freeze----"
python -c"import cx_Freeze" 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "cx_Freeze not available adding"
    pip install -U --force cx_Freeze
    if [ $? != 0 ]; then
        echo "FAILURE: cx_Freeze failed installing"
        WILL_FAIL=2
        FAIL_REASONS="$FAIL_REASONS\nFAILURE: cx_Freeze failed installing"
    fi
fi

echo "--------Setting up pyaudio----"
python -c"import pyaudio" 2>&1 >/dev/null
if [ $? != 0 ]; then
    echo "pyaudio not available adding"
    pip install -U --force --allow-external pyaudio --allow-unverified pyaudio pyaudio
    if [ $? != 0 ]; then
        echo "FAILURE: pyaudio failed installing"
        echo "FAILURE: Chances are you are missing the port audio binding."
        echo "FAILURE: If you have Homebrew installed 'brew install portaudio' should solve this problem"
        echo "FAILURE: Or if you prefer pain you can build from source, http://portaudio.com/docs/v19-doxydocs/tutorial_start.html"
        WILL_FAIL=2
        FAIL_REASONS="$FAIL_REASONS\nFAILURE: Pyaudio failed installing"
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
    echo "-----------------------------------"
    echo "Enviroment setup failed. Summery:"
    echo -e $FAIL_REASONS
    exit $WILL_FAIL
fi

echo "--------Applying work around to googles protobuf library----"
touch venv/lib/python2.7/site-packages/google/__init__.py
python -m compileall venv/lib/python2.7/site-packages/google/

echo ""
echo "-----------------------------------"
echo "Enviroment setup complete and seemingly successful."
echo "You can start the enviroment with the command\"source venv/bin/activate\""
