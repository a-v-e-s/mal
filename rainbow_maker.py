"""
rainbowmaker.py (untested)
Convert passwords from a gigantic text file into associated hash values

-Jon David Tannehill
"""

import hashlib, gzip, pickle, optparse
from os.path import isdir, isfile, join
from itertools import islice

INCREMENT = 100000
Metadict = {}


def rainbow_maker(file, function, dire, salt_prefix=None, salt_suffix=None):
    length = sum(1 for line in open(file, 'r'))
    lines_read = 0
    with open(file, 'rb') as f:
        while lines_read < length:
            megadict = {}
            if (length - lines_read) >= INCREMENT:
                chunk = islice(f, lines_read, lines_read + INCREMENT)
                for x in chunk:
                    megadict[x] = (
                        function(salt_prefix + x).digest() if salt_prefix
                        else function(x + salt_suffix).digest() if salt_suffix
                        else function(x).digest()
                    )
                lines_read += INCREMENT
            elif lines_read < length:
                chunk = islice(f, lines_read, length)
                for x in chunk:
                    megadict[x] = (
                        function(salt_prefix + x).digest() if salt_prefix
                        else function(x + salt_suffix).digest() if salt_suffix
                        else function(x).digest()
                    )
                lines_read = length
            #
            first_4 = sorted(list(megadict.keys()))[:4]
            Metadict[first_4] = megadict
    #
    with open(join(dire, 'rainbow_table_' + str(function.__name__)), 'wb') as g:
        g.write(bytes(gzip.compress(pickle.dumps(Metadict))))


if __name__ == '__main__':
    path = input('Enter the path to the password text file:\n')
    if not isfile(path):
        raise FileNotFoundError(path, 'is not a file')
    #
    print('\nChoose a hash function to use:')
    count = 1
    options = {}
    for x in hashlib.algorithms_available:
        print(str(count) + ') ' + x)
        options[count] = x
        count += 1
    choice = int(input('\n# of Choice: '))
    if choice not in range(1, len(hashlib.algorithms_available) + 1):
        raise ValueError('Invalid choice #')
    #
    dire = input('\nEnter the directory path to save the results to:\n')
    if not isdir(dire):
        raise NotADirectoryError(dire, 'is not a directory')
    #

    rainbow_maker(path, options[choice], dire, salt_prefix, salt_suffix)