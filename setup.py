from distutils.core import setup
import py2exe

setup(
    name="Calculator",
    zipfile=None,
    data_files=[('assets', ['./assets/favicon.ico'])],
    windows=[{
        'script': './app.py',
        'icon_resources': [(1, './assets/favicon.ico')]
    }])
