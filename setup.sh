#/bin/bash

# Install Python
apt update
apt install python3 python3-pip -y

# Install App Dependencies
pip3 install --upgrade -r requirements.txt

# Launch App
python3 app/app.py
