
import os
import configparser

from lambda_function import process

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read(['config.cfg'])

    process(config['DEFAULT'])
