#!/bin/bash
echo "----------Creating symlinks to kivy venv------------"
ln -s /Applications/Kivy.app/Contents/Resources/venv venv
echo "----------Activating kivy venv------------"
source /Applications/Kivy.app/Contents/Resources/venv/bin/activate

echo "--------Setting up pyinstaller----"
pip install -U pyinstaller

echo "--------Getting Latest API----"
./get_latest_api.sh

echo "--------Applying work around to googles protobuf library----"
touch venv/lib/python2.7/site-packages/google/__init__.py
python -m compileall venv/lib/python2.7/site-packages/google/

echo ""
echo "-----------------------------------"
echo "Enviroment setup complete and seemingly successful."
echo "You can start the enviroment with the command\"source venv/bin/activate\""
