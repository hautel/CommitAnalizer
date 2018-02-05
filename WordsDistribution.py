import Configurations
from os import listdir
from os.path import isfile, join, isdir, basename, dirname, exists
from os import makedirs
import re
from shutil import copyfile
import io
import string
import nltk
from nltk.util import ngrams

from Utils import *


def GetFilesList(folder):

    files = []

    oneFileFolder = join(folder, 'MSG')
    repoFolders = GetFoldersInDatasetPath(oneFileFolder)
    for repoFolder in repoFolders:
        repoFiles = GetFilesInFolder(repoFolder)
        files.extend(repoFiles)

    return files


def GetUnigrams(files):
    tokens = []
    for file in files:
        with open(file, 'r') as fobj:
            text = fobj.read().lower().strip()
            tokens.extend(nltk.tokenize.word_tokenize(text))

    return tokens

def GetBigrams(files):
    bigrams = []
    for file in files:
        with open(file, 'r') as fobj:
            text = fobj.read().lower().strip()
            tokens = nltk.tokenize.word_tokenize(text)
            bigrams.extend(ngrams(tokens, 2))

    return bigrams

def SaveUnigramDistribution(baseFolder, filePath):
    files = GetFilesList(baseFolder)
    unigrams = GetUnigrams(files)

    freq = nltk.FreqDist(unigrams)

    ordered = freq.most_common(len(freq))

    with open(filePath, 'w') as fobj:
        for token in ordered:
            line = token[0] + " " + str(token[1]) + '\n'
            fobj.write(line)

    return unigrams


def SaveBigramDistribution(baseFolder, filePath):
    files = GetFilesList(baseFolder)
    bigrams = GetBigrams(files)

    freq = nltk.FreqDist(bigrams)

    ordered = freq.most_common(len(freq))

    with open(filePath, 'w') as fobj:
        for token in ordered:
            line = '[' + token[0][0] + ' ' + token[0][1] + "] " + str(token[1]) + '\n'
            fobj.write(line)

    return bigrams

#nltk.download('punkt')
#files = GetFilesInFolder(join(join(Configurations.JavaDestPath,'MSG'),'repo1'))

def SaveAllUnigrams():
    javaunigrams = SaveUnigramDistribution(Configurations.JavaDestPath, 'javaUnigrams.txt')
    testunigrams = SaveUnigramDistribution(Configurations.JavaTestDestPath, 'testUnigrams.txt')
    xmlunigrams = SaveUnigramDistribution(Configurations.PomDestPath, 'xmlUnigrams.txt')

    allUnigrams = []

    allUnigrams.extend(javaunigrams)
    allUnigrams.extend(testunigrams)
    allUnigrams.extend(xmlunigrams)

    allfreq = nltk.FreqDist(allUnigrams)

    allordered = allfreq.most_common(len(allfreq))

    with open('allunigrams.txt', 'w') as fobj:
        for token in allordered:
            line = token[0] + " " +str(token[1]) + '\n'
            fobj.write(line)


def SaveAllBigrams():
    javabigrams = SaveBigramDistribution(Configurations.JavaDestPath, 'javaBigrams.txt')
    testbigrams = SaveBigramDistribution(Configurations.JavaTestDestPath, 'testBigrams.txt')
    xmlbigrams = SaveBigramDistribution(Configurations.PomDestPath, 'xmlBigrams.txt')

    allBigrams = []

    allBigrams.extend(javabigrams)
    allBigrams.extend(testbigrams)
    allBigrams.extend(xmlbigrams)

    allBigramFreq = nltk.FreqDist(allBigrams)

    allBigramOrdered = allBigramFreq.most_common(len(allBigramFreq))

    with open('allbigrams.txt', 'w') as fobj:
        for token in allBigramOrdered:
            line = '[' + token[0][0] + ' ' + token[0][1] + "] " + str(token[1]) + '\n'
            fobj.write(line)

SaveAllBigrams()

x=1


