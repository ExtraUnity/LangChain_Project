#!/bin/bash
echo "Setting Flask App Environment..."
export FLASK_APP=GUI/main.py
sleep 2

echo "Setting Flask Environment to Developer Mode..."
export FLASK_ENV=development
sleep 2

echo "Running Flask..."
flask run
sleep 2

echo "Done..."