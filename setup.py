#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

VERSION = '0.0.1'

wd = os.path.abspath(os.path.dirname(__file__))


def readme():
    with open(os.path.join(wd, 'README.rst')) as f:
        return f.read()


setup(name='plottree',
      version=VERSION,
      description="""plottree - A command tool for quickly visualizing
      phylogenetic tree via a single command in terminal.""",
      long_description=readme(),
      url='https://github.com/iBiology/plottree',
      author='FEI YUAN',
      author_email='yuanfeifuzzy@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['biopython', 'matplotlib>='],
      entry_points={
          'console_scripts': ['plottree=plottree.plottree:main']
          },
      include_package_data=True,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          ],
      keywords='phylogeny tree dendrogram visualization plot bioinformatics'
      )


if __name__ == '__main__':
    pass
