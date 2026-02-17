# setup.py
from setuptools import setup

setup(
    name="sales-dashboard",
    version="1.0",
    install_requires=[
        "streamlit==1.28.0",
        "pandas==2.0.3",
        "numpy==1.24.3",
        "plotly==5.17.0",
    ],
)
