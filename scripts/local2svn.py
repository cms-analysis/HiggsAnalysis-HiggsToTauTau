#!/usr/bin/env python


'''

Copy some datacards to the SVN area.

'''

from RecoLuminosity.LumiDB import argparse
import os
import shutil
import logging
import re
import sys
log = logging.getLogger('local2svn')
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

_matcher = re.compile('(?P<preamble>.*)-(?P<mass>[0-9\.]*).txt')

def parse_card_path(fullpath):
    ''' Determine relevant information about a card from its path

    Returns:
        channel (htt or vhtt)
        mass
        combo card name

    >>> parse_card_path('sm/vhtt/vhtt_0_7TeV-125.5.txt')
    ('vhtt', 'vhtt', '125.5', 'vhtt_0_7TeV.txt')
    >>> parse_card_path('sm/mt/htt_mt_5_8TeV-130.txt')
    ('htt', 'htt_mt', '130', 'htt_mt_5_8TeV.txt')

    '''
    dir, card = os.path.split(fullpath)
    assert(dir.split('/'))
    channel_path = dir.split('/')[-1] # get channel type
    channel = 'vhtt' if channel_path == 'vhtt' else 'htt'

    match = _matcher.match(card)
    assert(match)

    return (channel, match.group('mass'), match.group('preamble')  + '.txt')

def find_root_files(cardfile):
    ''' Find the matching shape files for a card '''
    cards = set([])
    with open(cardfile, 'r') as card:
        for line in card:
            if 'shapes' in line:
                card_file = line.split(' ')[3]
                cards.add(os.path.join(os.path.dirname(cardfile), card_file))
    return cards

def copy_and_replace(inputfile, outputfile, fromstr, tostr):
    ''' Copy a file from input to output, making a str replacement '''
    with open(inputfile, 'r') as input:
        with open(outputfile, 'w') as output:
            for line in input:
                output.write(line.replace(fromstr, tostr))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('cards', nargs='+', help='Data cards to copy')
    parser.add_argument('--output', default='hcp2012',
                        help='HCG SVN directory')
    parser.add_argument('--dry-run', action='store_true', dest='dry')
    args = parser.parse_args()

    # Shape files we need to copy over
    shape_copies = set([])

    for card in args.cards:
        chan, mass, card_name = parse_card_path(card)
        root_files = find_root_files(card)
        # Require only 1 shape file/card
        assert(len(root_files) == 1)
        shape_file = tuple(root_files)[0]
        shape_file_name = os.path.basename(shape_file)
        output_dir = os.path.join(args.output, chan, mass)
        output_file = os.path.join(output_dir, card_name)
        log.info("Card %s => %s", card, output_file)
        if not args.dry:
            copy_and_replace(
                card, output_file, shape_file_name, "../common/%s" % shape_file_name)
            # Copy over the root file
        shape_copies.add(
            (shape_file, os.path.normpath(os.path.join(
                output_dir,
                "../common/%s" % shape_file_name)))
        )

    for fromfile, tofile in shape_copies:
        log.info("Shape %s => %s", fromfile, tofile)
        if not args.dry:
            shutil.copyfile(fromfile, tofile)
