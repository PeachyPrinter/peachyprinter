@ECHO OFF

ECHO ----Ensuring Virtual Environment Running----
IF  "%VIRTUAL_ENV%" == "" (
    ECHO You need to be running the virtual environment first type \"source venv/bin/activate\"
    ECHO This can be done with the \"deactivate\" command.
    EXIT /B 88
)

ECHO ----Running Installer----
pip install --upgrade http://software.peachyprinter.com/builds/api/latest.zip
IF NOT "%ERRORLEVEL%" == "0" (
    ECHO FAILURE: Installer failed, check log
    EXIT /B 99
)

ECHO ----API Successfully updated/installed.
EXIT /B 0