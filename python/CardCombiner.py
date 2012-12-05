'''

Tool for combining datacards together

'''

import tempfile
import glob
import subprocess
import logging
import re
import sys

log = logging.getLogger('cardcombiner')
logging.basicConfig(level=logging.INFO)


def combine_cards(card_globs, output_stream=sys.stdout):
    ''' Combine .txt cards

    card_globs can a single glob or a list of globs corresponding to a set of
    files or wildcards.  The output_stream can be set to an open file if
    desired.
    '''
    # Build the shell command
    cmd = [
        'combineCards.py',
        '-S',
    ]
    if isinstance(card_globs, basestring):
        card_globs = [card_globs]
    cards = set([])
    for card_glob in card_globs:
        for card in glob.glob(card_glob):
            cards.add(card)
    if not cards:
        raise IOError("No cards matched by: " + " ".join(card_globs))
    cmd.extend(cards)
    log.info("Running card combine: %s", " ".join(cmd))
    return subprocess.call(cmd, stdout=output_stream)


def create_workspace(output_file, card_globs, txt2ws_options=None):
    ''' Merge .txt datacards pointed to by card_globs into a RooWorkspace

    txt2ws_options is a list of tuples of '--option' : 'value' pairs
    that will be passed to text2workspace.py

    One can pass multi-arg options like::

        --X-rescale-nuisance CMS_eff_t_high_8TeV 5

    using a tuple::

        ('--X-rescale-nuisance': 'CMS_eff_t_high_8TeV', 5)

    Note: you need to at _minimum_ pass ('-m', 'THEMASS') in txt2ws_options

    '''
    # Create a temporary txt file
    with tempfile.NamedTemporaryFile() as tmp_file:
        combine_cards(card_globs, output_stream=tmp_file)
        # Make sure it's all written to disk.
        tmp_file.flush()
        cmd = [
            'text2workspace.py',
            '-b', tmp_file.name,
            '-o', output_file,
        ]
        for option_tuple in txt2ws_options:
            for x in option_tuple:
                cmd.append(str(x))
        log.info("Create workspace: %s", " ".join(cmd))
        return subprocess.call(cmd)

_pull_match = re.compile(
    '^(?P<systematic>\S*).*\((?P<bfit>.*)\).*\((?P<sfit>.*)\)')


def extract_pull(pull_str):
    ''' Determines pull and post-fit error from a pull fragment

    >>> " ".join("%0.2f" % x for x in extract_pull("(+0.24sig, 0.79)"))
    '0.24 0.79'
    >>> " ".join("%0.2f" % x for x in extract_pull("(-0.24sig, 0.79)"))
    '-0.24 0.79'
    '''
    pull_str = pull_str.replace(')', '')
    pull_str = pull_str.replace('(', '')
    fields = pull_str.split('sig,')
    return float(fields[0]), float(fields[1])


def extract_pull_options(pull_file, bonly=True):
    ''' Reads in an ML fit output and builds the command line options
    needed to apply the set of pulls to a datacard '''
    # We write the options in terms of a set of tuples
    output = []
    for line in pull_file.readlines():
        match = _pull_match.match(line.strip())
        if match:
            name = match.group('systematic')
            bfit = extract_pull(match.group('bfit'))
            sfit = extract_pull(match.group('sfit'))
            log.debug("Found systematic: %s bfit: %s sfit: %s",
                      name, bfit, sfit)
            fit_to_use = bfit if bonly else sfit
            output.append(
                ('--X-rescale-nuisance', name, fit_to_use[1])
            )
            output.append(
                ('--X-shift-nuisance', name, fit_to_use[0]),
            )
    return output

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    ml = open('test_cardz/125/out/mlfit.txt', 'r')
    import pprint
    pprint.pprint(extract_pull_options(ml))
