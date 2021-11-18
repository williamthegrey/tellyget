import sys

import datetime

from tellyget.utils.cipher import Cipher


def usage():
    print('Usage:')
    print('\t\ttellyget-decrypt -h')
    print('\t\ttellyget-decrypt <authenticator> [--all]')


def find_encryption_keys(authenticator, find_all=False):
    keys = []
    print('Searching for encryption keys in 00000000 - 99999999')
    for num in range(0, 100000000):
        key = f'{num:08}'
        # noinspection PyBroadException
        try:
            plain_text = Cipher(key).decrypt(authenticator)
            print(f'Found key: {key} Decrypted text: {plain_text}')
            keys.append(key)
            if not find_all:
                break
        except:
            pass
    print(f'Found {len(keys)} keys:\n{keys}')
    return keys


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    if sys.argv[1] == '-h':
        usage()
        sys.exit()

    authenticator = sys.argv[1]
    if len(sys.argv) == 2:
        find_all = False
    elif len(sys.argv) == 3 and sys.argv[2] == '--all':
        find_all = True
    else:
        usage()
        sys.exit(1)

    start = datetime.datetime.now()
    find_encryption_keys(authenticator, find_all)
    end = datetime.datetime.now()
    print(f'Time used: {end - start}')
