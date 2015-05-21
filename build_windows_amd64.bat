@ECHO OFF

ECHO ------------------------------------
ECHO Cleaning workspace
ECHO ------------------------------------

DEL /Q *.exe
DEL /q 
RMDIR /S /Q build
RMDIR /S /Q dist
DEL /S *.pyc

ECHO ------------------------------------
ECHO Setting up Enviroment
ECHO ------------------------------------

CALL c:\kivy_amd64\kivy-2.7.bat
CALL setup_development_windows_amd64.bat
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
copy version.properties VERSION.py

ECHO ------------------------------------
ECHO Creating Package
ECHO ------------------------------------

COPY /Y PeachyPrinter-win64.spec.source PeachyPrinter.spec
IF NOT "%ERRORLEVEL%" == "0" (
  ECHO FAILED executing command: COPY /Y PeachyPrinter-win64.spec.source PeachyPrinter.spec
  EXIT /B 78
)

pyinstaller --clean --noconfirm PeachyPrinter.spec
IF NOT "%ERRORLEVEL%" == "0" (
  ECHO FAILED executing command: pyinstaller --clean --noconfirm PeachyPrinter.spec
  EXIT /B 78
)

ECHO ------------------------------------
ECHO Moving file
ECHO ------------------------------------

COPY dist\PeachyPrinter*.exe .
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO "FAILED moving files"
    EXIT /B 798
)