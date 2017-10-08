import random
from decrypter import Decrypter

class CypherFinder:
    def __init__(self, corpus_path, encrypted_file_path):
        self.corpus_path, self.encrypted_file_path, self.alphabet, self.previous_cyphers, self.current_cypher = corpus_path, encrypted_file_path, list('abcdefghijklmnopqrstuvwxyz'), [], {}
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

    def get_next_cypher(self, words_matched):
        self.previous_cyphers.append(self.current_cypher.copy())

        while self.current_cypher in self.previous_cyphers:
            letter1, letter2 = random.choice(self.alphabet), random.choice(self.alphabet)
            while letter1 == letter2:
                letter2 = random.choice(self.alphabet)
            self.swap(letter1, letter2)

    def get_words_from_file_data(self, file_data):
        return list(map(self.remove_non_alpha, file_data.split()))

    def check_if_cypher_works(self):
        decrypter, words_matched, letters_matched = Decrypter(self.current_cypher), 0, 0
        for encrypted_word in self.bag_of_encrypted_words:
            decrypted_word = decrypter.decrypt(self.remove_non_alpha(encrypted_word))
            if not decrypted_word in self.bag_of_words:
                return False, words_matched
            else:
                words_matched = words_matched + 1
        return True, words_matched

    def remove_duplicate_words(self, bag_of_words):
        clean_bag_of_words, dirty_bag_of_words, words_of_same_length, words_removed, total_words, current_length = [], bag_of_words.copy(), [], 0, len(bag_of_words), 0

        while len(dirty_bag_of_words) > 0:
            temp_bag_of_words, number_of_duplicates = [], 0
            print('Removing words from bag of words')
            for word in dirty_bag_of_words:
                lower_word = word.lower()
                if current_length != len(lower_word):
                    words_of_same_length = []
                    current_length = len(lower_word)
                    print('Moving onto words with the length of {}'.format(current_length))
                if lower_word not in words_of_same_length:
                    temp_bag_of_words.append(lower_word)
                    words_of_same_length.append(lower_word)
                else:
                    words_removed, number_of_duplicates, clean_count = words_removed + 1, number_of_duplicates + 1, len(temp_bag_of_words) + len(clean_bag_of_words)
                    if words_removed % 250000 == 0:
                        print('Removed {} and added {} words out of {} so far. {}% complete'.format(words_removed, clean_count, total_words, ((clean_count + words_removed) / total_words) * 100))
                    if len(temp_bag_of_words) >= 5000:
                        break
            print('Copying data over')
            dirty_bag_of_words = dirty_bag_of_words[len(temp_bag_of_words) + number_of_duplicates:]
            clean_bag_of_words.extend(temp_bag_of_words)
            print('Done copying')
        print('The bag of words is now {}% of it\'s original size'.format((len(clean_bag_of_words) / total_words) * 100))
        return clean_bag_of_words

    def remove_impossible_words_by_length(self):
        clean_bag_of_words, lengths = [], []

        for word in self.bag_of_encrypted_words:
            if len(word) not in lengths:
                lengths.append(len(word))

        for word in self.bag_of_words:
            if len(word) in lengths:
                clean_bag_of_words.append(word)

        print('Removed {} words by length'.format(len(self.bag_of_words) - len(clean_bag_of_words)))
        self.bag_of_words = clean_bag_of_words

    def get_cypher(self):
        print('Loading corpus')
        with open(self.corpus_path) as corpus_reader:
            self.bag_of_words = self.get_words_from_file_data(corpus_reader.read())

        print('Loading encoded')
        with open(self.encrypted_file_path) as encrypted_reader:
            self.bag_of_encrypted_words = self.get_words_from_file_data(encrypted_reader.read())

        print('Sorting bag of words')
        self.bag_of_words.sort(key=len)

        print('Sorting encrypted bag of words')
        self.bag_of_encrypted_words.sort(key=len)

        print('Removing impossible words by length')
        self.remove_impossible_words_by_length()

        print('Cleaning bags of words')
        self.bag_of_words, self.bag_of_encrypted_words = self.remove_duplicate_words(self.bag_of_words), self.remove_duplicate_words(self.bag_of_encrypted_words)

        print('Searching for cypher')
        for attempts in range(26*25*24*23*22*21*20*19*18*17*16*15*14*13*12*11*10*9*8*7*6*5*4*3*2):
            cypher_works, words_matched = self.check_if_cypher_works()
            if not cypher_works:
                print('Attempt {} didn\'t work'.format(attempts))
                self.get_next_cypher(words_matched)
            else:
                print('Found cypher')
                break

        return self.current_cypher