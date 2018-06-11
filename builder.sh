#!/bin/bash

RED='\033[0;31m'

echo "Initializing"


# if [[ -d venv ]]; then
#     echo "Checking venv"
# else
#     echo -e "${RED}Warning: Please create a virtual environment named \"venv\"!"
#     exit 1
# fi

echo "Checking OS"
if [[ "$OSTYPE" == "linux-gnu" || "$OSTYPE" == "darwin"* ]]; then
    echo "Installing requirements"
    source venv/bin/activate
    pip -q install --upgrade -r requirements.txt
    deactivate
    echo "Installing dev requirements"
    source dev_venv/bin/activate
    pip -q install --upgrade -r dev_requirements.txt
    deactivate
elif [[ "$OSTYPE" == "cygwin" ||  "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Installing requirements"
    venv\Scripts\activate.bat
    pip -q install --upgrade -r requirements.txt
    deactivate
    echo "Installing dev requirements"
    venv_dev\Scripts\activate.bat
    pip -q install --upgrade -r dev_requirements.txt
    deactivate
else
    echo -e "${RED}Warning: OS unsupported!"
    exit 1
fi


echo "Checking python version"
if [[ -d "venv/lib/python3.5" ]]; then
    DIR="venv/lib/python3.5/site-packages/."
else if [[ -d "venv/lib/python3.6" ]]; then
    DIR="venv/lib/python3.6/site-packages/."
else
    echo -e "${RED}Warning: Python version unsupported!"
    exit 1
fi
fi

echo "Building dist"
[[ -d dist ]] && rm -r dist
mkdir dist
cp -R $DIR dist
cp -R senpaibot dist
cp lambda_handler.py dist

echo "Building deployment package"
cd dist
zip -r -q -9 -T deployment .
mv deployment.zip ../
