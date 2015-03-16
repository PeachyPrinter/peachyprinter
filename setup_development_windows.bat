@ECHO OFF
SET will_fail=0
SET fail_reasons=""

ECHO ----Checking for already running Virtual Environment----
IF NOT "%VIRTUAL_ENV%" == "" (
    ECHO Deactivitate the existing virtual enviroment before running this script.
    ECHO This can be done with the \"deactivate\" command.
    EXIT /B 53 
)

ECHO ----Checking for Pip----
where pip 2> nul > nul
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO FAILURE: PIP is not available, you should install it.
    SET will_fail=11
    SET fail_reasons="%fail_reasons%\nFAILURE: Pip failed installing"
    EXIT /B %will_fail%
)

ECHO ----Checking for virtualenv----
where virtualenv 2> nul > nul
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO FAILURE: virtualenv not available, you should install it.
    SET will_fail=12
    SET fail_reasons="%fail_reasons%\nFAILURE: virtualenv not available, you should install it."
    EXIT /B %will_fail%
)

ECHO ----Checking for and create a virtual environment----
SET create_venv="TRUE"
IF NOT EXIST "venv" GOTO endquestion
:question
SET /P anwser="Do you wish remove and re-install this environment? (y/n)"
IF /i {%anwser%}=={y} (GOTO :yes) 
IF /i {%anwser%}=={n} (GOTO :no) 
GOTO :question 

:yes 
SET create_venv="TRUE"
GOTO :endquestion

:no 
SET create_venv="FALSE"
GOTO :endquestion

:endquestion


IF %create_venv% == "TRUE" (
    ECHO --------Createing new virtualenv----
    ECHO --------Note for windows to ease use system packages are included ----
    ECHO --------To avoid this and build from a clean environment use --no-site-packages -----
    virtualenv --system-site-packages  venv 
    IF NOT "%ERRORLEVEL%" == "0" (
        ECHO FAILURE: Virutal environment creation failed
        SET will_fail=59
        SET fail_reasons="%fail_reasons%\nFAILURE: Virutal environment creation failed"
        EXIT /B %will_fail%
    )
)

ECHO --------Activating virtualenv----
CALL "venv\Scripts\activate.bat"
IF "%VIRTUAL_ENV%" == "" (
        ECHO FAILURE: Virutal environment activation failed
        SET will_fail=666
        SET fail_reasons="%fail_reasons%\nFAILURE: Virutal environment activation failed"
        EXIT /B %will_fail%
)

ECHO ----Setting up virtual environment----
ECHO --------Setting up numpy----
python -c"import numpy" 2> nul > nul
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO Numpy not available adding
    pip install -U --force numpy
    IF NOT "%ERRORLEVEL%" == "0" (
        ECHO FAILURE: Numpy failed installing, you can manually install it from http://sourceforge.net/projects/numpy/
        SET will_fail=1
        fail_reasons="%fail_reasons%\nFAILURE: Numpy failed installing, you can manually install it from http://sourceforge.net/projects/numpy/"
    )
)

ECHO --------Setting up cx_Freeze----
python -c"import cx_Freeze" 2> nul > nul
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO cx-freeze Required installing
    pip install -U cx_Freeze
    IF NOT "%ERRORLEVEL%" == "0" (
        ECHO FAILURE: cx-freeze failed installing, You can manually install it from: https://pypi.python.org/pypi?:action=display&name=cx_Freeze&version=4.3.4 
        SET will_fail=2
        SET fail_reasons="%fail_reasons%\nFAILURE: cx-freeze failed installing, You can manually install it from: https://pypi.python.org/pypi?:action=display&name=cx_Freeze&version=4.3.4"
    )
)

ECHO --------Setting up pyaudio----
python -c"import pyaudio" 2> nul > nul
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO PyAudio Required, you can manually install it from: http://people.csail.mit.edu/hubert/pyaudio/#downloads
    SET will_fail=4
    SET fail_reasons="%fail_reasons%\nFAILURE :PyAudio Required, you can manually install it from: http://people.csail.mit.edu/hubert/pyaudio/#downloads"
)

ECHO --------Getting Latest API----
call "get_latest_api.bat"
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO FAILURE: Getting lastest api failed Check log for details
    SET will_fail=%lastest_result%
    SET fail_reasons="%fail_reasons%\nFAILURE: Getting lastest api failed Check log for details"
)

echo --------Applying work around to googles protobuf library----
echo "" >> venv/lib/site-packages/google/__init__.py
python -m compileall venv/lib/site-packages/google/

IF NOT %will_fail% == 0 (
    ECHO Enviroment Setup failed
    ECHO -e %fail_reasons%
    EXIT /B %will_fail%
)

ECHO -----------------------------------
ECHO Enviroment Setup complete and seemingly successful.
ECHO You can start the enviroment with the command\"source venv/bin/activate\"
