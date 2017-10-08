import random
from decrypter import Decrypter

class CypherFinder:
    def __init__(self, corpus_path, encrypted_file_path):
        self.corpus_path, self.encrypted_file_path = corpus_path, encrypted_file_path
        self.alphabet = list('abcdefghijklmnopqrstuvwxyz')
        self.previous_cyphers = []
        self.current_cypher = {}
        for letter in self.alphabet:
            self.current_cypher[letter] = letter

    def remove_non_alpha(self, input):
        output = ''
        for letter in list(input):
            if letter.isalpha():
                output = output + letter
            else:
                output = output + ' '
        return output

    def swap(self, letter1, letter2):
        self.current_cypher[letter1], self.current_cypher[letter2] = self.current_cypher[letter2], self.current_cypher[letter1]

    def get_next_cypher(self):
        self.previous_cyphers.append(self.current_cypher.copy())

        while self.current_cypher in self.previous_cyphers:
            self.swap(random.choice(self.alphabet), random.choice(self.alphabet))

    def get_words_from_file_data(self, file_data):
        return list(map(self.remove_non_alpha, file_data.split()))

    def check_if_cypher_works(self):
        decrypter = Decrypter(self.current_cypher)
        for encrypted_word in self.bag_of_encrypted_words:
            if not decrypter.decrypt(self.remove_non_alpha(encrypted_word)) in self.bag_of_words:
                return False
        return True

    def remove_duplicate_words(self, bag_of_words):
        clean_bag_of_words = []
        words_removed = 0
        for word in bag_of_words:
            if word.lower() not in clean_bag_of_words:
                clean_bag_of_words.append(word.lower())
            else:
                words_removed = words_removed + 1
                if words_removed % 100000 == 0:
                    print('Removed {} and added {} words so far'.format(words_removed, len(clean_bag_of_words)))
        return clean_bag_of_words

    def get_cypher(self):
        print('Loading corpus')
        with open(self.corpus_path) as corpus_reader:
            self.bag_of_words = self.get_words_from_file_data(corpus_reader.read())

        print('Loading encoded')
        with open(self.encrypted_file_path) as encrypted_reader:
            self.bag_of_encrypted_words = self.get_words_from_file_data(encrypted_reader.read())

        print('Cleaning bag of words')
        self.bag_of_words, self.bag_of_encrypted_words = self.remove_duplicate_words(self.bag_of_words), self.remove_duplicate_words(self.bag_of_encrypted_words)

        print('Searching for cypher')
        for attempts in range(26*25*24*23*22*21*20*19*18*17*16*15*14*13*12*11*10*9*8*7*6*5*4*3*2):
            if not self.check_if_cypher_works():
                if attempts % 25000 == 0:
                    print('Attempt {} didn\'t work'.format(attempts))
                self.get_next_cypher()
            else:
                print('Found cypher')
                break

        return self.current_cypher