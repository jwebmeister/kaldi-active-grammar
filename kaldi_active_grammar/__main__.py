#
# This file is part of kaldi-active-grammar.
# (c) Copyright 2019 by David Zurow
# Licensed under the AGPL-3.0, with exceptions; see LICENSE.txt file.
#

import logging, os.path, shutil

import six

from . import _log, _name
from .utils import debug_timer
from .compiler import Compiler
from .model import Model, convert_generic_model_to_agf

def compile_dictation_graph(model_dir, tmp_dir, g_filepath=None):
    compiler = Compiler(model_dir, tmp_dir)
    if g_filepath is None: g_filepath = compiler.default_dictation_g_filepath
    with debug_timer(six.print_, "graph compilation", independent=True):
        compiler.compile_dictation_fst(g_filepath)

def main():
    import argparse
    parser = argparse.ArgumentParser(prog='python -m %s' % _name)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-m', '--model_dir')
    parser.add_argument('-t', '--tmp_dir')
    parser.add_argument('command', choices=['compile_dictation_graph', 'convert_generic_model_to_agf', 'add_word'])
    # FIXME: helps
    # FIXME: subparsers?
    args, unknown = parser.parse_known_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    if args.command == 'compile_dictation_graph':
        if not args.model_dir: parser.error("MODEL_DIR required for compile_dictation_graph")
        compile_dictation_graph(args.model_dir, args.tmp_dir, unknown[0])
    if args.command == 'convert_generic_model_to_agf':
        if not args.model_dir: parser.error("MODEL_DIR required for convert_generic_model_to_agf")
        convert_generic_model_to_agf(unknown[0], args.model_dir)
    if args.command == 'add_word':
        if not args.model_dir: parser.error("MODEL_DIR required for add_word")
        Model(args.model_dir).add_word(unknown[0], unknown[1].split())

if __name__ == '__main__':
    main()
