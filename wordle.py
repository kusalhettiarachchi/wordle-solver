import random
from re import compile
from typing import Counter, List, Pattern, Set


common_starting_letters     = ['t', 'a', 'o', 'd', 'w']
common_ending_letters       = ['t', 's', 'e', 'd']


class VocabularyExhaustedException(Exception):
    pass


def build_starting_word_vocab():
    import os
    if not os.path.exists('words.txt'):
        raise Exception('save the words at weblink to file `words.txt`')
    if os.path.exists('starting_words.txt'):
        print('strating word list is already compiled')
        return
    with open('words.txt', 'r') as f:
        words = [i.strip() for i in f.readlines()]
    start_words = [w for w in words if len(Counter(w).keys()) == 5 and (w[0] in common_starting_letters or w[-1] in common_ending_letters)]
    with open('starting_words.txt', 'w') as f:
        f.write("\n".join(start_words))


def generate_vocab():
    files = ['words.txt', 'starting_words.txt']
    vocab = []
    for f in files:
        with open(f, 'r') as fi:
            vocab.append([i.strip() for i in fi.readlines()])
    return vocab[0], vocab[1]


def pick_one(options) -> str:
    """This function maps and array of options to one of the options

    Args:
        options (list): list of words

    Returns:
        word: suggested word
    """
    if len(options) == 0:
        raise VocabularyExhaustedException()
    return options[random.randint(0, len(options) - 1)]


def suggest_words(step=0, disqualified_letters=set(), qualified_letters=set(), pattern=None, disqualified_patterns=[], words=[], good_starting_words=[]) -> str:
    """suggests a word given the updated parameters

    Args:
        step (int, optional): indicates the current step. Defaults to 0.
        disqualified_letters (set, optional): list of letters marked unacceptable. Defaults to set().
        qualified_letters (set, optional): list of letters marked acceptable. Defaults to set().
        pattern (Pattern, optional): partial regex of the correct answer. Defaults to None.
        words (list, optional): vocabulary. Defaults to [].
        good_starting_words (list, optional): good starting words. Defaults to [].

    Returns:
        word: suggested word
    """
    if step == 0:
        return pick_one(good_starting_words)
    
    if len(qualified_letters) == 0:
        filtered_qualified_words = [w for w in good_starting_words if set(w).intersection(disqualified_letters) == set()]
        if len(filtered_qualified_words) == 0:
            filtered_qualified_words = [w for w in words if set(w).intersection(disqualified_letters) == set()]
        return pick_one(filtered_qualified_words)

    legal_words = [w for w in words \
        if len(set(w).intersection(qualified_letters)) == len(qualified_letters) \
            and set(w).intersection(disqualified_letters)  == set() \
                    and (pattern.match(w) is not None if pattern else True)\
                        and sum([anti_pattern.match(w) is None for anti_pattern in disqualified_patterns]) == len(disqualified_patterns)
                        ]
    return pick_one(legal_words)


def parse_output(suggestion: str, output: str, disqualified_letters: Set, qualified_letters: Set, pattern: Pattern, disqualified_patterns: List[Pattern]):
    for i, v in enumerate(output):
        anti_pattern = [r'\w'] * 5
        if v == '0' and suggestion[i] not in qualified_letters:
            disqualified_letters.add(suggestion[i])
        elif v == '1':
            qualified_letters.add(suggestion[i])
            pattern[i] = suggestion[i]
        elif v == '2':
            qualified_letters.add(suggestion[i])
            # we have atleast one misplaced letter
            anti_pattern[i] = suggestion[i]
            disqualified_patterns.append(compile("".join(anti_pattern)))
    return disqualified_letters, qualified_letters, pattern, disqualified_patterns


def play(seed):
    w, sw   = generate_vocab()
    dl      = set()
    ql      = set()
    r       = ['\w'] * 5
    dr      = list()
    random.seed(seed)
    
    step = 0

    while True:
        step += 1
        pattern = compile("".join(r))
        try:
            suggestion  = suggest_words(step, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw, pattern=pattern, disqualified_patterns=dr)
        except VocabularyExhaustedException:
            print(f'vocabulary exhausted\ntry regex: {str(pattern)}\nqualified letters: {ql}\ndisqualified letters: {dl}\ndisqualified patterns: {dr}')
            break
        game_output = input(f'try the word: {suggestion}\noutput: ')
        if game_output == '11111':
            print(f'WON!\nattempts: {step}')
            break
        else:
            dl, ql, r, dr = parse_output(suggestion, game_output, dl, ql, r, dr)

"""
`output` consists of 5 digits representing the tiles
0 - black
1 - green
2 - yellow
"""
build_starting_word_vocab()
play(534)