#!/bin/bash
echo "Setting Flask App Environment..."
export FLASK_APP=GUI/main.py
sleep 1

echo "Setting Flask Environment to Developer Mode..."
export FLASK_ENV=development
sleep 1

echo "Running Flask..."
flask run
sleep 1

echo "Done..."