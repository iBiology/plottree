#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PLOTTREE - Plot a phylogenetic tree with just a single line of code.

Usage: plottree TREE [options]

positional arguments:
  TREE                  A tree in NEWCIK format file or string (surrounded by
                        double quotes).

optional arguments:
  -h, --help            show this help message and exit
  -a, --axes            Display ticks for x and y axes.
  -b, --box             Display the tree inside a box.
  -c, --confidence      Display confidence values, if present on the tree.
  -n, --name            Display name for internal node, if present on the
                        tree.
  -s SIZE, --size SIZE  Set the fontsize of leaf and node names.
  -w WIDTH, --width WIDTH
                        Set the width of the figure.
  -l HEIGHT, --height HEIGHT
                        Set the height of the figure
  -x XLIM XLIM, --xlim XLIM XLIM
                        Set the limits for x-axis, two numbers for min and max.
  -y YLIM YLIM, --ylim YLIM YLIM
                        Set the limits for y-axis, two numbers for min and max.
  -o OUTPUT, --output OUTPUT
                        Save the figure into a file.
"""

import argparse
import os
import sys

from io import StringIO

from Bio import Phylo
import matplotlib as mpl
import matplotlib.pylab as plt


def plot(tree, axes, box, confidence, name, size, width, height, x, y, output):
    if os.path.isfile(tree):
        tree = Phylo.read(tree, 'newick')
    elif tree.startswith('(') and tree.endswith(';'):
        tree = Phylo.read(StringIO(tree), 'newick')
    else:
        raise TypeError('Invalid tree, tree only accepts NEWICK format file or '
                        'string.')
    
    settings = []
    size = size or mpl.rcParams.get('font.size', 8)
    mpl.rcParams.update({'font.size': size})
    settings.append(f'fontsize (-s): {size:.1f}')
    
    fig, ax = plt.subplots()
    
    w, h = fig.get_size_inches()
    width, height = width or w, height or h
    fig.set_size_inches(width, height, forward=True)
    settings.append(f'width (-w): {width:.1f}')
    settings.append(f'height (-l): {height:.1f}')
    
    for clade in tree.find_clades():
        if not name and not clade.is_terminal():
            clade.name = None
    
    Phylo.draw(tree, do_show=False, axes=ax, show_confidence=confidence)
    
    x, y = x or ax.get_xlim(), y or ax.get_ylim()
    ax.set_xlim(*x), ax.set_ylim(*y)
    settings.append(f'xlim(-x): {x[0]:.2f}, {x[1]:.2f}')
    settings.append(f'ylim(-y): {y[0]:.2f}, {y[1]:.2f}')
    
    if axes:
        settings.append(f'Display axes ticks for further tuning: -a')
        plt.subplots_adjust(left=0.05, bottom=0.05, top=0.99, right=0.99)
    else:
        plt.subplots_adjust(left=0.01, bottom=0.01, top=0.99, right=0.99)
        ax.set_xticks([]), ax.set_yticks([])
        ax.set_xticklabels([]), ax.set_yticklabels([])
    ax.set_xlabel(''), ax.set_ylabel('')
    
    if box:
        settings.append('Plot a box surrounding the tree: -b')
    else:
        if axes:
            ax.spines['left'].set_visible(True)
            ax.spines['bottom'].set_visible(True)
        else:
            for spine in ax.spines.values():
                spine.set_visible(False)
    if confidence:
        settings.append('Display confidence on the tree: -c')
    if name:
        settings.append('Display internal node name: -n')
    
    if output:
        settings.append(f'output figure to file (-o): {output}')
        fig.savefig(output)

    print('\nPlotting tree using the following setting:')
    print('\t{}'.format('\n\t'.join(settings)))
    print('Feel free to modify them to tune the figure nice.')
    
    plt.show()


def main():
    des = 'Plot a phylogenetic tree with just a single line of code.'
    parser = argparse.ArgumentParser(
            description=des,
            prog='plottree',
            usage='%(prog)s TREE [options]')
    parser.add_argument('TREE', help='A tree in NEWCIK format file or string.')
    parser.add_argument('-a', '--axes', action='store_true',
                        help='Display ticks for x and y axes.')
    parser.add_argument('-b', '--box', action='store_true', 
                        help='Display the tree inside a box.')
    parser.add_argument('-c', '--confidence', action='store_true',
                        help='Display confidence values, if present on the '
                             'tree.')
    parser.add_argument('-n', '--name', action='store_true',
                        help='Display name for internal node, if present on '
                             'the tree.')
    parser.add_argument('-s', '--size', type=float,
                        help='Set the fontsize of leaf and node names.')
    parser.add_argument('-w', '--width', type=float,
                        help='Set the width of the figure.')
    parser.add_argument('-l', '--height', type=float,
                        help='Set the height of the figure')
    parser.add_argument('-x', '--xlim', nargs=2, type=float,
                        help='Set the limits for x-axis, two numbers for '
                             'min and max.')
    parser.add_argument('-y', '--ylim', nargs=2, type=float,
                        help='Set the limits for y-axis, two numbers for '
                             'min and max.')
    parser.add_argument('-o', '--output', help='Save the figure into a file.')

    args = parser.parse_args()
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print(__doc__.rstrip())
        else:
            args = parser.parse_args()
            plot(args.TREE, args.axes, args.box, args.confidence,
                 args.name, args.size, args.width, args.height, args.xlim,
                 args.ylim, args.output)
    else:
        # print(__doc__.rstrip())
        pass

if __name__ == '__main__':
    main()
    