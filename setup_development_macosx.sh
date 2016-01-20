#!/bin/bash

echo "--------Install Kivy--------------"
pip install -I Cython==0.23
USE_OSX_FRAMEWORKS=0 pip install -U kivy==1.9.1
echo "--------Setting up pyinstaller----"
pip install -U pyinstaller==3.1

echo "--------Applying work around to googles protobuf library----"
pip install protobuf==2.6.1
touch venv/lib/python2.7/site-packages/google/__init__.py
python -m compileall venv/lib/python2.7/site-packages/google/

echo "--------Getting Latest API----"
if [ -f api.source ]; then
    echo"***************USING OVERRIDDEN API SOURCE*********************"
    api_source=`cat api.source`
else
    api_source=http://software.peachyprinter.com/builds/api/latest.tar.gz
fi

pip install --upgrade $api_source

echo ""
echo "-----------------------------------"
echo "Enviroment setup complete and seemingly successful."

