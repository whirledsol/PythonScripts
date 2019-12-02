import random
import nltk


def fence(lst, numrails):
    fence = [[None] * len(lst) for n in range(numrails)]
    rails = list(range(numrails - 1)) + list(range(numrails - 1, 0, -1))
    for n, x in enumerate(lst):
        fence[rails[n % len(rails)]][n] = x

    if 0: # debug
        for rail in fence:
            print(''.join('.' if c is None else str(c) for c in rail))

    return [c for rail in fence for c in rail if c is not None]

def encode(text, n):
    return ''.join(fence(text, n))

def decode(text, n):
    rng = range(len(text))
    pos = fence(rng, n)
    return ''.join(text[pos.index(n)] for n in rng)

def bruteforce(text):
    decodes = [decode(text,n) for n in range(2,len(text))]
    decodes = [d for d in decodes if not d.startswith(' ') and not d.endswith(' ') and '  ' not in d]
    return decodes

def anagramsLegacy(encrypted,knowns):
    encrypted = list(encrypted)
    words = encrypted.count(' ') + 1

    wordsleft = words - len(knowns)
    print(knowns)
    print('there are {} words left to figure out'.format(wordsleft))

    knownletters = list(''.join(knowns))
    for letter in list(set(knownletters)):
        count = knownletters.count(letter)
        countEncrypted = encrypted.count(letter)

        if countEncrypted < count:
            print('sorry. encryption doesn\'t have that many of the letter {}'.format(letter))
            return
        for i in range(count):
            index = encrypted.index(letter)
            del encrypted[index]
    
    encrypted = ''.join(encrypted).replace(' ','')
    print('what\'s left is {}'.format(encrypted))
    for j in range(10):
        print(''.join([str(w) for w in random.sample(encrypted, len(encrypted))]))

def anagrams(encrypted,knowns = []):
    count_words = encrypted.count(' ') + 1

    encrypted = encrypted.replace(" ","")
    len_full_phrase = len(encrypted)
    all_words = nltk.corpus.words.words()
    letter_distribution = nltk.FreqDist(encrypted)
    trimmed_wordlist = [w.upper() for w in all_words if len(w) <= len_full_phrase - count_words + 1]
    matching_wordlist = [w for w in trimmed_wordlist if nltk.FreqDist(w) <= letter_distribution]
    sorted_wordlist = sorted(matching_wordlist, key = lambda s: len(s))
    print('number of matching words',len(matching_wordlist))

    searchDictionary(sorted_wordlist,letter_distribution,encrypted,count_words)


def searchDictionary(sorted_wordlist,letter_distribution,encrypted,word_count,idx=0,match=[],matches = [], level=0):
    sentence = "".join(match)
    len_match = len(match)
    print(idx,len(sorted_wordlist),len_match,word_count)
    if len_match == word_count or idx == len(sorted_wordlist):
        print(match)
        return match
    
    
    while idx < len(sorted_wordlist):
        word = sorted_wordlist[idx]
        print('recursing',level,idx,word)
        if len(sentence+word) <= len(encrypted) if len_match < word_count else len(sentence+word) == len(encrypted):
            if(nltk.FreqDist(sentence+word) <= letter_distribution):
                match.append(word)
                matches.append(searchDictionary(sorted_wordlist,letter_distribution,encrypted,word_count,idx,match,level+1))
        idx+=1

    return matches

    
anagrams('IAAGLTKYCNEALY O   REI YUDSDKSOI')
#z = bruteforce('IAAGLTKYCNEALY O   REI YUDSDKSOI')
#print(z)  


