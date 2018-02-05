import Configurations
from os import listdir
from os.path import isfile, join, isdir, basename, dirname, exists
import json
from os import makedirs
from Utils import *
from pprint import pprint


def SaveFilesForClassifier(basePath, saveNonInformativeDir):
    informativePath = join(basePath, 'INFORMATIVE')
    repoDirs = GetFoldersInDatasetPath(informativePath)
    for repoDir in repoDirs:
        if saveNonInformativeDir:
            repoDir = join(repoDir, 'NONINFORMATIVE')
        jsonFiles = GetFilesInFolder(repoDir)



def ReviewFilesForClassifier(basePath, saveNonInformativeDir):
    informativePath = join(basePath, 'INFORMATIVE')
    destFolder = Configurations.ClassifierJsonDest
    repoDirs = GetFoldersInDatasetPath(informativePath)
    i = 0
    for repoDir in repoDirs:
        fileCount = 0
        if saveNonInformativeDir:
            repoDir = join(repoDir, 'NONINFORMATIVE')
        jsonFiles = GetFilesInFolder(repoDir)
        for file in jsonFiles:
            fileCount += 1

            i+=1
            fileName = basename(file)
            fileShortFolder = ''
            if saveNonInformativeDir:
                fileShortFolder = join(basename(dirname(dirname(dirname(dirname(file))))), basename(dirname(file)))
            else:
                fileShortFolder = join(basename(dirname(dirname(dirname(file)))),basename(dirname(file)))
            destFilePath = join(destFolder, fileShortFolder)
            if not exists(destFilePath):
                makedirs(destFilePath)
            destFilePath = join(destFilePath, fileName)
            if exists(destFilePath):
                continue
            if fileCount > 20:
                break
            print('Example ' + str(i))
            with open(file, 'r') as fobj:
                data = json.load(fobj)
                print('Msg path: ' + data['msgPath'])
                print('Msg: \n' + data['msg'] + '\n')
                print('Diff: \n' + data['diff'] + '\n')
                print('MsgTokens:')
                print(data['words'])
                print('Pos:')
                print(data['pos'])
                if 'relevant' not in data:
                    data['relevant'] = 1
                print('Relevant: ' + str(data['relevant']) + '   ')
                data['relevant'] = input('')
                print('Informative: ' + str(data['informative']) + '   ')
                data['informative'] = input('')
                print('Naturalness: ' + str(data['naturalness']) + '   ')
                data['naturalness'] = input('')
                data['isReviewd'] = 1
                resultJsonData = json.dumps(data)
                with open(destFilePath, 'w') as destfobj:
                    destfobj.write(resultJsonData)



ReviewFilesForClassifier(Configurations.JavaDestPath, False)
