# pydeploy is a python script that runs on the terminal to help python
# wed development project get easily configured for one button deployment on 
# platforms like Heroku, Railway or render

import os
import sys
import argparse
import subprocess


def SUCCESS(value):
    return f"\033[1;32m{value}\033[00m"
def ERROR(value):
    return f"\033[1;91m{value}\033[00m"

DESCRIPTION = "This project is centred around formatting and editing web applications made in Django, FastApi or flask into the correct deployable format for popular hosting platforms such as Heroku, Railway, Render etc…"
EPILOG = "Simple automation project made by SydneyIdundun"
PROG = "PyDeploy"

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
    return dependencies
def detect_python_version():
    version = sys.version.split(" ")[0]
    return version
def generate_runtime(version):
    with open("./runtime.txt", 'w') as runtime:
        runtime.writelines("Python " + version)

def generate_requirements(dependencies):
    with open("./requirements.txt", 'w') as requirements:
        requirements.writelines(dependencies)

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def generate_procfile():
    print("Generating Procfile")
    settings_file = find("settings.py","./")
    config = ""
    with open(settings_file, 'r') as settings:
        lines = settings.readlines()
        for line in lines:
            if "WSGI_APPLICATION" in line:
                temp = str(line).split("=")[1].replace("'","").replace(".application", "").replace(" ", "").replace("\n", "")
                procfile_config = f"web: gunicorn '{temp}'"
                config = procfile_config
    if config != "":
        with open("./Procfile", "w") as Procfile:
            Procfile.writelines(procfile_config+"\n")
            print(SUCCESS("Your project is ready to be deployed!!!"))
    else:
        print(ERROR(f"{PROG} could failed to generate Procfile"))
        sys.exit()


if args.platform == "railway":
    print(f"Configuring files for {args.platform} deployment")
    requirements = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    print("Detecting project type")
    dependency = detect_project(requirements.decode("utf-8").lower())
    version = detect_python_version()
    print(f"Detecting python version\n{version}")
    generate_runtime(version)
    generate_requirements(dependency)
    generate_procfile()
else:
    print(ERROR(f"{PROG} currently does not support this platform "))

