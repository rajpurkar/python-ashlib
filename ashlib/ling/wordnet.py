import collections

import nltk.corpus
import pattern.en

import ashlib.ling.pos
import ashlib.ling.token

def generateSynonyms(word, loose=True):
    synonyms = collections.defaultdict(lambda: collections.Counter())
    
    addedOriginal = False
    
    phraseFromLemma = lambda lemma: lemma.name().lower().replace("_", " ")
    formatPhrase = lambda obj: obj.lower() if isinstance(obj, str) else phraseFromLemma(obj)
    
    def update(obj, pos):
        phrase = formatPhrase(obj)
        synonyms[pos][phrase] += 1
        if phrase == word: addedOriginal = True
    
    for synset in nltk.corpus.wordnet.synsets(word):
        pos = ashlib.ling.pos.standardizeWordnet(synset.pos())
        for lemma in synset.lemmas():
            update(lemma, pos)
            for tense in pattern.en.lexeme(phraseFromLemma(lemma)):
                update(tense, pos)
                    
    if not addedOriginal:
        pos = ashlib.ling.pos.tag([word])[0]
        update(word, pos)

    ## TODO: can require larger count or something like that
    isValid = lambda counter, phrase: counter[phrase] >= 1
                    
    for pos in synonyms:
        synonyms[pos] = [phrase for phrase in list(synonyms[pos].keys()) if isValid(synonyms[pos], phrase)]

    return synonyms

def collapseSynonyms(synonyms):
    aggregate = []
    for pos in synonyms:
        aggregate += synonyms[pos]
    return aggregate


