# -*- coding: utf-8 -*-

import jpype as jp
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup
import requests

import openpyxl as op
import xlrd
## Zemberek: Word Generation Example
# Documentation: https://github.com/ahmetaa/zemberek-nlp/tree/master/morphology#word-generation
# Java Code Example: https://github.com/ahmetaa/zemberek-nlp/blob/master/examples/src/main/java/zemberek/examples/morphology/GenerateWords.java

# Relative path to Zemberek .jar
ZEMBEREK_PATH = '/home/busra/System_Programming_HWS/src/0.17.1-20190726T121643Z-001/0.17.1/zemberek-full.jar'

# Start the JVM
jp.startJVM(jp.getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))

# Import the required Java classes
TurkishMorphology = jp.JClass('zemberek.morphology.TurkishMorphology')
TurkishSpellChecker = jp.JClass('zemberek.normalization.TurkishSpellChecker')
TurkishSentenceNormalizer = jp.JClass('zemberek.normalization.TurkishSentenceNormalizer')
Paths = jp.JClass('java.nio.file.Paths')
morphology = TurkishMorphology.createWithDefaults()
# Instantiate the spell checker class using the morphology instance
spell = TurkishSpellChecker(morphology)


df = pd.read_excel ('busra_sentiwordnet_rule_derivation_with_pos_tags.xlsx')
liste = []
text_list = []
word_list= []


for word in df['stemmed_version']:
    word = str(word)
    if 'Ã§' in word or 'รง' in word or 'Ã‡' in word:
        word = word.replace('Ã§', 'ç')
        word = word.replace('รง', 'ç')
        word = word.replace('Ã‡', 'ç')
    if 'Ä±' in word:
        word = word.replace('Ä±', 'ı')
    if 'ÄŸ' in word:
        word = word.replace('ÄŸ', 'ğ')
    if 'Ã¶' in word or 'รถ':
        word = word.replace('Ã¶', 'ö')
        word = word.replace('รถ', 'ö')
    if 'ÅŸ' in word:
        word = word.replace('ÅŸ', 'ş')
    if 'Ã¼' in word:
        word = word.replace('Ã¼', 'ü')

    text_list.append(word)
    analysis = morphology.analyzeSentence(word)
    sonuclar = morphology.disambiguate(word, analysis).bestAnalysis()
    liste.append(str(sonuclar))

