#!/usr/bin/python3

#####################################################################################
# Copyright (C) 2017  David Welch                                                   #
#                                                                                   #
# This program is free software; you can redistribute it and/or                     #
# modify it under the terms of the GNU General Public License                       #
# as published by the Free Software Foundation; either version 2                    #
# of the License, or (at your option) any later version.                            #
# this program is distributed in the hope that it will be useful,                   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                    #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                     #
# GNU General Public License for more details.                                      #
# You should have received a copy of the GNU General Public License                 #
# along with this program; if not, write to the Free Software                       #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.   #
#####################################################################################

import sys
import os
import argparse
from decrypter import Decrypter
from cypherfinder import CypherFinder

def find_and_print_cypher_and_decrypted_lines(corpus_path, encrypted_path, print_cypher, print_decrypted, verbose):
    found_cypher, cypher = CypherFinder(corpus_path).get_cypher(encrypted_path)
    if found_cypher:
        decrypter = Decrypter(cypher)
        if print_decrypted or verbose:
            with open(encrypted_path) as encrypted_file:
                for line in encrypted_file:
                    print('{} = {}'.format(line.replace('\n', ''), decrypter.decrypt(line)))

        if print_cypher or verbose:
            for _, v in enumerate(sorted(cypher)):
                print('{} = {}'.format(v, cypher[v]))
    else:
        print('Could not find cypher')

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
