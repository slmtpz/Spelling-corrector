# Finds which steps have been followed (ins, sub, del, tra) and
# which characters are manipulated in Damerau-Levenshtein procedure.
# After that, calculates confusion matrices for all operations.
class DL_Handler:
    def __init__(self):
        self.ALPHABET_SIZE = 29  # and apostrophe ', underscore _, start ' '
        # initialization and smoothening
        self._del_mx, self._ins_mx, self._sub_mx, self._tra_mx = ([[1 for i in range(self.ALPHABET_SIZE)] for j in range(self.ALPHABET_SIZE)],) * 4

    # a -> 0 .. z -> 25
    def lttr2nmbr(self, c):
        if c == "'":
            return self.ALPHABET_SIZE - 3
        elif c == '_':
            return self.ALPHABET_SIZE - 2
        elif c == ' ':
            return self.ALPHABET_SIZE - 1
        return ord(c) - 97

    def get_operations_using_DL(self, a, b):
        da = [0]*self.ALPHABET_SIZE
        la = len(a)
        lb = len(b)

        d = {}
        ops = {}
        for i in range(-1, la+1):
            for j in range(-1, lb+1):
                d[(i, j)] = 0
        maxdist = la+lb
        d[(-1, -1)] = maxdist
        for i in range(la+1):
            d[(i, -1)] = maxdist
            d[(i, 0)] = i
            ops[(i, 0)] = ('del', ' ', a[i-1])
        for j in range(lb+1):
            d[(-1, j)] = maxdist
            d[(0, j)] = j
            ops[(0, j)] = ('ins', ' ', b[j-1])

        for i in range(1, la+1):
            db = 0
            for j in range(1, lb+1):
                k = da[self.lttr2nmbr(b[j-1])]
                l = db
                if a[i-1] == b[j-1]:
                    cost = 0
                    db = j
                else:
                    cost = 1
                d[(i, j)] = min(d[(i-1, j-1)] + cost,  # substitution
                                d[(i, j - 1)] + 1,  # insertion
                                d[(i - 1, j)] + 1,  # deletion
                                d[(k - 1, l - 1)] + (i - k - 1) + 1 + (j - l - 1)  # transposition
                                )
                if d[(i, j)] == d[(i-1, j-1)] + cost:
                    ops[(i, j)] = ('sub', b[j-1], a[i-1])
                elif d[(i, j)] == d[(i, j - 1)] + 1:
                    ops[(i, j)] = ('ins', b[j-2], b[j-1])
                elif d[(i, j)] == d[(i - 1, j)] + 1:
                    ops[(i, j)] = ('del', a[i-2], a[i-1])
                elif d[(i, j)] == d[(k - 1, l - 1)] + (i - k - 1) + 1 + (j - l - 1):
                    ops[(i, j)] = ('tra', a[i-2], a[i-1])

            da[self.lttr2nmbr(a[i-1])] = i
        # distance is d[(la, lb)] but it is unimportant
        return ops

    def update_confusion_matrices(self, a, b, weigth):
        ops = self.get_operations_using_DL(a, b)

        # backtrace
        i = len(a)
        j = len(b)
        while i != 0 or j != 0:
            op = ops[(i, j)]
            if op[0] == 'sub':
                i -= 1
                j -= 1
                if op[1] != op[2]:
                    print('substitution: ' + op[2] + ' typed as ' + op[1])
                    self._sub_mx[self.lttr2nmbr(op[1])][self.lttr2nmbr(op[2])] += weigth
            elif op[0] == 'ins':
                j -= 1
                print('insertion: ' + op[1] + ' typed as ' + op[1] + op[2])
                self._ins_mx[self.lttr2nmbr(op[1])][self.lttr2nmbr(op[2])] += weigth
            elif op[0] == 'del':
                i -= 1
                print('deletion: ' + op[1] + op[2] + ' typed as ' + op[1])
                self._del_mx[self.lttr2nmbr(op[1])][self.lttr2nmbr(op[2])] += weigth
            elif op[0] == 'tra':
                i -= 2
                j -= 2
                print('transposition: ' + op[1] + op[2] + ' typed as ' + op[2] + op[1])
                self._tra_mx[self.lttr2nmbr(op[1])][self.lttr2nmbr(op[2])] += weigth

    def get_confusion_matrices(self):
        return self._sub_mx, self._ins_mx, self._del_mx, self._tra_mx
