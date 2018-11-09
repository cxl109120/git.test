

import nltk
import re
import sys
from nltk.corpus import wordnet as wn
#from nltk.corpus import stopwords
#stop_words = set(stopwords.words('english'))

stop_words = {'a', 'an', 'the', 'is', 'was', 'are', 'this', 'that',
              'be', 'from', 'for', 'in', 'of', 'on', 'to'}

def overlapping(word, sent1, sent2, delete_stopwords = True):
    sent1 = re.sub(r'[^\w\s\']', ' ', sent1).lower()
    sent2 = re.sub(r'[^\w\s\']', ' ', sent2).lower()
    sent1_tokens = set(nltk.word_tokenize(sent1))
    sent2_tokens = set(nltk.word_tokenize(sent2))

    if delete_stopwords:
        sent1_tokens = [w for w in sent1_tokens if w not in stop_words]
        sent2_tokens = [w for w in sent2_tokens if w not in stop_words]

    overlap = []
    for token1 in sent1_tokens:
        for token2 in sent2_tokens:
            if token1 == token2 and not token1 == word:
                overlap.append(token1)
    return overlap


def lesk(word, sentence):
    word = word.lower()
    word_synsets = wn.synsets(word, pos='n')

    best_sense = None
    max_overlap = 0

    for i in range(len(word_synsets)):
        word_sense = word_synsets[i]

        word_signature = word_sense.definition()
        for word_exp in word_sense.examples():
            word_signature += (' ' + word_exp)

        overlap = overlapping(word, word_signature, sentence)
        count = len(overlap)

        print(f'word sense ({i+1}): {word_sense} | overlap: {len(overlap)} {overlap}')
        if count > max_overlap:
            max_overlap = count
            best_sense = word_sense
    return best_sense


def main():

    if not len(sys.argv) == 3:
        print('Error in arguments. Usage: python LESK.py \'word\' \'sentence\'')
    else:
        word = sys.argv[1]
        sentence = sys.argv[2]

        best_sense = lesk(word, sentence)
        if not best_sense:
            print('There is no best sense by LESK algorithm.')
        else:
            print(f'Best sense: {best_sense} | definition: {best_sense.definition()}')


if __name__ == '__main__':
    main()