from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(name='grafanacli',
      version='1.0.5',
      description='Library to manage Grafana API',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/JeferCatarina/grafanacli',
      author='Jeferson Catarina',
      author_email='catarinajeferson@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Topic :: Internet',
          'Topic :: System :: Monitoring',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ]
      )
