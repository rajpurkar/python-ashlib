import os
import sys
import re

from . import gender

## Title #####################################################################################

class Title(object):
    
    TITLE_MR_REGEX = "^mr\.?$" # Mr.
    TITLE_MRS_REGEX = "^mr?s\.?$" # Mrs. and Ms.
    TITLE_DR_REGEX = "^dr\.?$" # Dr.
    TITLE_SIR = "sir"
    TITLE_MADAM = "madam"
    TITLE_MONSIEUR = "monsieur" # French
    TITLE_MADAME = "madame" # French
    TITLE_KING = "king"
    TITLE_QUEEN = "queen"
    TITLE_PRINCE = "prince"
    TITLE_PRINCESS = "princess"
    TITLE_DUKE = "duke"
    TITLE_DUCHESS = "duchess"
    TITLE_BARON = "baron"
    TITLE_BARONESS = "baroness"
    ## TODO: lots of potential additions to list of royalty titles (see http://en.wikipedia.org/wiki/Royal_and_noble_ranks)
    
    LANGUAGE_ENGLISH = "English"
    LANGUAGE_FRENCH = "French"
    
    RESPECT_LEVEL_ROYALTY = "royalty"
    RESPECT_LEVEL_HIGH = "high"
    RESPECT_LEVEL_NEUTRAL = "neutral"
    RESPECT_LEVEL_LOW = "low"
    
    def __init__(self, word):
        self.word = word
        
        word = word.lower()
        
        # Defaults
        self.language = self.LANGUAGE_ENGLISH
        
        if self.__matches(self.TITLE_MR_REGEX, word):
            self.gender = gender.MALE
            self.respectLevel = self.RESPECT_LEVEL_NEUTRAL
        
        elif self.__matches(self.TITLE_MRS_REGEX, word):
            self.gender = gender.FEMALE
            self.respectLevel = self.RESPECT_LEVEL_NEUTRAL
                
        elif self.__matches(self.TITLE_DR_REGEX, word):
            self.gender = gender.NEUTRAL
            self.respectLevel = self.RESPECT_LEVEL_HIGH
        
        elif word == self.TITLE_SIR:
            self.gender = gender.MALE
            self.respectLevel = self.RESPECT_LEVEL_HIGH
                
        elif word == self.TITLE_MADAM:
            self.gender = gender.FEMALE
            self.respectLevel = self.RESPECT_LEVEL_HIGH
        
        elif word == self.TITLE_MONSIEUR:
            self.gender = gender.MALE
            self.respectLevel = self.RESPECT_LEVEL_HIGH
            self.language = self.LANGUAGE_FRENCH
        
        elif word == self.TITLE_MADAME:
            self.gender = gender.FEMALE
            self.respectLevel = self.RESPECT_LEVEL_HIGH
            self.language = self.LANGUAGE_FRENCH
        
        elif word == self.TITLE_KING:
            self.gender = gender.MALE
            self.respectLevel = self.RESPECT_LEVEL_ROYALTY
        
        elif word == self.TITLE_QUEEN:
            self.gender = gender.FEMALE
            self.respectLevel = self.RESPECT_LEVEL_ROYALTY
        
        elif word == self.TITLE_PRINCE:
            self.gender = gender.MALE
            self.respectLevel = self.RESPECT_LEVEL_ROYALTY
        
        elif word == self.TITLE_PRINCESS:
            self.gender = gender.FEMALE
            self.respectLevel = self.RESPECT_LEVEL_ROYALTY
        
        elif word == self.TITLE_DUKE:
            self.gender = gender.MALE
            self.respectLevel = self.RESPECT_LEVEL_ROYALTY
        
        elif word == self.TITLE_DUCHESS:
            self.gender = gender.FEMALE
            self.respectLevel = self.RESPECT_LEVEL_ROYALTY
        
        elif word == self.TITLE_BARON:
            self.gender = gender.MALE
            self.respectLevel = self.RESPECT_LEVEL_ROYALTY
        
        elif word == self.TITLE_BARONESS:
            self.gender = gender.FEMALE
            self.respectLevel = self.RESPECT_LEVEL_ROYALTY

        else:
            raise Exception("Invalid title.")
                
    def isMale(self):
        return gender.isMale(self.gender)
    
    def couldBeMale(self):
        return gender.couldBeMale(self.gender)
    
    def isFemale(self):
        return gender.isFemale(self.gender)
    
    def couldBeFemale(self):
        return gender.couldBeFemale(self.gender)
    
    def __repr__(self):
        return self.word

    @classmethod
    def valid(cls, word):
        word = word.lower()
        for regex in cls.titleRegexes():
            if cls.__matches(regex, word):
                return True
        return False
                
    @classmethod
    def titleRegexes(cls):
        return [cls.TITLE_MR_REGEX,
                cls.TITLE_MRS_REGEX,
                cls.TITLE_DR_REGEX,
                cls.__toRegex(cls.TITLE_SIR),
                cls.__toRegex(cls.TITLE_MADAM),
                cls.__toRegex(cls.TITLE_MONSIEUR),
                cls.__toRegex(cls.TITLE_MADAME),
                cls.__toRegex(cls.TITLE_KING),
                cls.__toRegex(cls.TITLE_QUEEN),
                cls.__toRegex(cls.TITLE_PRINCE),
                cls.__toRegex(cls.TITLE_PRINCESS),
                cls.__toRegex(cls.TITLE_DUKE),
                cls.__toRegex(cls.TITLE_DUCHESS),
                cls.__toRegex(cls.TITLE_BARON),
                cls.__toRegex(cls.TITLE_BARONESS)]

    @staticmethod
    def __matches(regex, string):
        return not re.match(regex, string) == None

    @staticmethod
    def __toRegex(title):
        return "^" + title + "$"

