# pydeploy is a python script that runs on the terminal to help python
# wed development project get easily configured for one button deployment on 
# platforms like Heroku, Railway or render

import os
import sys
import subprocess
import argparse
from .utils import *
from .Django.django_utils import *

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


def initialize():
    args = py_deploy_parser.parse_args()

    if args.platform == "railway":
        print(f"Configuring files for {args.platform} deployment")
        requirements = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
        print("Detecting project type")
        dependency = detectProject(requirements.decode("utf-8").lower())
        version = detectPythonVersion()
        print(f"Detecting python version\n{version}")
        generateRuntime(version)
        generateRequirements(dependency)
        settings_content = generateProcfile()
        if settings_content != "":
            djangoSettings(settings_content)

    elif args.platform=="render":
        print(f"Configuring files for {args.platform} deployment") 
        requirements = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
        dependency = detectProject(requirements.decode("utf-8").lower()) 
        generateRequirements(dependency)
        generate_build_file() 
        os.system('chmod a+x build.sh') 

    elif args.platform == "heroku":
        print(f"Configuring files for {args.platform} deployment")
        requirements = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
        print("Detecting project type")
        dependency = detectProject(requirements.decode("utf-8").lower())
        version = detectPythonVersion()
        print(f"Detecting python version\n{version}")
        generateRuntime(version)
        generateRequirements(dependency)
        settings_content = generateProcfile(args.platform)
        if settings_content != "":
            djangoSettings(settings_content)

    else:
        print(ERROR(f"{PROG} currently does not support this platform "))

    logger.displayLogs()

