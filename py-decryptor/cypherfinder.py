class CypherFinder:
    def __init__(self, corpus_path, encrypted_file_path):
        self.corpus_path, self.encrypted_file_path = corpus_path, encrypted_file_path

    def trim_sentence(self, sentence):
        return sentence.strip()

    def break_up_paragraph_into_sentences(self, paragraph):
        return list(map(self.trim_sentence, paragraph.replace('.', '.. ').replace('?', '?. ').replace('!', '!. ').split('. ')))

    def break_up_paragraphs_into_sentences(self, paragraphs):
        return list(map(self.break_up_paragraph_into_sentences, paragraphs))

    def break_up_body_into_paragraphs(self, body):
        return body.split('\n\n')

    def replace_letters_with_numbers(self, line):
        key = {}
        next_number = 0
        list_of_lists_of_numbers = []
        list_of_numbers = []
        for letter in list(line):
            if letter.isalpha():
                letter_value: int
                try:
                    letter_value = key[letter]
                except:
                    key[letter], letter_value, next_number = next_number, next_number, next_number + 1
                finally:
                    list_of_numbers.append(letter_value)
            elif len(list_of_numbers) > 0:
                list_of_lists_of_numbers.append(list_of_numbers)
                list_of_numbers = []
        return list_of_lists_of_numbers

    def compare_lines(self, encrypted_line, corpus_line):
        output = self.replace_letters_with_numbers(encrypted_line) == self.replace_letters_with_numbers(corpus_line)
        return output

    def generate_cypher_from_encrypted_corpus_pairs(self, encrypted_corpus_pair_list):
        cypher = {}
        for encrypted_line, corpus_line in encrypted_corpus_pair_list:
            for encrypted_letter, corpus_letter in zip(encrypted_line, corpus_line):
                cypher[encrypted_letter] = corpus_letter
        return cypher

    def get_cypher(self):
        print('Getting cypher')
        with open(self.corpus_path) as corpus_reader:
            corpus_data = corpus_reader.read()

        corpus_broken_down = self.break_up_paragraphs_into_sentences(self.break_up_body_into_paragraphs(corpus_data))

        encrypted_corpus_pair_list = []
        threads = []
        with open(self.encrypted_file_path) as encrypted_reader:
            for encrypted_line in encrypted_reader:
                for corpus_paragraph in corpus_broken_down:
                    for corpus_sentence in corpus_paragraph:
                        if self.compare_lines(encrypted_line, corpus_sentence):
                            encrypted_corpus_pair_list.append((encrypted_line, corpus_sentence))

        return self.generate_cypher_from_encrypted_corpus_pairs(encrypted_corpus_pair_list)