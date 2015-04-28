@ECHO OFF

ECHO ----Checking for already running kivy Environment----
ECHO "%kivy_portable_root%"
IF "%kivy_portable_root%" == "" (
    ECHO Run this from kivy portable environment v 1.8.0.
    EXIT /B 53 
)
ECHO ----Running Installer----
pip install --upgrade ..\peachyprintertools\PeachyPrinterToolsAPI-0.4.726.zip
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO FAILURE: Installer failed, check log
    EXIT /B 99
)

ECHO ----API Successfully updated/installed.
EXIT /B 0