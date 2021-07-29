import os 
import subprocess

# move to location of library files
os.chdir(os.getcwd() + "\src\lib")

# get library files and call ./mpy_cross.exe on them
for file in os.listdir():
    if file[-3:] != "mpy" and file[-2:] == "py":
        subprocess.run(["./../../mpy_cross.exe",f"./{file}"])

print(os.listdir())
