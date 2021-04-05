#!/bin/bash
python myproject_repo/manage.py makemigrations
python myproject_repo/manage.py migrate

# hand over control to cmd
exec "$@"