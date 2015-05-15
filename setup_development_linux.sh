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
    echo "Pip not available"
fi

echo "----Checking for existing and (re)create a virtual environment----"
rm -rf venv

virtualenv -p python2.7 venv
if [ $? != 0 ]; then
    echo "Virutal environment failed. Is virtualenv available?"
    exit 59
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

echo ""
echo "-----------------------------------"
echo "Enviroment setup complete and seemingly successful."
echo "You can start the enviroment with the command\"source venv/bin/activate\""
