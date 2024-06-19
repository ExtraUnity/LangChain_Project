#!/bin/bash
#This file is made by Nikolaj
echo "Setting Flask App Environment..."
set FLASK_APP=GUI/main.py
$env:FLASK_APP = "GUI/main.py"
sleep 1

echo "Setting Flask Environment to Developer Mode..."
set FLASK_ENV=development
sleep 1

echo "Running Flask..."
flask run --reload -h 0.0.0.0
sleep 1

echo "Done..."