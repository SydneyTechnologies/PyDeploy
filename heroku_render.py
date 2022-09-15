
from utils import*
import sys
import os


def generate_runtime(version):
    with open("./runtime.txt", 'w') as runtime:
        runtime.writelines("Python " + version)


def generate_procfile():
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
                procfile_config = f"web: gunicorn '{temp}'"
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