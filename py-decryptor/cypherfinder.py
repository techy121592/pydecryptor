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

from collections import OrderedDict

class CypherFinder:
    def __init__(self, corpus_path, verbose):
        self.bag_of_words, self.verbose = self.load_clean_bag_of_words_from_file(corpus_path), verbose

    def load_clean_bag_of_words_from_file(self, file_path):
        with open(file_path) as file:
            return list(map(self.remove_non_alpha, set(file.read().split())))

    def remove_non_alpha(self, input):
        output = ''
        for letter in list(input):
            if letter.isalpha():
                output = output + letter
        return output

    def convert_word_to_numbers(self, word):
        key = {}
        next_number = 0
        list_of_numbers = []
        for letter in list(word):
            letter = letter.lower()
            letter_value = key.get(letter, next_number)
            if letter_value == next_number:
                next_number = next_number + 1
                key[letter] = letter_value
            list_of_numbers.append(letter_value)
        return list_of_numbers

    def get_possible_words(self, encrypted_word):
        numeric_encrypted_word, possible_words = self.convert_word_to_numbers(encrypted_word), []
        for word in self.bag_of_words:
            if self.convert_word_to_numbers(word) == numeric_encrypted_word:
                possible_words.append(word)
        return possible_words

    def get_possible_word_sets(self, encrypted_words):
        word_sets = {}
        for encrypted_word in encrypted_words:
            word_sets[encrypted_word] = self.get_possible_words(encrypted_word)

        ordered_word_sets = sorted(word_sets.items(), key=lambda word_set: (len(word_set[1])))
        
        return OrderedDict(ordered_word_sets)

    def try_to_add_letter_pair_to_cypher(self, encrypted_letter, letter, cypher):
        new_cypher = cypher.copy()
        if cypher.get(encrypted_letter, letter) == letter:
            new_cypher[encrypted_letter] = letter
            return True, new_cypher
        else:
            return False, {}

    def try_to_add_word_pair_to_cypher(self, encrypted_word, possible_word, cypher):
        new_cypher = cypher.copy()
        for encrypted_letter, letter in zip(list(encrypted_word), list(possible_word)):
            added_letter_to_cypher, new_cypher = self.try_to_add_letter_pair_to_cypher(encrypted_letter.lower(), letter.lower(), new_cypher)
            if not added_letter_to_cypher:
                return False, {}
        return True, new_cypher

    def look_for_cypher(self, list_of_encrypted_words_with_possible_words_param, cypher_param):
        encrypted_word, found_cypher, list_of_encrypted_words_with_possible_words, cypher = next(iter(list_of_encrypted_words_with_possible_words_param)), False, list_of_encrypted_words_with_possible_words_param.copy(), cypher_param.copy()
        possible_words = list_of_encrypted_words_with_possible_words[encrypted_word]
        del list_of_encrypted_words_with_possible_words[encrypted_word]

        for possible_word in possible_words:
            added_word, new_cypher = self.try_to_add_word_pair_to_cypher(encrypted_word, possible_word, cypher)
            if added_word and len(list_of_encrypted_words_with_possible_words) >= 1:
                if self.verbose:
                    print('Added appropriate keys for {} = {}'.format(encrypted_word, possible_word))
                return self.look_for_cypher(list_of_encrypted_words_with_possible_words, new_cypher)
            elif added_word:
                if self.verbose:
                    print('Current cypher worked')
                return True, new_cypher

        if len(possible_words) == 0:
            if self.verbose:
                print('Skipping {}, because it had to possible known words.'.format(encrypted_word))
            return self.look_for_cypher(list_of_encrypted_words_with_possible_words, cypher)
        else:
            print('Current cypher failed')
            return False, {}

    def get_cypher(self, encrypted_file_path):
        got_cypher, cypher = self.look_for_cypher(self.get_possible_word_sets(self.load_clean_bag_of_words_from_file(encrypted_file_path)), {})

        if got_cypher and len(cypher.items()) < 26:
            free_letters, free_keys = [], []

            for letter in list('abcdefghijklmnopqrstuvwxyz'):
                found_letter, found_key = False, False
                for _, key in enumerate(cypher):
                    found_letter, found_key = letter == cypher[key] or found_letter, letter == key or found_key
                    if found_letter and found_key:
                        break
                if not found_letter:
                    free_letters.append(letter)
                if not found_key:
                    free_keys.append(letter)



            for key, letter in zip(free_keys, free_letters):
                cypher[key] = letter

        return got_cypher, cypher
