#!/usr/bin/env python

import logging
import sys
from random import choice
from os import listdir
from os.path import isfile, join, abspath, expanduser
from time import strftime
from strategy import *


logger = logging.getLogger('mutilator')


def run(seed_dir, samples_dir, strategy, max_total_mutations, strategy_args=dict()):
    file_list = [f for f in listdir(seed_dir) if isfile(join(seed_dir, f))]
    try:
        file_list.remove('.ignore')
    except ValueError:
        pass

    itr = 0
    logger.info('Starting Mutilator with {}'.format(strategy))
    while True:
        if max_total_mutations:
            if max_total_mutations < itr:
                logger.warning('Reached the limit of {} mutations.'.format(max_total_mutations))
                sys.exit(0)
        itr = itr + 1
        try:
            file_choice = join(seed_dir, choice(file_list))
        except IndexError:
            logger.error('No seeds found in {}'.format(seed_dir))
            sys.exit(1)

        fd = open(abspath(file_choice), 'rb')
        buf = bytearray(fd.read())
        fd.close()

        # Load & Run Mutation Strategy
        try:
            # TODO : Allow to set strategy_args with --tool mutilator or when mutilator is standalone
            buf = globals()[strategy](buf, itr, **strategy_args)
        except KeyError:
            logger.fatal('Strategy {} does not exist.'.format(strategy))
        except TypeError:
            logger.fatal('Strategy {} is missing arguments.'.format(strategy))

        stamp = strftime('%y%m%d%H%M%S')
        new_filename = join(samples_dir, 'sample_{}_{}'.format(stamp, itr))
        logger.debug('Creating file: {}'.format(new_filename))
        fd = open(new_filename, 'wb')
        fd.write(buf)
        fd.close()



if __name__ == '__main__':
    from settings import *
    run(SEED_DIRECTORY, SAMPLES_DIRECTORY, STRATEGY, MAX_TOTAL_MUTATIONS)