k = 0
for list_word in liste:
        splitted = list_word.split("]")
        text = text_list[k]

        if text.find(' ') != -1:#if text contains words more than 1
            kelime = text.split(" ")
            ilk_kelime = kelime[0]
            #if "Verb" in splitted[0]:  # suffixation if text contains two words with first word is verb
               # if "Adj" in splitted[1] or "Noun" in splitted[1]:  # add suffix for first word
                    #ikinci_kelime = text[text.find(' '):]
                    #for i in ilk_kelime:
                       # if i in 'eiöü':
                        #    ilk_kelime = ilk_kelime + "mek"
                         #   break
                      #  elif i in 'aıou':
                        #    ilk_kelime = ilk_kelime + "mak"
                         #   break
                   # ilk_kelime = ilk_kelime.replace(" ", "+")
                    #source = requests.get('https://cooljugator.com/tr/' + ilk_kelime)
                    #soup = BeautifulSoup(source.content, "lxml")

                   # ana = soup.find('body')
                   # alt = ana.findAll('div', attrs={"class": "conjugation-cell conjugation-cell-our"})
                    #new = ana.findAll('div', attrs={"class": "meta-form"})
                    #for i in new:
                     #   text = i.text + ikinci_kelime
                     #   word_list.append(text)

               # elif "Verb" in splitted[1]:  # add suffix for second word
                  #  ikinci_kelime = text[text.find(' '):]
                  #  for i in ilk_kelime:
                     #   if i in 'eiöü':
                     #       ilk_kelime = ilk_kelime + "mek"
                      #      break
                      #  elif i in 'aıou':
                      #      ilk_kelime = ilk_kelime + "mak"
                      #      break
                   # for i in ikinci_kelime:
                     #   if i in 'eiöü':
                        #    ikinci_kelime = ikinci_kelime + "mek"
                        #    break
                      #  elif i in 'aıou':
                       #     ikinci_kelime = ikinci_kelime + "mak"
                       #     break
                 #   ilk_kelime = ilk_kelime.replace(" ", "+")
                 #   source = requests.get('https://cooljugator.com/tr/' + ilk_kelime)
                 #   soup = BeautifulSoup(source.content, "lxml")

                   # ana = soup.find('body')
                    #alt = ana.findAll('div', attrs={"class": "conjugation-cell conjugation-cell-our"})
                    #new = ana.findAll('div', attrs={"class": "meta-form"})

                    #for i in new:
                      #  text = i.text + ikinci_kelime
                       # word_list.append(text)

                    #ikinci_kelime = ikinci_kelime.replace(" ", "+")
                    #source = requests.get('https://cooljugator.com/tr/' + ikinci_kelime)
                    #soup = BeautifulSoup(source.content, "lxml")

                   # ana = soup.find('body')
                  #  alt = ana.findAll('div', attrs={"class": "conjugation-cell conjugation-cell-our"})
                   # new = ana.findAll('div', attrs={"class": "meta-form"})
                   # for i in new:
                     #   text = ilk_kelime + i.text
                      #  word_list.append(text)

            if "Adj" in splitted[0] or "Noun" in splitted[0]:  # suffixation if text is verb and text contains two words
                    if "Verb" in splitted[1]:  # add suffix for first word
                        ikinci_kelime = text[text.find(' '):]
                        for i in ikinci_kelime:
                            if i in 'eiöü':
                                ikinci_kelime = ikinci_kelime + "mek"
                                break
                            elif i in 'aıou':
                                ikinci_kelime = ikinci_kelime + "mak"
                                break

                        ikinci_kelime = ikinci_kelime.replace(" ", "+")
                        source = requests.get('https://cooljugator.com/tr/' + ikinci_kelime)
                        soup = BeautifulSoup(source.content, "lxml")

                        ana = soup.find('body')
                        alt = ana.findAll('div', attrs={"class": "conjugation-cell conjugation-cell-our"})
                        new = ana.findAll('div', attrs={"class": "meta-form"})
                        for i in new:
                            text = ilk_kelime + i.text
                            word_list.append(text)

        else:#if text contains just 1 word
            if "Noun" in splitted[0]:#if word is noun
                # Disabling the cache and building using the word as the lexicon itself
                morphology = TurkishMorphology.builder().setLexicon(text).disableCache().build()

                # Getting the dictionary item
                dictionary_item = morphology.getLexicon().getMatchingItems(text).get(0)

                # Possessive and case suffix combinations will
                # be used for generating inflections of the word
                number = ['A3sg', 'A3pl']
                possessives = ['P1sg', 'P2sg', 'P3sg']
                cases = ['Dat', 'Loc', 'Abl', 'Gen', 'Acc', 'Inst', 'Nom']
                suffixes = {"With", "Past", "A3sg"}
                # tenses = ['Fut', 'Past']

                # Iterating the Result class instance to to access
                # the generated word and the analysis
                for numberM in number:
                    for possessiveM in possessives:
                        for caseM in cases:
                            results = morphology.getWordGenerator().generate(dictionary_item, numberM, possessiveM,
                                                                             caseM)
                            for result in results:
                                #print('Surface Form: %s' % result.surface)
                                #print('Analysis: %s\n' % result.analysis)
                                text = str(result).split("-")
                                if spell.check(text[0]):#if noun is correct
                                    word_list.append(text[0])

                                #print(text[0])

            if "Verb" in splitted[0]:  # if word is verb
                for i in text:
                    if i in 'eiöü':
                        text = text + "mek"
                        break
                    elif i in 'aıou':
                        text = text + "mak"
                        break

                text = text.replace(" ", "+")
                source = requests.get('https://cooljugator.com/tr/' + text)
                soup = BeautifulSoup(source.content, "lxml")

                ana = soup.find('body')
                alt = ana.findAll('div', attrs={"class": "conjugation-cell conjugation-cell-our"})
                new = ana.findAll('div', attrs={"class": "meta-form"})

                for i in new:
                    word_list.append(i.text)

        #print(text)
        k = k+1

# Do basic spell checking and print the results

#for word in word_list:
	#print('%s -> Correct' % (word) if spell.check(word) else '%s -> Wrong' % (word))


dafram = DataFrame({'Word List': word_list})
dafram.to_excel('New_Word_Generator_2.xlsx', index=True)

# Shutting down the JVM
jp.shutdownJVM()