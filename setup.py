try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'py2neo==2.0.6',
]

setup(
    name='neophyte',
    version='0.1',
    description="Assorted python scripts for Neo4j",
    long_description=readme,
    author="Smesh",
    url='https://github.com/sgarcez/neophyte',
    packages=[
        'neophyte',
    ],
    package_dir={'neophyte': 'neophyte'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)
