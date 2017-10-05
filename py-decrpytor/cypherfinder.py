class CypherFinder:
    def __init__(self, corpus_path, encrypted_file_path):
        self.corpus_path, self.encrypted_file_path = corpus_path, encrypted_file_path

    def get_cypher(self):
        cypher, alphabet = {}, 'abcdefghijklmnopqrstuvwxyz'
        for letter in alphabet.upper() + alphabet:
            cypher[letter] = '?'
        print(self.corpus_path)
        print(self.encrypted_file_path)
        return cypher