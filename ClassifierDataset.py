import Configurations
from os import listdir
from os.path import isfile, join, isdir, basename, dirname, exists
import json
from os import makedirs
import re
from shutil import copyfile
import io
import random
import string
import nltk
from Utils import *


def CreateInformativeDataset(basePath):
    punctuation = list(string.punctuation)
    punctuation.append("''")
    punctuation.append('``')
    msgPath = join(basePath, 'MSG')
    diffPath = join(basePath, 'OneLine')
    msgRepoFolders = GetFoldersInDatasetPath(msgPath)
    for msgRepoFolder in msgRepoFolders:
        repoName = basename(msgRepoFolder)
        diffRepoFolder = join(diffPath, repoName)
        msgFiles = GetFilesInFolder(msgRepoFolder)
        for msgFile in msgFiles:
            fileName = basename(msgFile).replace('.cmsg', '.diff').replace('.msg', '.diff')
            diffFile = join(diffRepoFolder, fileName)
            try:
                with open(msgFile, 'r') as msgFobj, open(diffFile, 'r') as diffFobj:
                    msgText = msgFobj.read()
                    diffText = diffFobj.read()

                    msgTokens = nltk.tokenize.word_tokenize(msgText)
                    msgTokens = tokensWithoutPunctuation(msgTokens, punctuation)

                    diffTokens = nltk.tokenize.word_tokenize(diffText)
                    diffTokens = tokensWithoutPunctuation(diffTokens, punctuation)

                    found = False
                    for msgToken in msgTokens:
                        if msgToken in diffTokens:
                            found = True
                            data = {}
                            data['diff'] = diffText
                            data['msg'] = msgText
                            data['msgPath'] = msgFile
                            data['diffPath'] = diffFile
                            data['matchingWord'] = msgToken
                            data['informative'] = 1
                            data['relevant'] = 1
                            jsonData = json.dumps(data)
                            destFolder = join(join(basePath, 'INFORMATIVE'),repoName)
                            if not exists(destFolder):
                                makedirs(destFolder)
                            jsonFileName = fileName.replace('.diff', '.json')
                            jsonFullPath = join(destFolder, jsonFileName)
                            with open(jsonFullPath, 'w') as jsonFobj:
                                jsonFobj.write(jsonData)
                            break
            except Exception as e:
                print(e)
                with open('jsonLog.txt', 'a') as jLog:
                    jLog.write('Error for file\n' + msgFile + '\n' + diffFile +'\n\n')

def IsMessageInformative(message, diff, punctuation):
    msgTokens = nltk.tokenize.word_tokenize(message)
    msgTokens = tokensWithoutPunctuation(msgTokens, punctuation)

    diffTokens = nltk.tokenize.word_tokenize(diff)
    diffTokens = tokensWithoutPunctuation(diffTokens, punctuation)

    for msgToken in msgTokens:
        if msgToken in diffTokens:
            return True

    return False

def FindRandomNonInformativeMessage(repoFolders, repoFolder, data, punctuation):

    repoFoldersList = list(repoFolders)
    repoFoldersList.remove(repoFolder)
    randRepo = random.choice(repoFoldersList)
    filesInRepo = GetFilesInFolder(randRepo)
    tries = 0
    while True:
        tries +=1
        if tries > 500 or len(repoFoldersList) == 0:
            return None
        if len(filesInRepo) == 0:
            repoFoldersList.remove(randRepo)
            randRepo = random.choice(repoFoldersList)
            filesInRepo = GetFilesInFolder(randRepo)

        randFile = random.choice(filesInRepo)
        with open(randFile, 'r') as randFobj:
            randData = json.load(randFobj)
            if not IsMessageInformative(randData['msg'], data['diff'], punctuation):
                return randData
        filesInRepo.remove(randFile)




def AugumentInformativeDatasetWithNonInformativeExamples(basePath):
    punctuation = list(string.punctuation)
    punctuation.append("''")
    punctuation.append('``')
    informativePath = join(basePath, 'INFORMATIVE')
    repoFolders = GetFoldersInDatasetPath(informativePath)
    for repoFolder in repoFolders:
        jsonFiles = GetFilesInFolder(repoFolder)
        for jsonFile in jsonFiles:
            with open(jsonFile, 'r') as jsonFobj:
                data = json.load(jsonFobj)
                nonInfoData = FindRandomNonInformativeMessage(repoFolders, repoFolder, data, punctuation)
                if nonInfoData is None:
                    continue
                resultData = {}
                resultData['diff'] = data['diff']
                resultData['msg'] = nonInfoData['msg']
                resultData['msgPath'] = nonInfoData['msgPath']
                resultData['diffPath'] = data['diffPath']
                resultData['matchingWord'] = None
                resultData['informative'] = 1
                resultData['relevant'] = 0
                resultJsonData = json.dumps(resultData)

                jsonFolder = dirname(jsonFile)
                jsonFolder = join(jsonFolder,'NONINFORMATIVE')
                if not exists(jsonFolder):
                    makedirs(jsonFolder)
                jsonFileName = basename(jsonFile)
                idx = jsonFileName.index('.json')
                destJsonFileName = jsonFileName[:idx] + '-NonInformative' + jsonFileName[idx:]
                destJsonPath = join(jsonFolder, destJsonFileName)

                with open(destJsonPath, 'w') as jsonFobj:
                    jsonFobj.write(resultJsonData)


