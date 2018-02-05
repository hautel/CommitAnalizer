import Configurations
from os import listdir
from os.path import isfile, join, isdir, basename, dirname, exists
from os import makedirs
import re
from shutil import copyfile
import io
import string
import nltk
from Utils import *




def getMessagesList(commitsPath):
    log = []
    messageBasePath = Configurations.MessagePath
    for commitPath in commitsPath:
        try:
            shortPath = join(basename(dirname(commitPath)), basename(commitPath))
            shortPath = shortPath.replace('.diff', '.msg')
            baseDestPath = join(dirname(dirname(dirname(commitPath))), 'MSG')
            messagePath = join(messageBasePath, shortPath)
            destMsgPath = join(baseDestPath, shortPath)
            if not exists(dirname(destMsgPath)):
                makedirs(dirname(destMsgPath))
            with io.open(messagePath, 'r', encoding='ascii') as fobj:
                log.append(messagePath + " OK")
                allLines = fobj.read().strip().split('\n')
                if allLines[0].strip().lower().find('merge') == 0:
                    text = string.join(allLines[2:], '\n')
                    with open(destMsgPath, 'w') as df:
                        df.write(text)
                    continue
            copyfile(messagePath, destMsgPath)
        except:
            log.append(messagePath + " NOK")


    return log


def getSpecialMessagesList(commitsPath):
    log = []
    messageBasePath = Configurations.MessagePath
    for commitPath in commitsPath:
        try:
            shortPath = join(basename(dirname(commitPath)), basename(commitPath))
            shortPath = shortPath.replace('.diff', '.cmsg')
            baseDestPath = join(dirname(dirname(dirname(commitPath))), 'MSG')
            messagePath = join(messageBasePath, shortPath)
            destMsgPath = join(baseDestPath, shortPath)
            destMsgPath = destMsgPath.replace('.cmsg', '.msg')
            if not exists(dirname(destMsgPath)):
                makedirs(dirname(destMsgPath))
            with io.open(messagePath, 'r', encoding='ascii') as fobj:
                log.append(messagePath + " OK")
                allLines = fobj.read().strip().split('\n')
                if allLines[0].strip().lower().find('merge') == 0:
                    text = string.join(allLines[2:], '\n')
                    with open(destMsgPath, 'w') as df:
                        df.write(text)
                    continue
            copyfile(messagePath, destMsgPath)
        except:
            log.append(messagePath + " NOK")


    return log


def GetCommitFiles():
    files = []
    folders = [Configurations.PomDestPath, Configurations.JavaTestDestPath, Configurations.JavaDestPath]
    for folder in folders:
        oneFileFolder = join(folder, 'OneLine')
        repoFolders = GetFoldersInDatasetPath(oneFileFolder)
        for repoFolder in repoFolders:
            repoFiles = GetFilesInFolder(repoFolder)
            files.extend(repoFiles)

    return files


def GetSpecialCommitFiles():
    files = []
    folders = [Configurations.PomDestPath, Configurations.JavaTestDestPath, Configurations.JavaDestPath]
    for folder in folders:
        oneFileFolder = join(folder, 'OneLine')
        repoFolders = GetFoldersInDatasetPath(oneFileFolder)
        for repoFolder in repoFolders:
            if 'repo-' in repoFolder:
                repoFiles = GetFilesInFolder(repoFolder)
                files.extend(repoFiles)

    return files


commitFiles = GetSpecialCommitFiles()
log = getSpecialMessagesList(commitFiles)

with open('F:\\master\\1\\Cercetare\\Dataset\\logSpecialFiles.txt', 'w') as logf:
    logf.writelines(log)





path = 'F:\\master\\1\\Cercetare\\Commitgen Public\\Commitgen Public\\commitmsgs\\repo152\\748351.diff'
path = path.replace('diff','msg')
fobj = io.open(path, 'r', encoding='utf-8')
allLines = fobj.read().strip().split('\n')
if allLines[0].strip().lower().find('merge') == 0:
    text = string.join(allLines[2:], '\n')
    print(text)
#print(chars)

