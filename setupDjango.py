# Script to setup django environment without running the shell
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marindec1.settings")
django.setup()
