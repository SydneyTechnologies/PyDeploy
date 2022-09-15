#this file contains utitlities that help deployment across all platforms
import os
import sys
import argparse

def SUCCESS(value):
    return f"\033[1;32m{value}\033[00m"
def ERROR(value):
    return f"\033[1;91m{value}\033[00m"








DESCRIPTION = "This project is centred around formatting and editing web applications made in Django, FastApi or flask into the correct deployable format for popular hosting platforms such as Heroku, Railway, Render etc…"
EPILOG = "Simple automation project made by SydneyIdundun"
PROG = "PyDeploy"
DJANGO_SETTING_ESSENTIALS = [
    "ALLOWED_HOSTS",
    "CSRF_TRUSTED_ORIGINS",
    "STATIC_ROOT",
    "CORS_ORIGIN_ALLOW_ALL",
    "DEBUG",
]

py_deploy_parser = argparse.ArgumentParser(
    prog = PROG,
    description=DESCRIPTION,
    epilog=EPILOG,
)

# the platform that will be supported first will be railway
supported_platforms = ["heroku", "railway", "render"]
PLATFORM_DESCRIPTION = f"The platform argument helps {PROG} to configure for the right platform, it is a required argument"
py_deploy_parser.add_argument('platform', help=PLATFORM_DESCRIPTION, type=str.lower, choices=supported_platforms)

args = py_deploy_parser.parse_args()


def settings_setup(settings_content):
    # here we want to test if the following configurations already exist within
    # the settings.py file
    for configs in DJANGO_SETTING_ESSENTIALS:
        if configs not in "".join(settings_content):
            print(f"{configs} not found in settings.py")
        else:
            print(SUCCESS(f"{configs} found in settings.py"))



def detect_project(dependencies):
    if dependencies.__contains__("django"):
        print(SUCCESS("Django project detected"))
    elif dependencies.__contains__("fastApi"):
        print(SUCCESS("FastApi project detected"))
    elif dependencies.__contains__("flask"):
        print(SUCCESS("Flask project detected"))
    else: 
        print(ERROR("UNKNOWN project type"))
        sys.exit()
    dependencies = dependencies.replace('\r', '')
    return dependencies    

def generate_requirements(dependencies):
    with open("./requirements.txt", 'w') as requirements:
        requirements.writelines(dependencies)
        

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)



def detect_python_version():
    version = sys.version.split(" ")[0]
    return version            