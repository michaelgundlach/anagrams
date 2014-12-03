from collections import Counter
GLOBAL_DICTIONARY = open('words').read().split()


def anagrams_1(phrase):
    found = set()

    phrase = ''.join(phrase.split())
    match_words = match_words_for(phrase)
    match_tree = match_tree_from(match_words)
    for x in anagrams_1_recursive('', phrase, match_tree, match_tree, []):
        x = ' '.join(sorted(x))
        if x not in found:
            found.add(x)
            yield x


def anagrams_1_recursive(prefix, remaining_letters, match_root, match_node, words_so_far):
    """
    Recursively searches for and yields anagrams.  Called initially with an
    empty |prefix| and a full phrase in |remaining_letters|.

    The descriptions of the inputs below include examples for the phrase
    'computer'.

    prefix: the string prefix we've so far examined of a candidate result, e.g.
            'potrem'
    remaining_letters: iterable of remaining letters to complete the candidate,
                       e.g. 'cu'
    match_root: the root of the match tree; see match_tree_from() for details
    match_node: the current node in the match tree after walking through the
                tree to this point. E.g. we walked through 'p', 'o', 't', '\n',
                then started at the root again and walked through 'r', 'e', and
                are now at 'm'.
    words_so_far: list of words that we have found so far in walking through
                  this prefix, e.g. ['pot']

    """
    # Base case: we're out of letters to consume.  The prefix was built via a
    # successful series of walks through the match tree.  But we may not have
    # ended on a complete word.
    if not remaining_letters:
        if match_root is match_node: # we ended on a complete word
            yield words_so_far
        return
    # General case: the prefix consists of a successful series of walk(s)
    # through the match tree, but there are more letters to consume.  Recurse
    # for each letter that has a path deeper into the match tree.
    #
    # We use a set() because identical remaining letters yield equivalent
    # prefixes. In other words, if remaining_letters is 'abaac', we only need
    # to check the 'a' branch once.
    for letter in set(remaining_letters):
        if letter not in match_node:
            continue # dead end, e.g. prefix is 'soinsightf' and we tried 'z'
        next_node = match_node[letter]
        next_prefix = prefix + letter
        # TODO O() issues lurking here
        next_remaining = list(remaining_letters)
        next_remaining.remove(letter)
        # if we've spelled a word in the match tree, we must now branch into
        # two paths: the one that consumes the word and starts looking for new
        # words, and the one that assumes there's a longer word to be found.
        if '\n' in next_node:
            found_word = next_node['\n']
            for x in anagrams_1_recursive(
                    next_prefix, next_remaining, match_root, match_root,
                    words_so_far + [found_word]):
                yield x
        if True: # just to line things up
            for x in anagrams_1_recursive(
                    next_prefix, next_remaining, match_root, next_node,
                    words_so_far):
                yield x


def match_words_for(phrase):
    """
    Yields all dictionary words that can be made by rearranging a subset of
    letters in |phrase|.  E.g. 'computer' yields (among others) 'romp' and
    'cut' and 'computer'.
    """
    # Strategy: make a count of letters in phrase.  Then if a dictionary word's
    # letter count is <= the phrase's count, it's a subset.
    phrase_count = Counter(phrase)
    for word in GLOBAL_DICTIONARY:
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


import sys

anagrams = anagrams_1
for anagram in anagrams(sys.argv[1]):
    print anagram
