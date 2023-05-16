import sys
import os
import errno
from collections import Counter
from setup.settings import preprocessing, hparams
from core.tokenizer import tokenize
from core.sentence import score_answers, replace_in_answers
from tqdm import tqdm
from itertools import zip_longest
from multiprocessing import Pool
from threading import Thread
import time

files = {
    'train.from': {'amount': 1, 'up_to': -1},
    'tst2012.from': {'amount': .1, 'up_to': preprocessing['test_size']},
    'tst2013.from': {'amount': .1, 'up_to': preprocessing['test_size']},
    'train.to': {'amount': 1, 'up_to': -1},
    'tst2012.to': {'amount': .1, 'up_to': preprocessing['test_size']},
    'tst2013.to': {'amount': .1, 'up_to': preprocessing['test_size']},
}

vocab = Counter([])

def prepare_files():
    global vocab

    print("\nPreparing training set from raw set")

    try:
        os.makedirs(preprocessing['train_folder'])
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    train_log_dir = os.path.join(hparams['out_dir'], 'train_log')
    try:
        os.makedirs(train_log_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for file_name, amounts in files.items():

        vocab = Counter([])

        print("\nFile: {} (iteration = 10k lines)".format(file_name))

        out_file = open('{}/{}'.format(preprocessing['train_folder'], file_name), 'w', encoding='utf-8', buffering=131072)

        read = 0
        amount = int(min(amounts['amount'] * preprocessing['samples'] if preprocessing['samples'] > 0 else 10 ** 20,
                         amounts['up_to'] if amounts['up_to'] > 0 else 10 ** 20))

        write_thread = None
        vocab_thread1 = None
        vocab_thread2 = None

        with Pool(processes=preprocessing['cpu_count']) as pool:

            with open('{}/{}'.format(preprocessing['source_folder'], file_name), 'r', encoding='utf-8', buffering=131072) as in_file:

                for rows in tqdm(read_lines(in_file, 10000, '')):

                    rows = pool.map_async(tokenize, rows, 100).get()

                    if write_thread is not None:
                        write_thread.join()
                        vocab_thread1.join()
                        vocab_thread2.join()
