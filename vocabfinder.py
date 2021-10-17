# stop words should have a low score by default
# given text, tokenize the text to remove any conjugation suffixes
# frequency dataset, character frequency, number of syllables, length, common and uncommon groups of vowels/consonants (spelling difficulty)
# NLTK + dictionary api + tensorflow
# levenshein distance between word and phonetic spelling of word

import nltk
#nltk.download('cmudict')
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
from wordfreq import word_frequency
from nltk.corpus import cmudict
d = cmudict.dict()


letters = ['a', 'b', 'c', 'd' ,'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y', 'z']
wordstoprocess = " The output of word tokenization can be converted to Data Frame for better text understanding in machine learning applications. It can also be provided as input for further text cleaning steps such as punctuation removal, numeric character removal or stemming"

tokenized = word_tokenize(wordstoprocess)
removelist = []

for i in range(len(tokenized)):
    if i < len(tokenized):
        if len(tokenized[i]) == 0 or tokenized[i][0] not in letters:
            removelist.append(i)

counter = 0
#print(len(tokenized), removelist)
for removeindex in removelist:
    del tokenized[removeindex-counter]
    counter += 1

tokenized_character_freqency = [[0 for i in range(26)] for j in range(len(tokenized))]

for i in range(len(tokenized)):
    tokenized[i] = tokenized[i].lower()
    for character in tokenized[i]:
        tokenized_character_freqency[i][letters.index(character)] += 1


def get_syllables(word):
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
    except KeyError:
        #if word not found in cmudict
        count = 0
        vowels = 'aeiouy'
        word = word.lower()
        if word[0] in vowels:
            count +=1
        for index in range(1,len(word)):
            if word[index] in vowels and word[index-1] not in vowels:
                count +=1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count += 1
        if count == 0:
            count += 1
        return count

tokenized_frequency = []
for word in tokenized:
    tokenized_frequency.append(word_frequency(word, "en"))
    print(word + ": " + str(word_frequency(word, "en")*100) + " " + str(get_syllables(word)))



        
        
        
# train an ML model for syllable classification

# tokenize - contains list of words
# tokenized_character_frequency - contains character frequency list for each word
# tokenized_frequnecy - contains word frequency scaled between 0 and 1