#!/bin/bash
deactivate
cd /directory
pwd
source venv/bin/activate

echo "activated"
cd ilmis_accounts
pwd
python3 manage.py deactivate_users