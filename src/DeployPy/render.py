#this file contains all functions that automate render deployment

def generate_build_file():
    """
    genatates a build file
    """
    build_config=["#!/usr/bin/env bash\n", 
                  "# exit on error\n",
                   "set -o errexit \n", 
                   "pip install -r requirements.txt \n",
                   "python manage.py collectstatic --no-input\n",
                   "python manage.py migrate \n",]
    with open("./build.sh", 'w') as build:
        build.writelines(build_config)  


def generate_renderyaml_file():
    pass           