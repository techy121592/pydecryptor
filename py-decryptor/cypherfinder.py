class CypherFinder:
    def __init__(self, corpus_path, encrypted_file_path):
        self.corpus_path, self.encrypted_file_path = corpus_path, encrypted_file_path

    def trim_sentence(self, sentence):
        return sentence.strip()

    def break_up_paragraph_into_clean_sentences(self, paragraph):
        clean_paragraph = paragraph.replace('\n', ' ').replace('\r', ' ')
        for word in paragraph.split():
            clean_paragraph = clean_paragraph + ' ' + word

        clean_paragraph = clean_paragraph.replace('. ', '.. ').replace('?', '?. ').replace('!', '!. ').replace('"', '". ').strip('."').strip('..').strip(' .')
        return list(map(self.trim_sentence, clean_paragraph.split('. ')))

    def break_up_paragraphs_into_sentences(self, paragraphs):
        return list(map(self.break_up_paragraph_into_clean_sentences, paragraphs))

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

    def compare_numeric_lines(self, numeric_encrypted_line, numeric_corpus_line):
        return numeric_encrypted_line == numeric_corpus_line

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
        with open(self.encrypted_file_path) as encrypted_reader:
            for encrypted_line in encrypted_reader:
                encrypted_line = encrypted_line.strip()
                if encrypted_line == '':
                    continue

                numeric_encrypted_line = self.replace_letters_with_numbers(encrypted_line)
                found_match = False
                for corpus_paragraph in corpus_broken_down:
                    for corpus_sentence in corpus_paragraph:
                        if len(corpus_sentence.strip()) <= 1:
                            continue

                        numeric_corpus_line = self.replace_letters_with_numbers(corpus_sentence)
                        print(encrypted_line)
                        print(corpus_sentence)
                        print(numeric_encrypted_line)
                        print(numeric_corpus_line)
                        if self.compare_numeric_lines(numeric_encrypted_line, numeric_corpus_line):
                            encrypted_corpus_pair_list.append((encrypted_line, corpus_sentence))
                            found_match = True
                        if found_match:
                            break
                    if found_match:
                        break
                if not found_match:
                    print('Couldn\'t match sentence... :(')

        if len(encrypted_corpus_pair_list) > 0:
            return self.generate_cypher_from_encrypted_corpus_pairs(encrypted_corpus_pair_list)
        else:
            print('Did\'t find any matches!!!!')