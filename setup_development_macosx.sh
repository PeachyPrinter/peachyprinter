#!/bin/bash
echo "----------Creating symlinks to kivy venv------------"
ln -s /Applications/Kivy.app/Contents/Resources/venv venv

echo "----------Activating kivy venv------------"
KIVY_APP_PATH="/Applications/Kivy.app/Contents/Resources";

# activate the virtualenv
source ${KIVY_APP_PATH}/venv/bin/activate

# setup the environment to not mess with the system
export PYTHONPATH="${KIVY_APP_PATH}/kivy:${PYTHONPATH}"
# export DYLD_FALLBACK_LIBRARY_PATH="${KIVY_APP_PATH}/lib"
export LD_PRELOAD_PATH="${KIVY_APP_PATH}/lib"
export GST_REGISTRY="${KIVY_APP_PATH}/gst.registry"
export GST_PLUGIN_SCANNER="${KIVY_APP_PATH}/gst-plugin-scanner"
export GTK_PATH="${KIVY_APP_PATH}/../Frameworks/GStreamer.framework/Versions/Current"
export GST_PLUGIN_SYSTEM_PATH="${KIVY_APP_PATH}/../Frameworks/GStreamer.framework/Versions/Current/lib/gstreamer-1.0"
export GIO_EXTRA_MODULES="${KIVY_APP_PATH}/../Frameworks/GStreamer.framework/Versions/Current/lib/gio/modules"
export KIVY_HOME="${KIVY_APP_PATH}/.kivy"

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

