#!/bin/bash
cd "$(dirname "$0")"
python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org Flask==3.0.0 Flask-CORS==4.0.0 && python3 app.py
