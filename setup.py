"""Setup vn_norm libarary."""

import os
import sys
from distutils.version import LooseVersion

import pip
from setuptools import find_packages, setup

if LooseVersion(sys.version) < LooseVersion("3.6"):
    raise RuntimeError(
        "Tensorflow TTS requires python >= 3.6, "
        "but your Python version is {}".format(sys.version)
    )

if LooseVersion(pip.__version__) < LooseVersion("19"):
    raise RuntimeError(
        "pip>=19.0.0 is required, but your pip version is {}. "
        'Try again after "pip install -U pip"'.format(pip.__version__)
    )

# TODO(@dathudeptrai) update requirement if needed.
requirements = {
    "install": [
        "num2words>=0.5.10",
        "regex>=2021.3.17",
        "roman>=3.3",
        "numpy>=1.18.5",
        "unidecode @ git+https://github.com/anytool/unidecode_ext.git",
        "g2p_en",
        "espnet_tts_frontend"
    ],
    "setup": ["numpy", "pytest-runner", ],
    "test": [
        "pytest>=3.3.0",
        "hacking>=1.1.0",
    ],
}

# TODO(@dathudeptrai) update console_scripts.
entry_points = {
    "console_scripts": [

    ]
}

install_requires = requirements["install"]
setup_requires = requirements["setup"]
tests_require = requirements["test"]
extras_require = {
    k: v for k, v in requirements.items() if k not in ["install", "setup"]
}

dirname = os.path.dirname(__file__)
setup(
    name="vn_norm",
    version="0.0",
    url="https://github.com/anytool/vn_norm",
    author="anytool",
    author_email="nguyentritoanst@gmail.com",
    description="Vietnamese normalize",
    long_description=open(os.path.join(
        dirname, "README.md"), encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    packages=find_packages(include=["vn_norm*"]),
    package_data={'vn_norm': ['text/mapping/*.txt']},
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    entry_points=entry_points,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
