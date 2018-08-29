#!/usr/bin/python


import sys
import argparse


def parser(__version__, description):
    parser = argparse.ArgumentParser(
        description='Meraki Tools {}'.format(description),
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False)
    # Misc arguments are meant for informational help-based arguments
    misc = parser.add_argument_group('Misc Arguments')
    # Required arguments are needed to start the program
    required = parser.add_argument_group('Required Arguments')
    # Optional arguments are not required for the start of the program
    optional = parser.add_argument_group('Optional Arguments')
    misc.add_argument(
                        "-h", "--help",
                        help="show this help message and exit",
                        action="help")
    misc.add_argument(
                        "-v", "--version",
                        action="version",
                        version="Meraki Tools {}\nPython {}".format(
                            __version__, sys.version))
    required.add_argument(
                        '-k', "--api_key",
                        help="Meraki API Key",
                        metavar='KEY',
                        dest="api_key")
    return (parser, misc, required, optional)