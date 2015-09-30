#!/usr/bin/env python

import logging
import sys
from random import choice
from os import listdir
from os.path import isfile, join, abspath, expanduser
from strategy import charlie_miller_fuzz, radamsa_fuzz, bitflip_fuzz, nill_fuzz
from settings import *


logger = logging.getLogger('mutilator')


def run(seed_dir, samples_dir):
    file_list = [f for f in listdir(seed_dir) if isfile(join(seed_dir, f))]
    file_list.remove('.ignore')

    itr = 0
    logger.info('Starting Mutilator with {}'.format(STRATEGY))
    while True:
        itr = itr + 1
        try:
            file_choice = join(seed_dir, choice(file_list))
        except IndexError:
            logger.error('No seeds found')
            sys.exit(1)

        fd = open(abspath(file_choice), 'rb')
        buf = bytearray(fd.read())
        fd.close()

        # Load & Run Mutation Strategy
        buf = globals()[STRATEGY](buf, itr)

        new_filename = join(samples_dir, "sample_{}".format(itr))
        logger.debug('Creating file: {}'.format(new_filename))
        fd = open(new_filename, 'wb')
        fd.write(buf)
        fd.close()



if __name__ == '__main__':
    run(SEED_DIRECTORY, SAMPLES_DIRECTORY)
