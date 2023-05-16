import os

package_path = os.path.realpath(os.path.dirname(__file__) + '/..')

out_dir = os.path.join(package_path, "model")

train_dir = os.path.join(package_path, "data")

source_dir = os.path.join(package_path, "new_data")

preprocessing = {
    'samples': -1,
    'vocab_size': 30000,
    'test_size': 100,
    'source_folder': source_dir,
    'train_folder': train_dir,
    'protected_phrases_file': os.path.join(package_path, 'setup/protected_phrases.txt'),
    'answers_blacklist_file': os.path.join(package_path, 'setup/answers_blacklist.txt'),
    'answers_detokenize_file': os.path.join(package_path, 'setup/answers_detokenize.txt'),
    'answers_replace_file': os.path.join(package_path, 'setup/answers_replace.txt'),
    'vocab_blacklist_file': os.path.join(package_path, 'setup/vocab_blacklist.txt'),
    'vocab_replace_file': os.path.join(package_path, 'setup/vocab_replace.txt'),
    'cpu_count': None,
}

hparams = {
    'attention': 'scaled_luong',
    'src': 'from',
    'tgt': 'to',
    'vocab_prefix': os.path.join(train_dir, "vocab"),
    'train_prefix': os.path.join(train_dir, "train"),
    'dev_prefix': os.path.join(train_dir, "tst2012"),
    'test_prefix': os.path.join(train_dir, "tst2013"),
    'out_dir': out_dir,
    'num_train_steps': 500000,
    'num_layers': 2,
    'num_units': 512,
    'optimizer': 'adam',
    'encoder_type': 'bi',
    'learning_rate': 0.001,
    'beam_width': 10,
    'length_penalty_weight': 1.0,
    'num_translations_per_input': 10
}