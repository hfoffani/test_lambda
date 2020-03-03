
import os
import configparser

from lambda_function import process

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read(['config.cfg'])

    for k in config['DEFAULT']:
        os.environ[k] = config['DEFAULT'][k]

    process('aus')
