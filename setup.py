from setuptools import setup, find_packages

setup(
    name='MaxquantTools',
    version='1.0-SNAPSHOT',
    packages=find_packages(),
    author='Christian Poitras',
    author_email='christian.poitras@ircm.qc.ca',
    description='Utilities for MaxQuant',
    keywords='bioinformatics, MaxQuant',
    url='https://github.com/benoitcoulombelab/maxquant-tools',
    license='MIT License',
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.7.4',
    install_requires=[
        'click>=7.0',
        'PyYAML>=6.0'
    ],
    entry_points={
        'console_scripts': [
            'fixparameters = maxquanttools.FixParameters:fixparameters',
            'maxquant = maxquanttools.Maxquant:maxquant',
        ]
    }
)
