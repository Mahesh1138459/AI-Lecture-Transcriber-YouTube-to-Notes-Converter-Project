
from setuptools import find_packages, setup

HYPEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> list[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name="AI Project",
    version="0.0.1",
    author="Mahesh",
    author_email="mahesh1138459@gmail.com",
    install_requires=get_requirements("requirements.txt"),  # Provide the correct path to your requirements file
    packages=find_packages()
)
