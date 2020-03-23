import versioneer
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

PACKAGE_NAME = "openscm-units"
AUTHORS = [
    ("Zeb Nicholls", "zebedee.nicholls@climate-energy-college.org"),
    ("Sven Willner", "sven.willner@pik-potsdam.de"),
    ("Jared Lewis", "jared.lewis@climate-energy-college.org"),
    ("Robert Gieseke", "robert.gieseke@pik-potsdam.de"),
]
URL = "https://github.com/openscm-project/openscm-units"

DESCRIPTION = "Thin wrapper to run simple climate models (emissions driven runs only)"
README = "README.rst"

SOURCE_DIR = "src"

PACKAGES = find_packages(SOURCE_DIR)  # no exclude as only searching in `src`
PACKAGE_DIR = {"": SOURCE_DIR}
PACKAGE_DATA = {"openscm_units": ["data/*.csv"]}

REQUIREMENTS = ["pandas", "pint"]
REQUIREMENTS_NOTEBOOKS = ["notebook", "seaborn"]
REQUIREMENTS_TESTS = ["codecov", "coverage", "nbval", "pytest-cov", "pytest>=4.0"]
REQUIREMENTS_DOCS = ["sphinx>=1.4", "sphinx_rtd_theme"]
REQUIREMENTS_DEPLOY = ["twine>=1.11.0", "setuptools>=38.6.0", "wheel>=0.31.0"]

REQUIREMENTS_DEV = [
    *[
        "bandit",
        "black",
        "black-nb",
        "flake8",
        "isort",
        "mypy",
        "nbdime",
        "numpy",
        "pydocstyle",
        "pylint>=2.4.4",
    ],
    *REQUIREMENTS_DEPLOY,
    *REQUIREMENTS_DOCS,
    *REQUIREMENTS_NOTEBOOKS,
    *REQUIREMENTS_TESTS,
]

REQUIREMENTS_EXTRAS = {
    "deploy": REQUIREMENTS_DEPLOY,
    "dev": REQUIREMENTS_DEV,
    "docs": REQUIREMENTS_DOCS,
    "notebooks": REQUIREMENTS_NOTEBOOKS,
    "tests": REQUIREMENTS_TESTS,
}

# Get the long description from the README file
with open(README, "r") as f:
    README_LINES = ["OpenSCM-Units", "==============", ""]
    add_line = False
    for line in f:
        if line.strip() == ".. sec-begin-long-description":
            add_line = True
        elif line.strip() == ".. sec-end-long-description":
            break
        elif add_line:
            README_LINES.append(line.strip())

if len(README_LINES) < 3:
    raise RuntimeError("Insufficient description given")


class OpenscmUnits(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        pytest.main(self.test_args)


cmdclass = versioneer.get_cmdclass()
cmdclass.update({"test": OpenscmUnits})

setup(
    name=PACKAGE_NAME,
    version=versioneer.get_version(),
    description=DESCRIPTION,
    long_description="\n".join(README_LINES),
    long_description_content_type="text/x-rst",
    author=", ".join([author[0] for author in AUTHORS]),
    author_email=", ".join([author[1] for author in AUTHORS]),
    url=URL,
    license="3-Clause BSD License",
    classifiers=[  # full list at https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["openscm", "units", "python", "repo", "simple", "climate", "model"],
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    extras_require=REQUIREMENTS_EXTRAS,
    cmdclass=cmdclass,
)
