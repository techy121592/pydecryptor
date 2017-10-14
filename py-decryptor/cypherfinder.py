class CypherFinder:
    def __init__(self, corpus_path):
        self.bag_of_words = self.load_clean_bag_of_words_from_file(corpus_path)

    def load_clean_bag_of_words_from_file(self, file_path):
        with open(file_path) as file:
            #return self.remove_possible_proper_nouns(list(map(self.remove_non_alpha, set(file.read().split()))))
            return list(map(self.remove_non_alpha, set(file.read().split())))

    def remove_possible_proper_nouns(self, bag_of_words):
        bag_of_words_minus_proper_nouns = []
        for word in bag_of_words:
            if not list(word)[0]:
                bag_of_words_minus_proper_nouns.append(word)
        return bag_of_words_minus_proper_nouns

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
        return word_sets

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
                print('Added appropriate keys for {} = {}'.format(encrypted_word, possible_word))
                found_cypher, new_cypher = self.look_for_cypher(list_of_encrypted_words_with_possible_words, new_cypher)
                if found_cypher:
                    return True, new_cypher
            elif added_word:
                print('Current cypher worked')
                return True, new_cypher
        print('Current cypher failed')
        return False, {}

    def get_cypher(self, encrypted_file_path):
        return self.look_for_cypher(self.get_possible_word_sets(self.load_clean_bag_of_words_from_file(encrypted_file_path)), {})