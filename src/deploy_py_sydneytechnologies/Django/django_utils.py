# this folder contains all the functions that are directly needed
# for DeployPy to prepare a django file for deployment on any of the supported 
# platforms, which include heroku, railway and render

from ..utils import *
# optional settings DeployPy needs to check and evaluate to ensure proper deployment
DJANGO_SETTING_ESSENTIALS = [
    "ALLOWED_HOSTS",
    "CSRF_TRUSTED_ORIGINS",
    "STATIC_ROOT",
    "CORS_ORIGIN_ALLOW_ALL",
    "DEBUG",
]

def djangoSettings(settings_content):
    # here we want to test if the following configurations already exist within
    # the settings.py file
    for configs in DJANGO_SETTING_ESSENTIALS:
        if configs not in "".join(settings_content):
            print(f"{configs} not found in settings.py")
            rectifySettings(config=configs)
        else:
            print(SUCCESS(f"{configs} found in settings.py"))

def rectifySettings(config):
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
            logger.addIssue(config, "not configured")
            print(f"configure {config} in your settings.py file")
    elif config == DJANGO_SETTING_ESSENTIALS[1]:
        # this refers to csrf_trusted_origins 
        logger.addIssue(config, "not configured")
        print(f"configure {config} in your settings.py file")
    elif config == DJANGO_SETTING_ESSENTIALS[2]:
        # this config refers to the static root files
        logger.addIssue(config, "not configured")
        print(f"configure {config} in your settings.py file")
    elif config == DJANGO_SETTING_ESSENTIALS[3]:
        # this config refers to the CORS configuration root files
        user_input = input(WARNING(f"would you like to setup the default configuration for django {config} y/n?"))
        if user_input.lower() == "y":
            with open(settings, 'a') as file:
                file.write(f"\n{config}=True")
        else:
            logger.addIssue(config, "not configured")
            print(f"configure {config} in your settings.py file")
    elif config == DJANGO_SETTING_ESSENTIALS[4]:
          # this config refers to the DEBUG setting
        user_input = input(WARNING(f"would you like to setup the default configuration for django {config} y/n?"))
        if user_input.lower() == "y":
            with open(settings, 'a') as file:
                file.write(f"\n{config}=True")
        else:
            logger.addIssue(config, "not configured")
            print(f"configure {config} in your settings.py file")