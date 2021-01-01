#!/usr/bin/env python3
'''
NEAT evolver script for OpenAI Gym environemnts

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import argparse
from argparse import ArgumentDefaultsHelpFormatter
from neat_gym import _GymNeatConfig, _GymHyperConfig, _GymEsHyperConfig, _evolve

# Parse command-line arguments, making --hyper and --eshyper mutuall exclusive
parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
group = parser.add_mutually_exclusive_group()
group.add_argument('--hyper', action='store_true', help='Use HyperNEAT')
group.add_argument('--eshyper', action='store_true', help='Use ES-HyperNEAT')
parser.add_argument('--env', default='CartPole-v1', help='Environment id')
parser.add_argument('--checkpoint', dest='checkpoint', action='store_true',
                    help='Save at each new best')
parser.add_argument('--config', required=False, default=None,
                    help='Config file; if None, uses config/<env-name>.cfg')
parser.add_argument('--ngen', type=int, required=False,
                    help='Number of generations to run')
parser.add_argument('--reps', type=int, default=10, required=False,
                    help='Number of repetitions per genome')
parser.add_argument('--seed', type=int, required=False,
                    help='Seed for random number generator')
args = parser.parse_args()

# Default to environment name for config file
cfgfile = 'config/' + args.env + '.cfg' if args.config is None else args.config

# Default to original NEAT
configfun = _GymNeatConfig.make_config

# Check for HyperNEAT, ES-HyperNEAT
if args.hyper:
    configfun = _GymHyperConfig.make_config
if args.eshyper:
    configfun = _GymEsHyperConfig.make_config

config, evalfun = configfun(args, cfgfile)

# Evolve
_evolve(config, evalfun, args.seed, args.env, args.ngen, args.checkpoint)
