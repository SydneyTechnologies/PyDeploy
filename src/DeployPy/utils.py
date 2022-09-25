#this file contains utitlities that help deployment across all platforms
import os
import sys
import argparse

def SUCCESS(value):
    return f"\033[1;32m{value}\033[00m"

def WARNING(value):
    return f"\033[1;33m{value}\033[00m"

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
            RectifySettings(config=configs)
        else:
            print(SUCCESS(f"{configs} found in settings.py"))

def RectifySettings(config):
    # this function will either fix or warn the user about a missing configuration
    # required in the settings.py file for a Django project
    TARGET = "settings.py"
    settings = getFile(TARGET)
    if config == DJANGO_SETTING_ESSENTIALS[0]:
        # this refers to the allowed hosts
        user_input = input(WARNING(f"would you like to setup the default configuration for django {config} y/n?"))
        if user_input.lower() == "y":
            with open(settings, 'a') as file:
                file.write(f"\n{config}=[*]")
        else:
            print(f"configure {config} in your settings.py file")

    
    elif config == DJANGO_SETTING_ESSENTIALS[1]:
        # this refers to csrf_trusted_origins 
        print(f"configure {config} in your settings.py file")
    elif config == DJANGO_SETTING_ESSENTIALS[2]:
        # this config refers to the static root files
        print(f"configure {config} in your settings.py file")
    elif config == DJANGO_SETTING_ESSENTIALS[3]:
        # this config refers to the CORS configuration root files
        user_input = input(WARNING(f"would you like to setup the default configuration for django {config} y/n?"))
        if user_input.lower() == "y":
            with open(settings, 'a') as file:
                file.write(f"\n{config}=True")
        else:
            print(f"configure {config} in your settings.py file")
    elif config == DJANGO_SETTING_ESSENTIALS[4]:
          # this config refers to the DEBUG setting
        user_input = input(WARNING(f"would you like to setup the default configuration for django {config} y/n?"))
        if user_input.lower() == "y":
            with open(settings, 'a') as file:
                file.write(f"\n{config}=True")
        else:
            print(f"configure {config} in your settings.py file")


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

def getFile(file_name):
    current_dir = os.getcwd()
    file_location = find(file_name, current_dir)
    if file_location :
        return file_location

def detect_python_version():
    version = sys.version.split(" ")[0]
    return version            

def generate_runtime(version):
    with open("./runtime.txt", 'w') as runtime:
        runtime.writelines("Python " + version)


def generate_procfile(platform="railway"):
    print("Generating Procfile")
    settings_file = find("settings.py","./")
    config = ""
    settings_content = ""
    with open(settings_file, 'r') as settings:
        lines = settings.readlines()
        settings_content = lines
        for line in lines:
            if "WSGI_APPLICATION" in line:
                temp = str(line).split("=")[1].replace("'","").replace(".application", "").replace(" ", "").replace("\n", "")
                if platform == "railway":
                    procfile_config = f"web: gunicorn '{temp}'"
                    config = procfile_config
                elif platform == "heroku":
                    procfile_config = f"web: gunicorn {temp} --log-file -"
                    config = procfile_config
                break
    if config != "":
        with open("./Procfile", "w") as Procfile:
            Procfile.writelines(procfile_config+"\n")
            print(SUCCESS("Your project is ready to be deployed!!!"))
            return settings_content
    else:
        print(ERROR(f"{PROG} could failed to generate Procfile"))
        sys.exit()        