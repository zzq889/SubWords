#!/usr/bin/python
#_*_ encoding:utf-8 _*_

import sys, getopt

class SubWords:
    def __init__(self):
        self.dict = []
        self.result = []
        self.vocabs = []
        self.priorVocabs = []
        self.mustHave = []

    def readDict(self):
        f = open('wordsEn.txt', 'r')
        for line in f.readlines():
            word = line.strip()
            if word:
                self.dict.append(word)

    def searchQuery(self, query, prior = None, mustHave = None):
        self.vocabs = list(query)
        for word in self.dict:
            if self.isSubWord(word):
                if not mustHave:
                    self.result.append(word)
                else:
                    self.mustHave = list(mustHave)
                    if self.wordContainsMustHave(word):
                        self.result.append(word)

        if prior:
            self.priorVocabs = list(prior)
            self.result = sorted(self.result, key=lambda k:(self.wordPriority(k), len(k)))
        else:
            self.result = sorted(self.result, key=len)

    def isSubWord(self, word):
        v = [x for x in self.vocabs]
        for letter in list(word):
            if letter in v:
                v.remove(letter)
            else:
                return False
        return True

    def wordPriority(self, word):
        priority = 0
        v = [x for x in self.priorVocabs]
        for letter in list(word):
            if letter in v:
                priority += 1
                v.remove(letter)
        return priority

    def wordContainsMustHave(self, word):
        contain = True
        newWord = list(word)
        v = [x for x in self.mustHave]
        for letter in v:
            if not letter in newWord:
                contain = False
                break
            else:
                newWord.remove(letter)

        return contain

if __name__ == '__main__':
    words = SubWords()
    words.readDict()
    argv = sys.argv[1:]
    if len(argv) == 3:
        words.searchQuery(argv[0], argv[1], argv[2])
    elif len(argv) == 2:
        words.searchQuery(argv[0], argv[1])
    elif len(argv) == 1:
        words.searchQuery(argv[0])

    r = words.result
    for w in r:
        print(w, words.wordPriority(w))