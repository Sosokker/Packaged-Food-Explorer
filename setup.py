import subprocess
import sys

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.read().splitlines()

for requirement in requirements:
    install(requirement)