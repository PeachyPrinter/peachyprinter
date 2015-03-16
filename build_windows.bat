@ECHO OFF

ECHO ------------------------------------
ECHO Cleaning workspace
ECHO ------------------------------------

DEL /Q *.msi
RMDIR /S /Q src\build
RMDIR /S /Q src\dist
RMDIR /S /Q venv
DEL /S *.pyc

ECHO ------------------------------------
ECHO Setting up Virtual Enviroment venv
ECHO ------------------------------------

IF "%PYTHON_HOME%" == "" (
    ECHO FAILURE: Environment setup failed, PYTHON_HOME environment variable not available
    EXIT /B 27
)

set TCL_LIBRARY=%PYTHON_HOME%\tcl\tcl8.5
set TK_LIBRARY=%PYTHON_HOME%\tcl

CALL setup_development_windows.bat
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO FAILURE: Environment setup failed, check log
    EXIT /B 23
)

ECHO ------------------------------------
ECHO Extracting Git Revision Number
ECHO ------------------------------------

SET SEMANTIC=0.0.1
SET /p SEMANTIC=<symantic.version
IF NOT DEFINED GIT_HOME (
  git --version
  IF "%ERRORLEVEL%" == "0" (
    SET GIT_HOME=git
  ) ELSE (
    ECHO "Could not find git."
    PAUSE
    EXIT /B 1
  )
)

FOR /f "delims=" %%A in ('%GIT_HOME% rev-list HEAD --count') do SET "GIT_REV_COUNT=%%A"
FOR /f "delims=" %%A in ('%GIT_HOME% rev-parse HEAD') do SET "GIT_REV=%%A"

SET VERSION=%SEMANTIC%.%GIT_REV_COUNT%
ECHO Version: %VERSION%
ECHO # THIS IS A GENERATED FILE  > version.properties
ECHO version='%VERSION%' >> version.properties
ECHO revision='%GIT_REV%' >> version.properties
ECHO Git Revision Number is %GIT_REV_COUNT%
copy version.properties src\VERSION.py

ECHO ------------------------------------
ECHO Creating Package
ECHO ------------------------------------

CD src
python setup.py bdist_msi
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO "FAILED PACKAGING ABORTING"
    EXIT /B 3
)
CD ..

ECHO ------------------------------------
ECHO Moving file
ECHO ------------------------------------

MOVE src\dist\*.msi .