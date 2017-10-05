class CypherFinder:
    def __init__(self, corpus_path, encrypted_file_path):
        self.corpus_path, self.encrypted_file_path = corpus_path, encrypted_file_path

    def get_cypher(self):
        cypher, alphabet = {}, 'abcdefghijklmnopqrstuvwxyz'
        for letter in alphabet.upper() + alphabet:
            cypher[letter] = '?'

        with open(self.corpus_path) as corpus_reader:
            corpus_data = corpus_reader.read()

        corpus_data

        with open(self.encrypted_file_path) as encrypted_reader:
            for encrypted_line in encrypted_reader.read():
                numeric_line = replace_letters_with_numbers(encrypted_line)




        print(self.corpus_path)
        print(self.encrypted_file_path)
        return cypher