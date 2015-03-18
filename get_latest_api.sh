echo "----Checking to ensure running Virtual Environment----"
red='\033[0;31m'
NC='\033[0m'

if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo 'You need to be running the virtual environment first type "source venv/bin/activate"'
    exit 98
fi

if [ -f api.source ]; then
    api_source=`cat api.source`
else
    api_source=http://software.peachyprinter.com/builds/api/latest.tar.gz

fi

pip install --upgrade $api_source
if [ $? != 0 ]; then
        echo -e "${red}FAILED TO UPDATE${NC}"
        exit 59
    fi