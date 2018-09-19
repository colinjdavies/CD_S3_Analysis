import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "html.parser", "configparser", "boto3.s3.inject"],
                     "excludes": ["tkinter"], "include_msvcr": True}

setup(  name = "S3_Analysis",
        version = "0.1",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base="Console")])
