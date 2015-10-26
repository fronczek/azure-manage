# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import argparse

from ..config import Config


class ArgsActionDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        namespace_values = getattr(namespace, self.dest, None) or {}

        key, value = values.split('=', 1)
        namespace_values[key] = value

        setattr(namespace, self.dest, namespace_values)


def setup_argparse(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--auto', action='store_true')
    parser.add_argument('--config', metavar='CONFIG', default=None)
    parser.add_argument('--option', metavar='OPTION=VALUE', dest='options',
            default={}, action=ArgsActionDict)
    parser.add_argument('--workdir', metavar='WORKDIR',
            help='working directory (default: ./SECTION-VERSION)')
    parser.add_argument('section', metavar='SECTION')
    parser.add_argument('version', metavar='VERSION')
    return parser


class CliBase:
    parser = setup_argparse(description='Base')

    def __init__(self, args=None):
        self.args = self.parser.parse_args(args)

        if self.args.config:
            with open(self.args.config) as c:
                self.config_section = Config(c)[self.args.section]
        else:
            self.config_section = {}

        self.config_section.update(self.args.options)

    @property
    def workdir(self):
        return self.args.workdir or './{section}-{version}'.format_map(vars(self.args))
