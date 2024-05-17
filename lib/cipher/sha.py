class Keccak:
    # Constants for Keccak
    b = 1600  # Keccak state size in bits
    w = 64    # Keccak state word size in bits
    l = 6     # 2^l = w
    nr = 24   # Number of rounds

    # Round constants for Keccak
    RC = [
        0x0000000000000001, 0x0000000000008082, 0x800000000000808a, 0x8000000080008000,
        0x000000000000808b, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
        0x000000000000008a, 0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
        0x000000008000808b, 0x800000000000008b, 0x8000000000008089, 0x8000000000008003,
        0x8000000000008002, 0x8000000000000080, 0x000000000000800a, 0x800000008000000a,
        0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    ]

    # Rotation offsets for the rho step
    RO = [
        [ 0, 36,  3, 41, 18],
        [ 1, 44, 10, 45,  2],
        [62,  6, 43, 15, 61],
        [28, 55, 25, 21, 56],
        [27, 20, 39,  8, 14]
    ]

    def __init__(self):
        self.state = [[0] * 5 for _ in range(5)]

    @staticmethod
    def rotate_left(x, n, w=64):
        return ((x << n) & ((1 << w) - 1)) | (x >> (w - n))

    def keccak_f(self):
        for round_idx in range(self.nr):
            # Theta step
            C = [self.state[x][0] ^ self.state[x][1] ^ self.state[x][2] ^ self.state[x][3] ^ self.state[x][4] for x in range(5)]
            D = [C[(x - 1) % 5] ^ self.rotate_left(C[(x + 1) % 5], 1) for x in range(5)]
            for x in range(5):
                for y in range(5):
                    self.state[x][y] ^= D[x]

            # Rho and Pi steps
            B = [[0] * 5 for _ in range(5)]
            for x in range(5):
                for y in range(5):
                    B[y][(2 * x + 3 * y) % 5] = self.rotate_left(self.state[x][y], self.RO[x][y])

            # Chi step
            for x in range(5):
                for y in range(5):
                    self.state[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y])

            # Iota step
            self.state[0][0] ^= self.RC[round_idx]

    @staticmethod
    def keccak_pad(message, r):
        pad_len = r - len(message) % r
        padding = b'\x01' + b'\x00' * (pad_len - 2) + b'\x80'
        return message + padding

    def keccak_sponge(self, message, r=1088, c=512, output_length=256):
        self.state = [[0] * 5 for _ in range(5)]
        padded_message = self.keccak_pad(message, r // 8)

        for i in range(0, len(padded_message), r // 8):
            block = padded_message[i:i + r // 8]
            for j in range(r // 64):
                self.state[j % 5][j // 5] ^= int.from_bytes(block[8 * j:8 * (j + 1)], 'little')
            self.keccak_f()

        z = b''
        while len(z) < output_length // 8:
            for i in range(r // 64):
                z += self.state[i % 5][i // 5].to_bytes(8, 'little')
            self.keccak_f()

        return z[:output_length // 8]

    def hash(self, input_bytes):
        return self.keccak_sponge(input_bytes)

if __name__ == "__main__":
    data = b'Example'
    keccak = Keccak()
    hashed_data = keccak.hash(data)

    print("Input bytes:", data)
    print("Hashed bytes:", hashed_data)

    import base64
    print("Hashed (base64):", base64.b64encode(hashed_data).decode())