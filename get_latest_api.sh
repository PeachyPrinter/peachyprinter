echo "----Checking to ensure running Virtual Environment----"
red='\033[0;31m'
NC='\033[0m'

if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo 'You need to be running the virtual environment first type "source venv/bin/activate"'
    exit 98
fi

if [ -f api.source ]; then
    echo"***************USING OVERRIDDEN API SOURCE*********************"
    api_source=`cat api.source`
else
    api_source=https://github.com/PeachyPrinter/peachyprintertools/releases/download/1.0.0/PeachyPrinterToolsAPI-1.0.0.893.tar.gz
fi

# This accounts for the fact that fedora 22 comes with pytz version 2012d 
# which fails the protobuf dependancy check for >=2010 despite being correct.
pip install --upgrade pytz==2015.4

pip install --upgrade $api_source
if [ $? != 0 ]; then
        echo -e "${red}FAILED TO UPDATE${NC}"
        exit 59
    fi