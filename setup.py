from setuptools import setup, find_packages
import os

name = "collective_stats_logviewer"
version = "0.1"


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name=name,
    version=version,
    description="A simple log stat viewer app",
    long_description=read('README.rst'),
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords="",
    author="",
    author_email='',
    url='',
    license='',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Flask',
        'Flask-SQLAlchemy',
        'requests',
    ],
    entry_points="""
    [console_scripts]
    flask-ctl = collective_stats_logviewer.script:run

    [paste.app_factory]
    main = collective_stats_logviewer.script:make_app
    debug = collective_stats_logviewer.script:make_debug
    """,
)
