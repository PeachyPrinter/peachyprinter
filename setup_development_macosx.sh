#!/bin/bash

echo "--------Build Media---------------"
python build_media.py
if [ $? != 0 ]; then
    echo -e "${FRED}MEDIA BUILD FAILED{RS}"
    exit 59
fi

echo "--------Install Kivy--------------"
pip install -I Cython==0.23
USE_OSX_FRAMEWORKS=0 pip install -U kivy==1.9.1
echo "--------Setting up pyinstaller----"
pip install -U pyinstaller==3.1

echo "--------Applying work around to googles protobuf library----"
pip install protobuf==2.6.1
touch venv/lib/python2.7/site-packages/google/__init__.py
python -m compileall venv/lib/python2.7/site-packages/google/


pip install --upgrade -r requirements.txt
if [ $? != 0 ]; then
    echo -e "${FRED}FAILED TO INSTALL REQUIREMENTS{RS}"
    exit 59
fi

echo ""
echo "-----------------------------------"
echo "Enviroment setup complete and seemingly successful."