def UpdateNonInformativeToIrelevant(basePath):
    informativePath = join(basePath, 'INFORMATIVE')
    repoFolders = GetFoldersInDatasetPath(informativePath)
    for repoFolder in repoFolders:
        nonInformativeRepoFolder = join(repoFolder, 'NONINFORMATIVE')
        jsonFiles = GetFilesInFolder(nonInformativeRepoFolder)
        for jsonFile in jsonFiles:
            with open(jsonFile, 'r+') as jsonFobj:
                data = json.load(jsonFobj)
                data['relevant'] = 0
                data['informative'] = 1
                resultJsonData = json.dumps(data)
                jsonFobj.seek(0)
                jsonFobj.write(resultJsonData)


def isMessageTooShort(message, punctuation):
    msgTokens = nltk.tokenize.word_tokenize(message)
    msgTokens = tokensWithoutPunctuation(msgTokens, punctuation)
    if len(msgTokens) <= 3:
        return True
    return False

def UpdateInformativeLevel(basePath, inNonInformativeFolder = False):
    punctuation = list(string.punctuation)
    punctuation.append("''")
    punctuation.append('``')
    informativePath = join(basePath, 'INFORMATIVE')
    repoFolders = GetFoldersInDatasetPath(informativePath)
    for repoFolder in repoFolders:
        if inNonInformativeFolder:
            repoFolder = join(repoFolder, 'NONINFORMATIVE')
        jsonFiles = GetFilesInFolder(repoFolder)
        for jsonFile in jsonFiles:
            with open(jsonFile, 'r+') as jsonFobj:
                data = json.load(jsonFobj)
                message = data['msg']
                if isMessageTooShort(message, punctuation):
                    data['informative'] = 0
                else:
                    data['informative'] = 1
                resultJsonData = json.dumps(data)
                jsonFobj.seek(0)
                jsonFobj.write(resultJsonData)


def isMessageNatural(posPath):
    try:
        with open(posPath, 'r') as fobj:
            lines = fobj.readlines()
            words = [i.split('----->')[0] for i in lines]
            pos = [i.split('----->')[1].strip() for i in lines]
            vbIntersect =[val for val in pos if val in ['VB', 'VBD', 'VBG', 'VBN', 'VBP']]
            if len(vbIntersect) >= 1:
                return True, words, pos
            return False, words, pos
    except:
        return False, None, None


def UpdateNaturalnessLevel(basePath, inNonInformativeFolder):
    posPath = join(basePath, 'POS')
    informativePath = join(basePath, 'INFORMATIVE')
    repoFolders = GetFoldersInDatasetPath(informativePath)
    for repoFolder in repoFolders:
        if inNonInformativeFolder:
            repoFolder = join(repoFolder, 'NONINFORMATIVE')
        jsonFiles = GetFilesInFolder(repoFolder)
        for jsonFile in jsonFiles:
            with open(jsonFile, 'r+') as jsonFobj:
                data = json.load(jsonFobj)
                messagePath = data['msgPath']
                fileMsgName = basename(messagePath)
                folderMsgName = basename(dirname(messagePath))
                shortPath = join(folderMsgName, fileMsgName)
                posMsgPath = join(posPath, shortPath)
                isNatural, words, pos = isMessageNatural(posMsgPath)
                if isNatural:
                    data['naturalness'] = 1
                else:
                    data['naturalness'] = 0

                data['words'] = words
                data['pos'] = pos
                data['isReviewd'] = 0

                resultJsonData = json.dumps(data)
                jsonFobj.seek(0)
                jsonFobj.write(resultJsonData)

#CreateInformativeDataset(Configurations.JavaDestPath)
#CreateInformativeDataset(Configurations.JavaTestDestPath)
#CreateInformativeDataset(Configurations.PomDestPath)

#AugumentInformativeDatasetWithNonInformativeExamples(Configurations.JavaTestDestPath)
#AugumentInformativeDatasetWithNonInformativeExamples(Configurations.JavaDestPath)
#AugumentInformativeDatasetWithNonInformativeExamples(Configurations.PomDestPath)


#UpdateNonInformativeToIrelevant(Configurations.JavaTestDestPath)
#UpdateNonInformativeToIrelevant(Configurations.JavaDestPath)
#UpdateNonInformativeToIrelevant(Configurations.PomDestPath)

#UpdateInformativeLevel(Configurations.JavaDestPath, False)
#UpdateInformativeLevel(Configurations.JavaDestPath, True)
#UpdateInformativeLevel(Configurations.JavaTestDestPath, False)
#UpdateInformativeLevel(Configurations.JavaTestDestPath, True)
#UpdateInformativeLevel(Configurations.PomDestPath, False)
#UpdateInformativeLevel(Configurations.PomDestPath, True)


#UpdateNaturalnessLevel(Configurations.JavaDestPath, False)
#UpdateNaturalnessLevel(Configurations.JavaDestPath, True)
#UpdateNaturalnessLevel(Configurations.JavaTestDestPath, False)
#UpdateNaturalnessLevel(Configurations.JavaTestDestPath, True)
#UpdateNaturalnessLevel(Configurations.PomDestPath, False)
#UpdateNaturalnessLevel(Configurations.PomDestPath, True)
