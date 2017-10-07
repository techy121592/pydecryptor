#!/usr/bin/python3

import sys
import os
import argparse
from decrypter import Decrypter
from cypherfinder import CypherFinder

def find_and_print_cypher_and_decrypted_lines(corpus_path, encrypted_path, print_cypher, print_decrypted, verbose):
    cypher = CypherFinder(corpus_path, encrypted_path).get_cypher()
    decrypter = Decrypter(cypher)

    if print_decrypted or verbose:
        with open(encrypted_path) as encrypted_file:
            for line in encrypted_file:
                print(line)
                print(decrypter.decrypt(line))

    if print_cypher or verbose:
        for _, v in enumerate(cypher):
            print('{} = {}'.format(v, cypher[v]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', help='Path to corpus file.')
    parser.add_argument('encrypted', help='Path to encrypted file.')
    parser.add_argument('-c', '--cypher', help='Prints the cypher at the end.', action="store_true")
    parser.add_argument('-d', '--decrypted', help='Prints the decrypted lines at the end.', action="store_true")
    parser.add_argument('-v', '--verbose', help='Prints both the cypher and the decrypted lines at the end.', action="store_true")
    args = parser.parse_args()

    if not os.path.isfile(args.corpus):
        print('Invalid corpus path')
        return
    if not os.path.isfile(args.encrypted):
        print('Invalid encrypted path')
        return

    find_and_print_cypher_and_decrypted_lines(args.corpus, args.encrypted, args.cypher, args.decrypted, args.verbose)


if __name__ == '__main__':
    main()