## PersonalPronoun ###########################################################################

class PersonalPronoun(object):
    
    PRONOUN_I = "i"
    PRONOUN_YOU = "you"
    PRONOUN_HE = "he"
    PRONOUN_SHE = "she"
    PRONOUN_ME = "me"
    PRONOUN_HIM = "him"
    PRONOUN_HER = "her"
    PRONOUN_WE = "we"
    PRONOUN_THEY = "they"
    PRONOUN_US = "us"
    PRONOUN_THEM = "them"
    
    PRONOUNS = set([PRONOUN_I,
                    PRONOUN_YOU,
                    PRONOUN_HE,
                    PRONOUN_SHE,
                    PRONOUN_ME,
                    PRONOUN_HIM,
                    PRONOUN_HER,
                    PRONOUN_WE,
                    PRONOUN_THEY,
                    PRONOUN_THEM])
    
    NUMBER_SINGULAR = "singular"
    NUMBER_PLURAL = "plural"
    NUMBER_AMBIGUOUS = "ambiguous"
    
    FIRST_PERSON = 1
    SECOND_PERSON = 2
    THIRD_PERSON = 3
    
    TYPE_SUBJECT = "subject"
    TYPE_OBJECT= "object"
    TYPE_ABIGUOUS = "ambiguous"

    def __init__(self, word):
        self.word = word
        
        word = word.lower()
        
        if word == self.PRONOUN_I:
            self.number = self.NUMBER_SINGULAR
            self.person = self.FIRST_PERSON
            self.gender = gender.NEUTRAL
            self.type = self.TYPE_SUBJECT
        
        elif word == self.PRONOUN_YOU:
            self.number = self.NUMBER_AMBIGUOUS
            self.person = self.SECOND_PERSON
            self.gender = gender.NEUTRAL
            self.type = self.TYPE_ABIGUOUS
        
        elif word == self.PRONOUN_HE:
            self.number = self.NUMBER_SINGULAR
            self.person = self.THIRD_PERSON
            self.gender = gender.MALE
            self.type = self.TYPE_SUBJECT
        
        elif word == self.PRONOUN_SHE:
            self.number = self.NUMBER_SINGULAR
            self.person = self.THIRD_PERSON
            self.gender = gender.FEMALE
            self.type = self.TYPE_SUBJECT
        
        elif word == self.PRONOUN_ME:
            self.number = self.NUMBER_SINGULAR
            self.person = self.FIRST_PERSON
            self.gender = gender.NEUTRAL
            self.type = self.TYPE_OBJECT
        
        elif word == self.PRONOUN_HIM:
            self.number = self.NUMBER_SINGULAR
            self.person = self.THIRD_PERSON
            self.gender = gender.MALE
            self.type = self.TYPE_OBJECT
        
        elif word == self.PRONOUN_HER:
            self.number = self.NUMBER_SINGULAR
            self.person = self.THIRD_PERSON
            self.gender = gender.FEMALE
            self.type = self.TYPE_OBJECT
        
        elif word == self.PRONOUN_WE:
            self.number = self.NUMBER_SINGULAR
            self.person = self.FIRST_PERSON
            self.gender = gender.NEUTRAL
            self.type = self.TYPE_SUBJECT
        
        elif word == self.PRONOUN_THEY:
            self.number = self.NUMBER_AMBIGUOUS
            self.person = self.THIRD_PERSON
            self.gender = gender.NEUTRAL
            self.type = self.TYPE_SUBJECT

        elif word == self.PRONOUN_US:
            self.number = self.NUMBER_PLURAL
            self.person = self.FIRST_PERSON
            self.gender = gender.NEUTRAL
            self.type = self.TYPE_OBJECT

        elif word == self.PRONOUN_THEM:
            self.number = self.NUMBER_AMBIGUOUS
            self.person = self.THIRD_PERSON
            self.gender = gender.NEUTRAL
            self.type = self.TYPE_OBJECT

        else:
            raise Exception("Invalid pronoun.")

    def isSingular(self):
        return self.number == self.NUMBER_SINGULAR

    def couldBeSingular(self):
        return self.number == self.NUMBER_SINGULAR or self.number == self.NUMBER_AMBIGUOUS

    def isPlural(self):
        return self.number == self.NUMBER_PLURAL

    def couldBePlural(self):
        return self.number == self.NUMBER_PLURAL or self.number == self.NUMBER_AMBIGUOUS
    
    def isFirstPerson(self):
        return self.person == self.FIRST_PERSON
    
    def isSecondPerson(self):
        return self.person == self.SECOND_PERSON
    
    def isThirdPerson(self):
        return self.person == self.THIRD_PERSON
    
    def isMale(self):
        return gender.isMale(self.gender)
    
    def couldBeMale(self):
        return gender.couldBeMale(self.gender)
    
    def isFemale(self):
        return gender.isFemale(self.gender)
    
    def couldBeFemale(self):
        return gender.couldBeFemale(self.gender)
    
    def isSubject(self):
        return self.type == self.TYPE_SUBJECT
    
    def isObject(self):
        return self.type == self.TYPE_OBJECT
    
    def __repr__(self):
        return self.word

    @classmethod
    def valid(cls, word):
        return word.lower() in cls.PRONOUNS

## functions #################################################################################

def isTitle(word):
    return Title.valid(word)

def isPersonalPronoun(word):
    return PersonalPronoun.valid(word)

## tests #####################################################################################

def main():
    assert isSalutation("Mrs")
    assert isSalutation("Mrs.")
    assert isSalutation("Ms")
    assert isSalutation("Ms.")
    assert isSalutation("Mr")
    assert isSalutation("Mr.")
    assert not isSalutation("Mr..")
    assert not isSalutation("Mra")
    assert isSalutation("Dr")
    assert isSalutation("Dr.")
    assert not isSalutation("Dr..")
    assert not isSalutation("Dra")
    assert isSalutation("Sir")
    assert isSalutation("Madam")
    assert isSalutation("Monsieur")
    assert isSalutation("Madame")
    assert not isSalutation("asdf")

if __name__ == '__main__':
    main()
