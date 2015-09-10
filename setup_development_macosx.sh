#!/bin/bash
echo "----------Activating kivy venv------------"
if [ -z "${KIVY_APP_PATH}" ]; 
    then export KIVY_APP_PATH=/Applications/Kivy.app
fi

KIVY_APP_PATH_RESOURCES="${KIVY_APP_PATH}/Contents/Resources";
echo "Kivy App Path: ${KIVY_APP_PATH}"
echo "Kivy Resource Path: ${KIVY_APP_PATH_RESOURCES}"


echo "----------Creating symlinks to kivy venv------------"
ln -s ${KIVY_APP_PATH_RESOURCES}/venv venv

# activate the virtualenv
source venv/bin/activate

# setup the environment to not mess with the system
export PYTHONPATH="${KIVY_APP_PATH_RESOURCES}/kivy:${PYTHONPATH}"
# export DYLD_FALLBACK_LIBRARY_PATH="${KIVY_APP_PATH_RESOURCES}/lib"
export LD_PRELOAD_PATH="${KIVY_APP_PATH_RESOURCES}/lib"
export GST_REGISTRY="${KIVY_APP_PATH_RESOURCES}/gst.registry"
export GST_PLUGIN_SCANNER="${KIVY_APP_PATH_RESOURCES}/gst-plugin-scanner"
export GTK_PATH="${KIVY_APP_PATH_RESOURCES}/../Frameworks/GStreamer.framework/Versions/Current"
export GST_PLUGIN_SYSTEM_PATH="${KIVY_APP_PATH_RESOURCES}/../Frameworks/GStreamer.framework/Versions/Current/lib/gstreamer-1.0"
export GIO_EXTRA_MODULES="${KIVY_APP_PATH_RESOURCES}/../Frameworks/GStreamer.framework/Versions/Current/lib/gio/modules"
export KIVY_HOME="${KIVY_APP_PATH_RESOURCES}/.kivy"

echo "--------Setting up pyinstaller----"
pip install -U pyinstaller

echo "--------Applying work around to googles protobuf library----"
pip install protobuf==2.6.1
touch venv/lib/python2.7/site-packages/google/__init__.py
python -m compileall venv/lib/python2.7/site-packages/google/

echo "--------Getting Latest API----"
./get_latest_api.sh

echo ""
echo "-----------------------------------"
echo "Enviroment setup complete and seemingly successful."

