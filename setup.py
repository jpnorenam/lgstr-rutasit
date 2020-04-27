import os
from setuptools import setup, find_packages

def read(fname):
    dname = os.path.dirname(__file__)
    fname = os.path.join(dname, fname)

    try:
        import m2r
        return m2r.parse_from_file(fname)
    except ImportError:
        with open(fname) as f:
            return f.read()

setup(
    name = "lgstr-rutasit",
    version = "0.1.0",
    author = "Juan Pablo Norena",
    author_email = "jpnorenam@unal.edu.co",
    description = "Several tools for routing origin/destiny data using public transport systems in metropolitan areas",
    license = "GPL-3.0",
    keywords = "routing public transport metropolitan medellin",
    url = "https://sites.google.com/unal.edu.co/lab-gstr/proyectos/ptrvscovid",
    packages = find_packages(),
    long_description = read('README.md'),
    classifiers = [
        "Development Status :: Beta",
        "Topic :: Scientific/Engineering",
        "License :: OSI NOT Approved Yet :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3"
    ],
    install_requires = [
        "json5",
        "numpy",
        "pandas",
        "pyproj",
        "shapely"
    ],
    setup_requires = [
        'm2r',
        'wheel'
    ]
)

