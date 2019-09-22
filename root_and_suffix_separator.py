# -*- coding: utf-8 -*-

import jpype as jp
import re
import string
import csv

## Zemberek: Ambiguity Resolution Example
# Documentation: https://github.com/ahmetaa/zemberek-nlp/tree/master/morphology#ambiguity-resolution
# Java Code Example: https://github.com/ahmetaa/zemberek-nlp/blob/master/examples/src/main/java/zemberek/examples/morphology/DisambiguateSentences.java

# Relative path to Zemberek .jar
ZEMBEREK_PATH = '/home/busra/System_Programming_HWS/src/0.17.1-20190726T121643Z-001/0.17.1/zemberek-full.jar'

# Start the JVM
jp.startJVM(jp.getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))

# Import required Java classes
TurkishMorphology = jp.JClass('zemberek.morphology.TurkishMorphology')
Paths = jp.JClass('java.nio.file.Paths')

# Instantiating the morphology class with the default RootLexicon
morphology = TurkishMorphology.createWithDefaults()

lineList = [line.rstrip('\n') for line in open("tests2.txt")]
#REGEX = re.compile(r":\s*")
#REGEX2 = re.compile(r"\+\s*")

regex = re.compile('\+(.*?)\:')

# Dummy sentence to work on
for word in lineList:

    # Analyzing the dummy sentence. The returning WordAnalysis
    # object which can include zero or more SingleAnalysis objects
    analysis = morphology.analyzeSentence(word)

    # Resolving the ambiguity

    sonuclar = morphology.disambiguate(word, analysis).bestAnalysis()
    stemmed = []
    temp = []
    # Printing the results
    if "Ques" in str(sonuclar):
        stemmed.append("-")
    else:
       for i, sonuc in enumerate(sonuclar):



            x = sonuc.formatLong()
            stem = ' '.join(sonuc.getStems())
            #print('Analysis %d: %s' % (i+1, sonuc.formatLong()))
            #print('Stems %d: %s' % (i+1, ' '.join(sonuc.getStems())))
            stemmed = regex.findall(x)

            for a in stemmed:
               if "A3sg+" in stemmed[0]:
                    stemmed[0]  = stemmed[0].replace("A3sg+","")
               elif "Aor+" in stemmed[0]:
                    stemmed[0] = stemmed[0].replace("Aor+", "")
               elif len(stemmed) > 1 and "Aor+" in stemmed[1]:
                    stemmed[1] = stemmed[1].replace("Aor+", "")
               elif len(stemmed) > 1 and "A3sg+" in stemmed[1]:
                    stemmed[1]  = stemmed[1].replace("A3sg+","")
               elif "A3sg|" in stemmed[0]:
                    stemmed[0]  = stemmed[0].replace("A3sg|","")
               elif len(stemmed) > 1 and "A3sg|" in stemmed[1]:
                    stemmed[1] = stemmed[1].replace("A3sg|", "")

    #stemmed.insert(0, stem)
    #print(stemmed)
    with open('vocab_file_2.csv', mode='a') as employee_file:
       employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

       if len(stemmed) == 0:
         stemmed.append("-")
         employee_writer.writerow(stemmed)
       else:
         employee_writer.writerow(stemmed)

# Shutting down the JVM
jp.shutdownJVM()

#       if "Ques" in str(sonuclar):
#           x = sonuc.formatLong()
#           stem = ' '.join(sonuc.getStems())
#           print('Analysis %d: %s' % (i + 1, sonuc.formatLong()))
#           #print(str(sonuclar))
#           stemmed.insert(i,str(regex.findall(x)))

#       else: