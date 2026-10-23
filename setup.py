# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="afa-dach",
    version="1.0.0",
    description="DACH AfA-Rechner & Abschreibungs-Optimierer 2026: Lineare & degressive AfA nach Wachstumschancengesetz, optimales Wechseljahr, § 7g Sonder-AfA & GWG-Grenzen (DE, AT, CH).",
    author="DACH Digitalwerk",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "dach-afa=afa_dach.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Intended Audience :: Financial and Insurance Industry",
    ],
)
