echo "----Checking to ensure running Virtual Environment----"
red='\033[0;31m'
NC='\033[0m'
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo 'You need to be running the virtual environment first type "source venv/bin/activate"'
    exit 98
fi
pip install --upgrade http://software.peachyprinter.com/builds/api/latest.tar.gz
if [ $? != 0 ]; then
        echo -e "${red}FAILED TO UPDATE${NC}"
        exit 59
    fi