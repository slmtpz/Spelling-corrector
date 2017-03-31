import re
from damerau_levenshtein import DL_Handler


# learns the errors and produces likelihood probabilities for noisy channel model
# using confusion matrices.
class Learner:
    def __init__(self):
        self.dl_handler = DL_Handler()

    def is_numeric(self, list, index):
        try:
            int(list[index])
            return True
        except:
            return False

    def learn(self):
        print('Learning Error Model..')
        with open('spell-errors.txt') as f:
            for line in f:
                words_and_weights = re.findall(r'\b[^\W_]+[\'|_]?[^\W_]*\b', line.lower())
                correct_word = words_and_weights[0]
                i = 1
                while i < len(words_and_weights):
                    index = i
                    if self.is_numeric(words_and_weights, i+1):
                        weigth = int(i+1)
                        i += 1
                    else:
                        weigth = 1

                    self.dl_handler.update_confusion_matrices(correct_word, words_and_weights[index], weigth)
                    i += 1


    def get_likelihood_probability(self, op, x, y, text):
        sub_mx, ins_mx, del_mx, tra_mx = self.dl_handler.get_confusion_matrices()
        a = self.dl_handler.ALPHABET_SIZE
        lttr2nmbr = self.dl_handler.lttr2nmbr
        if op == 'ins':
            return ins_mx[lttr2nmbr(x)][lttr2nmbr(y)] / (text.count(x) + a)
        elif op == 'del':
            return del_mx[lttr2nmbr(x)][lttr2nmbr(y)] / (text.count(x+y) + a)
        elif op == 'sub':
            return sub_mx[lttr2nmbr(x)][lttr2nmbr(y)] / (text.count(y) + a)
        elif op == 'tra':
            return tra_mx[lttr2nmbr(x)][lttr2nmbr(y)] / (text.count(x+y) + a)
