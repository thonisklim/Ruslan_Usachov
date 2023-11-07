class VigenereCipher(object):
    def __init__(self, key, alphabet):
        self.alphabet = alphabet
        self.key = key

    def encode(self, text):
        keyed = self.key * (len(text) // len(self.key)) + self.key[:len(text) % len(self.key)]
        return ''.join([self.alphabet[(self.alphabet.find(text[i]) + self.alphabet.find(keyed[i])) % len(self.alphabet)] if text[i] in self.alphabet else text[i] for i in range(len(text))])

    def decode(self, text):
        keyed = self.key * (len(text) // len(self.key)) + self.key[:len(text) % len(self.key)]
        return ''.join([self.alphabet[(self.alphabet.find(text[i]) - self.alphabet.find(keyed[i])) % len(self.alphabet)] if text[i] in self.alphabet else text[i] for i in range(len(text))])

print(-1%5)