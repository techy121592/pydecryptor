class Decrypter:
    cypher = {}
    def __init__(self, cypher):
        self.cypher = cypher

    def swap_letters(self, letter):
        try:
            if letter.isupper():
                return self.cypher[letter.lower()].upper()
            else:
                return self.cypher[letter]
        except:
            return letter

    def decrypt(self, line):
        return ''.join(list(map(self.swap_letters, list(line))))
