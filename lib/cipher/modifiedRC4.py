class RC4:
    # Modified in KSA generation with playfair and vigenere cipher modification 

    def __init__(self, key) -> None:
        self.key = key

    def KSA(self) -> list:
        key = [ord(c) for c in self.key]
        S = list(range(256))
        j = 0

        # vigenere modification
        allAscii = [chr(i) for i in range(256)]
        for c in key:
            if chr(c) in allAscii:
                allAscii.remove(chr(c))
        key += [ord(c) for c in allAscii]

        # creating 16 by 16 matrix of ASCII key
        matrix = []
        for i in range(0, 256, 16):
            matrix.append(key[i:i+16])

        for i in range(256):
            # swapping with playfair modification
            # j = (j + S[i] + key[i % len(key)]) % 256

            j = (j + S[i] + key[matrix[i//16][i%16]]) % 256
            S[i], S[j] = S[j], S[i]

        return S
    
    def PRGA(self, S, plaintext) -> list:
        i = 0
        j = 0
        key = []
        shift = 0
        for c in plaintext:
            # swapping with vigenere modification, shifting with total sum ascii of key
            i = (i + 1) % 256
            j = (j + S[i] + shift) % 256
            S[i], S[j] = S[j], S[i]
            key.append(S[(S[i] + S[j]) % 256])
            shift += key[-1]
        return key
    
    def encrypt(self, plaintext: bytes) -> bytes:
        S = self.KSA()
        key = self.PRGA(S, plaintext)
        return bytes([p ^ k for p, k in zip(plaintext, key)])
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        S = self.KSA()
        key = self.PRGA(S, ciphertext)
        return bytes([c ^ k for c, k in zip(ciphertext, key)])
    
# cp = rc4("Super secure and long key")
# string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec odio et nunc fermentum, fermentum. "

# print(string)
# string = string.encode()
# print(string)
# ciphertext = cp.encrypt(string)
# print(ciphertext)

# # turning into string 256 bit ASCII
# ciphertext = ''.join([chr(i) for i in ciphertext])
# print(ciphertext, len(ciphertext))

# # turning back into bytes
# ciphertext = bytes([ord(i) for i in ciphertext])
# print(ciphertext)

# plaintext = cp.decrypt(ciphertext)
# print(plaintext)
# print(plaintext.decode())