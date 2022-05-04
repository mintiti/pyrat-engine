from typing import List

import setuptools
import shlex
from codecs import open
from setuptools import setup
from setuptools.command.develop import develop
from subprocess import check_call

__version__ = "0.1.0"


def read_requirements(file: str) -> List[str]:
    """Returns content of given requirements file."""
    return [
        line
        for line in open(file)
        if not (line.startswith("#") or line.startswith("--"))
    ]


class PostDevelopCommand(develop):
    def run(self) -> None:
        try:
            check_call(shlex.split("pre-commit install"))
            check_call(shlex.split("pre-commit install --hook-type commit-msg"))
        except Exception as e:
            print("Unable to run 'pre-commit install'", e)
        develop.run(self)


setup(
    name="PyRat-Engine",
    version=__version__,
    description="Reinforcement Learning library",
    author="Truong Minh Tri, Thiebaut Kevin",
    url="https://github.com/mintiti/pyrat-engine",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=read_requirements("./requirements/requirements.txt"),
    extras_require={
        "dev": read_requirements("./requirements/requirements-dev.txt"),
    },
    cmdclass={"develop": PostDevelopCommand},
    include_package_data=True,
)
