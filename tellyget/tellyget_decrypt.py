import datetime
import sys

from tellyget.utils.cipher import Cipher


def usage():
    print('Usage:')
    print('\t\ttellyget-decrypt -h')
    print('\t\ttellyget-decrypt <authenticator> [--all]')


def find_encryption_keys(authenticator, find_all=False, debug=False):
    keys = []
    if debug:
        print('Searching for encryption keys in 00000000 - 99999999')
    for num in range(0, 100000000):
        key = f'{num:08}'
        try:
            plain_text = Cipher(key).decrypt(authenticator)
            if debug:
                print(f'Found key: {key} Decrypted text: {plain_text}')
            keys.append(key)
            if not find_all:
                break
        except ValueError:
            pass
    if debug:
        print(f'Found {len(keys)} keys')
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
    find_encryption_keys(authenticator, find_all=find_all, debug=True)
    end = datetime.datetime.now()
    print(f'Time used: {end - start}')
