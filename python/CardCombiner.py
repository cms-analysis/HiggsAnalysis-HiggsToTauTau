'''

Tool for combining datacards together

'''

import tempfile
import glob
import subprocess
import logging
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

    txt2ws_options is a dictionary of '--option' : 'value' pairs
    that will be passed to text2workspace.py

    One can pass multi-arg options like::

        --X-rescale-nuisance CMS_eff_t_high_8TeV 5

    using a tuple::

        {'--X-rescale-nuisance': ('CMS_eff_t_high_8TeV', 5), ... }

    Note: you need to at _minimum_ pass {'-m': 'THEMASS'} in txt2ws_options

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
        for option, value in txt2ws_options.iteritems():
            cmd.append(option)
            # Check if the value is just a plain string
            if isinstance(value, (basestring, float, int)):
                cmd.append(str(value))
            else:
                # It's a list or tuple
                for x in value:
                    cmd.append(str(x))
        log.info("Create workspace: %s", " ".join(cmd))
        return subprocess.call(cmd)
