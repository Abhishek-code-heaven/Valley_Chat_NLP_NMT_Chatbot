import sys
import os
import argparse
from setup.settings import hparams
from nmt import nmt
import tensorflow as tf


def main():
    nmt_parser = argparse.ArgumentParser()
    nmt.add_arguments(nmt_parser)
    nmt.FLAGS, unparsed = nmt_parser.parse_known_args(['--'+k+'='+str(v) for k,v in hparams.items()])
    tf.compat.v1.app.run(main=nmt.main, argv=[os.getcwd() + '/nmt/nmt/nmt.py'] + unparsed)


if __name__ == "__main__":
    main()
