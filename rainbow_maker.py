"""
rainbowmaker.py (untested)
Convert passwords from a gigantic text file into associated hash values

-Jon David Tannehill
"""

import hashlib, gzip, pickle, optparse
from os.path import isdir, isfile, join
from itertools import islice

INCREMENT = 1000000
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
            first_8 = sorted(list(megadict.keys()))[:8]
            Metadict[first_8] = megadict
    #
    with open(join(dire, 'rainbow_table_' + str(function.__name__)), 'wb') as g:
        if length > 1000000:
            g.write(bytes(gzip.compress(pickle.dumps(Metadict))))
        else:
            g.write(bytes(pickle.dumps(Metadict)))


if __name__ == '__main__':
    parser = optparse.OptionParser(
        'usage: %prog -f <password_file> -d <directory_to_save_to> [-p <salt_prefix> | -u <salt_suffix>]'
    )
    parser.add_option('-f', dest='path', type='string', help='path to password file')
    parser.add_option('-d', dest='dire', type='string', help='directory to save rainbow table to')
    parser.add_option('-p', dest='salt_prefix', type='string', help='salt prefix, if applicable')
    parser.add_option('-u', dest='salt_suffix', type='string', help='salt suffix, if applicable')
    (options, args) = parser.parse_args()
    path = options.path
    dire = options.dire
    if not isfile(path):
        raise FileNotFoundError(path, 'is not a file')
    if not isdir(dire):
        raise NotADirectoryError(dire, 'is not a directory')
    salt_prefix = options.salt_prefix if options.salt_prefix else None
    salt_suffix = options.salt_suffix if options.salt_suffix else None
    try:
        assert not (salt_prefix and salt_suffix)
    except AssertionError:
        print('Cannot have both salt prefix and suffix.')
        exit(1)
    #
    print('\nChoose a hash function to use:')
    count = 1
    hash_funcs = {}
    for x in hashlib.algorithms_available:
        print(str(count) + ') ' + x)
        hash_funcs[count] = x
        count += 1
    choice = int(input('\n# of Choice: '))
    if choice not in range(1, len(hashlib.algorithms_available) + 1):
        raise ValueError('Invalid choice #')
    function = getattr(hashlib, hashfuncs[choice])
    #
    rainbow_maker(path, function, dire, salt_prefix, salt_suffix)