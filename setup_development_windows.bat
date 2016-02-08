@ECHO OFF
SET will_fail=0
SET fail_reasons=""

:ACTIVATE_VENV
call venv/Scripts/activate.bat
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO FAILURE: Installer failed, check log
    EXIT /B 99
)

:SETUP_DEP
ECHO ----Adding Kivy And Dependancies----
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools==19.2
python -m pip install --upgrade wheel==0.26.0
python -m pip install --upgrade docutils==0.12
python -m pip install --upgrade pygments==2.1
python -m pip install --upgrade pypiwin32==219 
python -m pip install --upgrade kivy.deps.sdl2==0.1.12
python -m pip install --upgrade kivy.deps.glew==0.1.4
python -m pip install --upgrade kivy==1.9.1


ECHO ----Adding PyInstaller----
python -m pip install --upgrade pyinstaller==3.1
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO FAILURE: Installer failed, check log
    EXIT /B 99
)

ECHO ----Fetching API for Peachy Printer Tools----
python -m pip install --upgrade https://github.com/PeachyPrinter/peachyprintertools/releases/download/1.0.0.916/PeachyPrinterToolsAPI-1.0.0.916.zip
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO FAILURE: Installer failed, check log
    EXIT /B 99
)

echo --------Applying work around to googles protobuf library for packaging----
echo "" >> %VIRTUAL_ENV%\Lib\site-packages/google/__init__.py
python -m compileall %VIRTUAL_ENV%\Lib\site-packages/google/

IF NOT "%will_fail%" == "0" (
    ECHO Enviroment Setup failed
    ECHO -e %fail_reasons%
    EXIT /B %will_fail%
)


ECHO ----Reverting Setup Tools to known good version----
python -m pip install --upgrade setuptools==19.2

ECHO -----------------------------------
ECHO Enviroment Setup complete and seemingly successful.
