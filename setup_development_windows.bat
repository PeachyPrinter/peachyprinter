@ECHO OFF
SET will_fail=0
SET fail_reasons=""

ECHO ----Checking for already running kivy Environment----
ECHO "%kivy_portable_root%"
IF "%kivy_portable_root%" == "" (
    ECHO Run this from kivy portable environment v 1.8.0.
    EXIT /B 53 
)

ECHO ----Adding PyInstaller----
python -c"import PyInstaller" 2> nul > nul
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO --------PyInstaller not available adding----
    pip install PyInstaller==2.1
    IF NOT "%ERRORLEVEL%" == "0" (
        ECHO --------PyInstaller Failed to install----
        EXIT /B 53 
    )
)

ECHO --------Setting up numpy----
python -c"import numpy" 2> nul > nul
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO Numpy not available adding
    pip install -U --force http://www.lfd.uci.edu/~gohlke/pythonlibs/z94jfosk/numpy-1.9.2+mkl-cp27-none-win32.whl
    python -c"import numpy" 2> nul > nul
    IF NOT "%ERRORLEVEL%" == "0" (
        ECHO FAILURE: Numpy failed installing, you can manually install it from http://sourceforge.net/projects/numpy/
        SET will_fail=1
        fail_reasons="%fail_reasons%\nFAILURE: Numpy failed installing, you can manually install it from http://sourceforge.net/projects/numpy/"
    )
)

ECHO --------Getting Latest API----
call "get_latest_api.bat"
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO FAILURE: Getting lastest api failed Check log for details
    SET will_fail=%lastest_result%
    SET fail_reasons="%fail_reasons%\nFAILURE: Getting lastest api failed Check log for details"
)

echo --------Applying work around to googles protobuf library for packaging----
echo "" >> %kivy_portable_root%\Python27\Lib\site-packages/google/__init__.py
python -m compileall %kivy_portable_root%\Python27\Lib\site-packages/google/

IF NOT "%will_fail%" == "0" (
    ECHO Enviroment Setup failed
    ECHO -e %fail_reasons%
    EXIT /B %will_fail%
)

ECHO -----------------------------------
ECHO Enviroment Setup complete and seemingly successful.
ECHO You can start the enviroment with the command\"source venv/bin/activate\"
