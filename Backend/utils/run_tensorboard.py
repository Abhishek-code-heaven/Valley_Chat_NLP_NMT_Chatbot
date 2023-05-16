import sys
import subprocess
from setup.settings import hparams

command = 'tensorboard --port 22222 --logdir {}'.format(hparams['out_dir'])
process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, bufsize=1)

for line in iter(process.stdout.readline, b''):
    print(line.decode('utf-8'), end='')

process.stdout.close()
process.wait()
