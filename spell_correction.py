import re
from collections import Counter
from error_learner import Learner
import sys


text = open('corpus.txt').read()
WORDS = Counter(re.findall(r'\w+', text.lower()))


def prior_probability(word):
    return WORDS[word] / sum(WORDS.values())


def likelihood(op, x, y):
    return learner.get_likelihood_probability(op, x, y, text)


# Generates candidates of edit distance 1 and calculates probabilities according to both
# noisy channel model and the model only language model is used.
def evaluate_candidates(word):
    candidate_probs = {}
    candidate_probs_only_language_model = {}
    letters = "abcdefghijklmnopqrstuvwxyz"
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    for L, R in splits:
        if R:
            # insertion
            candidate = L + R[1:]
            if candidate in WORDS:
                candidate_probs_only_language_model[candidate] = prior_probability(candidate)
                if L:
                    candidate_probs[candidate] = likelihood('ins', L[-1], R[0]) * prior_probability(candidate)
                else:
                    candidate_probs[candidate] = likelihood('ins', ' ', R[0]) * prior_probability(candidate)
            # substitution
            for c in letters:
                candidate = L + c + R[1:]
                if candidate in WORDS:
                    candidate_probs[candidate] = likelihood('sub', R[0], c) * prior_probability(candidate)
                    candidate_probs_only_language_model[candidate] = prior_probability(candidate)

            # transposition
            if len(R) > 1:
                candidate = L + R[1] + R[0] + R[2:]
                if candidate in WORDS:
                    candidate_probs[candidate] = likelihood('tra', R[0], R[1]) * prior_probability(candidate)
                    candidate_probs_only_language_model[candidate] = prior_probability(candidate)

        # deletion
        for c in letters:
            candidate = L + c + R
            if candidate in WORDS:
                candidate_probs_only_language_model[candidate] = prior_probability(candidate)
                if L:
                    candidate_probs[candidate] = likelihood('del', L[-1], c) * prior_probability(candidate)
                else:
                    candidate_probs[candidate] = likelihood('del', ' ', c) * prior_probability(candidate)

    return candidate_probs, candidate_probs_only_language_model


# get the maximum probability candidate among candidates
def get_prediction(candidate_probs):
    if candidate_probs:
        return max(candidate_probs, key=candidate_probs.get)
    return ''


# learn the error model
learner = Learner()
learner.learn()

comparable = False
if len(sys.argv) == 3:
    comparable = True

mispelled_words = open(sys.argv[1]).read().splitlines()
correct_words = []
if comparable:
    correct_words = open(sys.argv[2]).read().splitlines()
v1 = open('noisy_channel_model_corrections.txt', 'w')
v2 = open('only_language_model_corrections.txt', 'w')

count = len(mispelled_words)
count_correct_prediction = 0
count_correct_prediction_only_language_model = 0
for i in range(count):
    candidate_probs, candidate_probs_only_language_model = evaluate_candidates(mispelled_words[i])
    prediction = get_prediction(candidate_probs)
    v1.write(prediction + '\n')
    prediction_only_language_model = get_prediction(candidate_probs_only_language_model)
    v2.write(prediction_only_language_model + '\n')
    if comparable:
        if prediction == correct_words[i]: count_correct_prediction += 1
        if prediction_only_language_model == correct_words[i]: count_correct_prediction_only_language_model += 1

if comparable:
    print('%' + str(count_correct_prediction / count * 100) + ' accuracy with noisy channel model.')
    print('%' + str(count_correct_prediction_only_language_model / count * 100) + ' accuracy with only language model.')
