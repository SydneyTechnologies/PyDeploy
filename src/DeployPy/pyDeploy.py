# pydeploy is a python script that runs on the terminal to help python
# wed development project get easily configured for one button deployment on 
# platforms like Heroku, Railway or render

import os
import sys
import subprocess
from src.DeployPy.render import generate_build_file
from src.DeployPy.utils import*



if args.platform == "railway":
    print(f"Configuring files for {args.platform} deployment")
    requirements = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    print("Detecting project type")
    dependency = detect_project(requirements.decode("utf-8").lower())
    version = detect_python_version()
    print(f"Detecting python version\n{version}")
    generate_runtime(version)
    generate_requirements(dependency)
    settings_content = generate_procfile()
    if settings_content != "":
        settings_setup(settings_content)

elif args.platform=="render":
    print(f"Configuring files for {args.platform} deployment") 
    requirements = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    dependency = detect_project(requirements.decode("utf-8").lower()) 
    generate_requirements(dependency)
    generate_build_file() 
    os.system('chmod a+x build.sh') 

elif args.platform == "heroku":
    print(f"Configuring files for {args.platform} deployment")
    requirements = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    print("Detecting project type")
    dependency = detect_project(requirements.decode("utf-8").lower())
    version = detect_python_version()
    print(f"Detecting python version\n{version}")
    generate_runtime(version)
    generate_requirements(dependency)
    settings_content = generate_procfile(args.platform)
    if settings_content != "":
        settings_setup(settings_content)

    

else:
    print(ERROR(f"{PROG} currently does not support this platform "))

