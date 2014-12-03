from collections import Counter
GLOBAL_DICTIONARY = open('words').read().split()


def match_words_for(phrase, source_dictionary=GLOBAL_DICTIONARY):
    """
    Given a |source_dictionary| list of words, yields all words that
    can be made by rearranging a subset of letters in |phrase|.  E.g.
    'computer' yields (among others) 'romp' and 'cut' and 'computer' if
    those words are in |source_dictionary|.

    Optional |source_dictionary| defaults to the list of words in the 'words'
    file on disk.
    """
    # Strategy: make a count of letters in phrase.  Then if a dictionary word's
    # letter count is <= the phrase's count, it's a subset.
    phrase_count = Counter(phrase)
    for word in source_dictionary:
        word_count = Counter(word)
        if all(word_count[L] <= phrase_count[L] for L in word_count):
            yield word


def match_tree_from(words):
    """
    Returns a match tree for the given collection of |words|.

    A match tree lets you find out if a string is a prefix of any of |words| in
    constant time per letter of the prefix.  Here's a match tree for ['a',
    'an', 'the', 'them'].
    ROOT: {'a', 't'}
    'a': {'\n', 'n'} #'\n' is a leaf meaning "end of word"
    'n': {'\n'}
    't': {'h'}
    'h': {'e'}
    'e': {'\n', 'm'}
    'm': {'\n'}
    """
    result = {}
    def add(word):
        """Update |result| to contain |word|."""
        node = result
        for letter in word:
            node = node.setdefault(letter, {})
        node['\n'] = word
    for word in words:
        add(word)
    return result


