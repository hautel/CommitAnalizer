from os import listdir
from os.path import isfile, join, isdir, basename, dirname, exists
import json
from os import makedirs


def GetFoldersInDatasetPath(path):
    return [join(path, f) for f in listdir(path) if isdir(join(path, f))]


def GetFilesInFolder(path):
    files = listdir(path)
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]


def tokensWithoutPunctuation(tokens, punctuation):
    return [i for i in tokens if i not in punctuation]