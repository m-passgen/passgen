"""
Password generation tool. Usage:
1.) passgen -> Combine password and a suffix (separated by a space) and hash with PBKDF2-SHA256.
2.) passgen n -> Generate a DiceWare password of length n using the EFF short wordlist.
3.) passgen n m -> Runs the "passgen n" command m times.
"""

import binascii as b
import getpass
import hashlib as h
import sys
from random import SystemRandom

checksum_indices_list = [
    ('Checksum 1', range(0, 5)),
]


def pbkdf2(password):
    return b.hexlify(h.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)).decode()


def generate_password():
    password = ''
    # Get master password:
    pass_correct = False
    while not pass_correct:
        password = getpass.getpass('Enter master password: ')
        checksum = pbkdf2(password)
        for checksum_indices in checksum_indices_list:
            name = checksum_indices[0]
            indices = checksum_indices[1]
            print(name + ': ' + ''.join([checksum[i] for i in indices]))
        pass_correct = True if getpass.getpass('Correct? (y = yes): ') in ['y', 'Y'] else False
    # Generate passwords as required:
    next_pass = True
    while next_pass:
        # Calculate password:
        suffix = getpass.getpass('Enter suffix: ')
        hash_value = pbkdf2(password + ' ' + suffix)
        output = hash_value[:16] + 'A'
        # Print result:
        print('Full hash: ' + hash_value)
        print('\n')
        print('Suffix: #' + suffix + '#')
        print(output)
        print('\n')
        next_pass = False if getpass.getpass('Another password? (n = no): ') in ['n', 'N'] else True


def test_libraries():
    expected = '0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5'
    # Check libraries work as expected:
    test = pbkdf2('password')
    if test == expected:
        return True
    else:
        print('Expected: #' + expected + '#')
        print('Found:    #' + test + '#')
        print('\nERROR: Library test failed\n')
        return False


def generate_master(word_count, repeat):
    print('\n')
    for _ in range(repeat):
        # Convert word list into map
        dice_word_map = {}
        for line in open(sys.path[0] + '/eff_short_wordlist_1.txt').readlines():
            pair = line.replace('\n', '').split('\t')
            dice_word_map.update({pair[0]: pair[1]})
        # Generate dice values to get password of required length
        words = []
        for _ in range(word_count):
            dice_val = ''.join([str(SystemRandom().randrange(6) + 1) for _ in range(4)])
            words += [dice_word_map[dice_val]]
        password = ' '.join(words)
        print('\n' + password + '\n')
    print('\n')


if __name__ == '__main__':
    if len(sys.argv) > 2:
        generate_master(int(sys.argv[1]), int(sys.argv[2]))
    elif len(sys.argv) > 1:
        generate_master(int(sys.argv[1]), 1)
    elif test_libraries():
        generate_password()
