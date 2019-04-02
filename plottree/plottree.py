#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
`plottree` - Plot a tree from terminal line with just a single line of code.
"""

import argparse
import os

from io import StringIO

from Bio import Phylo
import matplotlib.pylab as plt

HELP = """
Plot a phylogenetic tree with just a single line of code.

Usage: plottree TREE [options]

positional arguments:
  TREE                  A tree in NEWCIK format file or string.

optional arguments:
  -h, --help            show this help message and exit
  -a, --axes            Display ticks for x and y axes.
  -b, --box             Display the tree inside a box.
  -m TOP BOTTOM LEFT RIGHT, --margin TOP BOTTOM LEFT RIGHT
                        Set the margins of the figure, four numbers in the
                        order of top bottom left and right.
  -s SIZE, --size SIZE  Set the fontsize of leaf and node names.
  -x MIN MAX, --xlim MIN MAX
                        Set the limits for x-axis, two numbers for min and max.
  -y MIN MAX, --ylim MIN MAX
                        Set the limits for y-axis, two numbers for min and max.
  -o OUTPUT, --output OUTPUT
                        Save the figure into a file.
"""


def plot(tree, axes, box, margin, size, xlim, ylim, output):
    if os.path.isfile(tree):
        tree = Phylo.read(tree, 'nwick')
    elif tree.startswith('(') and tree.endswith(';'):
        tree = Phylo.read(StringIO(tree), 'newick')
    else:
        raise TypeError('Invalid tree, tree accepts NEWICK format file or string.')

    if size:
        plt.rcParams.update({'fontsize': size})
    fig, ax = plt.subplots()
    Phylo.draw(tree, do_show=False, axes=ax)
    if not axes:
        ax.set_xlabel(''), ax.set_ylabel('')
        ax.set_xticklabels([]), ax.set_yticklabels([])
    if not box:
        for spine in ax.spines.values():
            spine.set_visible(False)
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    if margin:
        plt.subplot_ajust(left=margin[2], bottom=margin[1], 
                          top=margn[0], right=margin[3])
    if output:
        fig.savefig(output)
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
    parser.add_argument('-m', '--margin', nargs=4,
                        help='Set the margins of the figure, four numbers in tht order of top bottom left and right.')
    parser.add_argument('-s', '--size', help='Set the fontsize of leaf and node names.')
    parser.add_argument('-x', '--xlim', nargs=2, 
                        help='Set the limits for x-axis, two numbers for min and max.')
    parser.add_argument('-y', '--ylim', nargs=2, 
                        help='Set the limits for y-axis, two numbers for min and max.')
    parser.add_argument('-o', '--output', help='Save the figure into a file.')

    args = parser.parse_args()
    plot(args.TREE, args.axes, args.box, args.margin, args.size, 
         args.xlim, args.ylim, args.output)

if __name__ == '__main__':
    main()

