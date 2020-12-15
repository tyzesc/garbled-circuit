import random


class Gate:
    def __init__(self, tb):
        # 不是二的次方倍
        if (len(tb) & (len(tb)-1) != 0) or len(tb) == 0:
            raise Exception('invalid table.')
        # table 裏頭不等長
        if len(list(set([len(a) for a in tb]))) > 1 or len(tb[0]) == 0:
            raise Exception('invalid table.')

        self.table = tb
        self.keys = []
        for i in range(len(tb[0])*2):
            self.keys.append(random.randint(1, 100000))

    def getKeys(self):
        return self.keys

    def hash(self, s):
        import hashlib
        return hashlib.md5(s.encode()).hexdigest()

    def encrypt(self, x, key):
        return x ^ key

    def decrypt(self, x, key):
        return x ^ key

    def getGC(self):
        import hashlib
        sha = hashlib.sha256()

        arr = []
        for i in range(len(self.table)):
            a = []
            for j in range(len(self.table[i])):
                if self.table[i][j] == 0:
                    a.append(self.encrypt(self.table[i][j], self.keys[j]))
                else:
                    a.append(self.encrypt(self.table[i][j], self.keys[len(self.table[i]) + j]))
            arr.append(a)

        gc = []
        for i in range(len(self.table)):
            c = self.table[i][-1]
            a = [c, ""]
            for x in arr[i][:-1]:
                a[0] = self.encrypt(a[0], x)
            for x in arr[i][:-1]:
                a[1] = a[1] + str(x)
            a[1] += str(c)  # 最後要放 c
            a[1] = self.hash(a[1])
            gc.append(a)

        return gc

    def getGI(self, inputs):
        arr = inputs[:]
        for i in range(len(arr)):
            if arr[i] == 0:
                arr[i] = self.encrypt(inputs[i], self.keys[i])
            else:
                arr[i] = self.encrypt(inputs[i], self.keys[len(self.table[i]) + i])

        return arr

    def evaluate(self, gc, gi):
        for x in gc:
            c = x[0]
            s = ""
            for elem in gi:
                c = self.decrypt(c, elem)
                s = s + str(elem)
            s += str(c)
            if self.hash(s) == x[1]:
                return c


if __name__ == '__main__':
    table = [
        [0, 0, 0],
        [0, 1, 0],
        [1, 0, 0],
        [1, 1, 1]
    ]

    sender = Gate(table)
    gc = sender.getGC()
    cases = [[1, 0], [0, 0], [0, 1], [1, 1]]
    print("keys:", sender.getKeys())
    print("gc:", gc)
    for testcase in cases:
        gi = sender.getGI(testcase)
        ans = sender.evaluate(gc, gi)
        print("gi:", gi, "testcase:", testcase, "ans:", ans)
