import random
from re import compile
from typing import Counter

common_starting_letters     = ['t', 'a', 'o', 'd', 'w']
common_ending_letters       = ['t', 's', 'e', 'd']

def build_starting_word_vocab():
    import os
    if not os.path.exists('words.txt'):
        raise Exception('save the words at weblink to file `words.txt`')
    if os.path.exists('starting_words.txt'):
        print('strating word list is already compiled')
    with open('words.txt', 'r') as f:
        words = [i.strip() for i in f.readlines()]
    start_words = [w for w in words if len(Counter(w).keys()) == 5 and (w[0] in common_starting_letters or w[-1] in common_ending_letters)]
    with open('starting_words.txt', 'w') as f:
        f.write("\n".join(start_words))

def suggest_words(step=0, disqualified_letters=set(), qualified_letters=set(), pattern=None, words=[], good_starting_words=[]):
    if step == 0:
        return good_starting_words[random.randint(0, len(good_starting_words))]
    
    if len(qualified_letters) == 0:
        filtered_qualified_letters = [w for w in good_starting_words if set(w).intersection(disqualified_letters) == set()]
        if len(filtered_qualified_letters) == 0:
            filtered_qualified_letters = [w for w in words if set(w).intersection(disqualified_letters) == set()]
        return filtered_qualified_letters[random.randint(0, len(filtered_qualified_letters))]

    legal_words = [w for w in words \
        if len(set(w).intersection(qualified_letters)) == len(qualified_letters) \
            and set(w).intersection(disqualified_letters)  == set() \
                # and len(Counter(w).keys()) == 5 \
                    and (pattern.match(w) is not None if pattern else True)\
                        ]
    return legal_words[random.randint(0 ,len(legal_words) - 1)]

def generate_vocab():
    files = ['words.txt', 'starting_words.txt']
    vocab = []
    for f in files:
        with open(f, 'r') as fi:
            vocab.append([i.strip() for i in fi.readlines()])
    return vocab[0], vocab[1]


def parse_output(suggestion, output, disqualified_letters, qualified_letters, pattern):
    for i, v in enumerate(output):
        if v == '0':
            disqualified_letters.add(suggestion[i])
        elif v == '1':
            qualified_letters.add(suggestion[i])
            pattern[i] = suggestion[i]
        elif v == '2':
            qualified_letters.add(suggestion[i])
    return disqualified_letters, qualified_letters, pattern


def play(seed):
    w, sw   = generate_vocab()
    dl      = set()
    ql      = set()
    r       = ['\w'] * 5
    random.seed(seed)
    
    step = 0

    while True:
        step += 1
        pattern = compile("".join(r))
        suggestion  = suggest_words(step, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw, pattern=pattern)
        game_output = input(f'try the word: {suggestion}\noutput: ')
        if game_output == '11111':
            print(f'WON!\nattempts: {step}')
            break
        else:
            dl, ql, r = parse_output(suggestion, game_output, dl, ql, r)

"""
`output` consists of 5 digits representing the tiles
0 - black
1 - green
2 - yellow
"""
build_starting_word_vocab()
play(123)

### sample plays
def play_one():
    w, sw   = generate_vocab()
    dl      = set()
    ql      = set()

    random.seed(417)

    ## real play step 1
    # print(suggest_words(0, words=w, good_starting_words=sw))
    # output: write
    # game output: 
    dl.update({'w', 'i', 't', 'e'})
    ql.update({'r'})

    ## real play step 2
    # print(suggest_words(1, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw))
    # output: yards
    # game output: 
    dl.update({'s', 'd', 's'})
    ql.update({'a'})
    r = compile(r'[\w]a[\w]{3}')

    ## real play step 3
    # print(suggest_words(2, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw, pattern=r))
    # output: labor
    # game output: 
    dl.update({'l', 'b'})
    ql.update({'o', 'r'})
    r = compile(r'[\w]a[\w]or')

    ## real play step 4
    print(suggest_words(3, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw, pattern=r))
    # output: favor
    # game output: 
    # WON!

def play_two():
    w, sw   = generate_vocab()
    dl      = set()
    ql      = set()

    random.seed(1129)

    ## real play step 1
    # print(suggest_words(0, words=w, good_starting_words=sw))
    # output: quilt
    # game output: 
    dl.update({'q', 'i', 't', 'u', 'l'})

    ## real play step 2
    # print(suggest_words(1, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw))
    # output: faxes
    # game output: 
    dl.update({'x', 'e', 's'})
    ql.update({'a', 'f'})
    r = compile(r'fa[\w]{3}')

    ## real play step 3
    print(suggest_words(2, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw, pattern=r))
    # output: favor
    # game output: 
    # WON!

def play_three():
    w, sw   = generate_vocab()
    dl      = set()
    ql      = set()

    random.seed(114)

    ## real play step 1
    # print(suggest_words(0, words=w, good_starting_words=sw))
    # output: dames
    # game output: 
    dl.update({'d', 'm', 's', 'e'})
    ql.update({'a'})
    r = compile(r'[\w]a[\w]{3}')

    ## real play step 2
    # print(suggest_words(1, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw, pattern=r))
    # output: caput
    # game output: 
    dl.update({'c', 'p', 'u', 't'})

    ## real play step 3
    # print(suggest_words(2, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw, pattern=r))
    # output: baron
    # game output: 
    dl.update({'b', 'n'})
    ql.update({'o', 'r'})
    r = compile(r'[\w]a[\w]o[\w]')

    ## real play step 4
    print(suggest_words(3, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw, pattern=r))
    # output: favor
    # game output: 
    # WON!

def play_four():
    w, sw   = generate_vocab()
    dl      = set()
    ql      = set()

    random.seed(1119)

    ## real play step 1
    print(suggest_words(0, words=w, good_starting_words=sw))
    # output: askew
    # game output: 
    dl.update({'a', 's', 'k', 'w', 'e'})

    ## real play step 2
    print(suggest_words(1, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw))
    # output: third
    # game output: 
    dl.update({'t', 'h', 'i', 'r', 'd'})

    ## real play step 3
    print(suggest_words(2, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw))
    # output: bloom
    # game output: 
    dl.update({'l', 'o', 'm'})
    ql.update({'b'})
    r = compile(r'b[\w]{4}')

    ## real play step 4
    print(suggest_words(3, disqualified_letters=dl, qualified_letters=ql, words=w, good_starting_words=sw, pattern=r))
    # output: bunny
    # game output: 
    # WON!

# play_one()
# play_two()
# play_three()
# play_four()
