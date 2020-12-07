import random


class Gate:
    table = [
        [0, 0, 0],
        [0, 1, 0],
        [1, 0, 0],
        [1, 1, 1]
    ]

    keys = [random.randint(1, 100000), random.randint(1, 100000)]

    def getKeys(self):
        return self.keys

    def hash(self, x, y, z):
        import hashlib
        return hashlib.md5("{}{}{}".format(x, y, z).encode()).hexdigest()

    def encrypt(self, x, key):
        return x ^ key

    def decrypt(self, x, key):
        return x ^ key

    def getGC(self):
        import hashlib
        sha = hashlib.sha256()


        arr = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ans = [[0, 0], [0, 0], [0, 0], [0, 0]]
        for j in range(2):
            for i in range(4):
                arr[i][j] = self.encrypt(self.table[i][j], self.keys[j])

        dic = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i in range(4):
            arr[i][2] = self.table[i][2]
            arr[i][2] = self.encrypt(arr[i][2], arr[i][0])
            arr[i][2] = self.encrypt(arr[i][2], arr[i][1])

            ans[i][0] = arr[i][2]
            ans[i][1] = self.hash(self.encrypt(dic[i][0], self.keys[0]), self.encrypt(
                dic[i][1], self.keys[1]), self.table[i][2])

        return ans

    def getGI(self, inputs):
        arr = inputs[:]
        for i in range(2):
            arr[i] = self.encrypt(inputs[i], self.keys[i])
        return arr

    def evaluate(self, gc, gi):
        for x in gc:
            c = self.decrypt(self.decrypt(x[0], gi[0]), gi[1])
            if self.hash(gi[0], gi[1], c) == x[1]:
                return c


gate = Gate()
print(gate.getKeys())
print(gate.getGC())
print(gate.getGI([1, 0]))

print("--------------")

print(gate.evaluate(gate.getGC(), gate.getGI([1, 0])))
