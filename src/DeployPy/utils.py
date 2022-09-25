#this file contains utitlities that help deployment across all platforms
import os
import sys

def SUCCESS(value):
    return f"\033[1;32m{value}\033[00m"

def WARNING(value):
    return f"\033[1;33m{value}\033[00m"

def ERROR(value):
    return f"\033[1;91m{value}\033[00m"

class Logger():
    issues = {}
    def __init__(self) -> None:
        pass
    def addIssue(self, header, issue):
        self.issues[header] = issue
    def displayLogs(self):
        if self.issues != {}:
            print("Issues Logged During Project Configuration")
            for key, value in self.issues:
                print(f"{key}: {value}")

logger = Logger()


def detectProject(dependencies):
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

def generateRequirements(dependencies):
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

def detectPythonVersion():
    version = sys.version.split(" ")[0]
    return version            

def generateRuntime(version):
    with open("./runtime.txt", 'w') as runtime:
        runtime.writelines("Python " + version)


def generateProcfile(platform="railway"):
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
        print(ERROR(f"Could failed to generate Procfile"))
        sys.exit()        

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