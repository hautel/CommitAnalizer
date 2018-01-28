import Configurations
from os import listdir
from os.path import isfile, join, isdir, basename, dirname, exists
from os import makedirs
import re
from shutil import copyfile
"""

"""

def isOneFileChange(text):
    try:
        lines = text.split('\n')
        totalFiles = 0
        for line in lines:
            if line.find('diff --git') != -1:
                totalFiles += 1
                if totalFiles > 1:
                    return False
        return True
    except:
        print('Error when deciding if is one file change')
        return False


def isOneLineChange(path):
    threePlus = '^([+][+][+])'
    onePlus = '^([+])'
    threeMinus = '^([-][-][-])'
    oneMinus = '^([-])'
    countPlus = 0
    countMinus = 0
    try:
        with open(path) as fobj:
            for line in fobj:
                if re.search(threePlus, line):
                    continue
                if re.search(threeMinus, line):
                    continue
                if re.search(onePlus, line):
                    countPlus += 1
                    if countPlus > 1:
                        return False
                if re.search(oneMinus, line):
                    countMinus += 1
                    if countMinus > 1:
                        return False
            return True
    except:
        return False


def countoverlappingdistinct(pattern, thestring):
    total = 0
    start = 0
    there = re.compile(pattern)
    while True:
        mo = there.search(thestring, start)
        if mo is None: return total
        total += 1
        start = 1 + mo.start()

def countMatchingString(pattern, thestring):
    total = 0
    words = thestring.split(' ')
    for word in words:
        if word.endswith(pattern):
            total += 1
    return total

def GetFoldersInDatasetPath(path):
    return [join(path, f) for f in listdir(path) if isdir(join(path, f))]

def GetFilesInFolder(path):
    files = listdir(path)
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

def GetChangesByFile(path):
    text = []
    try:
        fobj = open(path)
        content = []
        for line in fobj:
            if line.find('diff --git') != -1:
                if content != []:
                    oneFile = ''.join(content)
                    text.append(oneFile)
                    content = []
            content.append(line)
        oneFile = ''.join(content)
        text.append(oneFile)
    except:
        print("Error while getting lines")

    finally:
        fobj.close()
        return text



def IsPomFile(path):
    fileChanges = GetChangesByFile(path)
    pomfilesCount = 0
    for fileChange in fileChanges:
        lines = fileChange.split('\n')
        occu = countoverlappingdistinct(Configurations.PomRegex, lines[0])
        if occu >= 2:
            pomfilesCount += 1
    if len(fileChanges) == pomfilesCount:
        return True
    return False


def IsTextPomFile(text):
    lines = text.split('\n')
    occu = countoverlappingdistinct(Configurations.PomRegex, lines[0])
    if occu >= 2:
        return True


def IsJavaFile(path):
    fileChanges = GetChangesByFile(path)
    javaFilesCount = 0
    javaTestFilesCount = 0
    for fileChange in fileChanges:
        lines = fileChange.split('\n')
        occu = countMatchingString(Configurations.JavaMatching, lines[0])
        testOccu = countMatchingString(Configurations.JavaTestMatching, lines[0])
        if occu >= 2:
            javaFilesCount += 1
        if testOccu >= 2:
            javaTestFilesCount += 1
    if  javaFilesCount >= 1 and javaFilesCount != javaTestFilesCount:
        return True
    return False


def IsTextJavaFile(text):

    lines = text.split('\n')
    occu = countMatchingString(Configurations.JavaMatching, lines[0])
    testOccu = countMatchingString(Configurations.JavaTestMatching, lines[0])
    if occu >= 2 and testOccu <2 :
        return True
    return False


def IsJavaTestFile(path):
    fileChanges = GetChangesByFile(path)
    javaFilesCount = 0
    javaTestFilesCount = 0
    for fileChange in fileChanges:
        lines = fileChange.split('\n')
        occu = countMatchingString(Configurations.JavaMatching, lines[0])
        testOccu = countMatchingString(Configurations.JavaTestMatching, lines[0])
        if occu >= 2:
            javaFilesCount += 1
        if testOccu >= 2:
            javaTestFilesCount += 1
    if javaFilesCount >= 1 and javaFilesCount == javaTestFilesCount:
        return True
    return False


def IsTextJavaTestFile(text):

    lines = text.split('\n')
    testOccu = countMatchingString(Configurations.JavaTestMatching, lines[0])
    if testOccu >= 2:
        return True
    return False


def GetPomFiles(files):
    pomFiles = []
    for i, file in enumerate(files):
        if IsPomFile(file):
            filePath = join(basename(dirname(file)), basename(file))
            print(filePath)
            pomFiles.append((file, filePath))

    return pomFiles


def GetJavaFiles(files):
    javaFiles = []
    for i, file in enumerate(files):
        if IsJavaFile(file):
            filePath = join(basename(dirname(file)), basename(file))
            print(filePath)
            javaFiles.append((file, filePath))

    return javaFiles


def GetJavaTestFiles(files):
    javaTestFiles = []
    for i, file in enumerate(files):
        if IsJavaTestFile(file):
            filePath = join(basename(dirname(file)), basename(file))
            print(filePath)
            javaTestFiles.append((file, filePath))

    return javaTestFiles

def GetDiffsByType(files, destPath):
    fileTypes = [Configurations.FileTypeXML, Configurations.FileTypeJava, Configurations.FileTypeTest, Configurations.FileTypeXML]
    allFiles = []
    if not exists(destPath):
        makedirs(destPath)
    for i, file in enumerate(files):
        with open(file) as fobj:
            text = fobj.read()
            if not isOneFileChange(text):
                continue
            if IsTextPomFile(text):
                dest = CopyFileToNewDest(file, destPath, 'XML')
                allFiles.append((Configurations.FileTypeXML, file, dest))
            elif IsTextJavaFile(text):
                dest = CopyFileToNewDest(file, destPath, 'JAVA')
                allFiles.append((Configurations.FileTypeJava, file, dest))
            elif IsTextJavaTestFile(text):
                dest = CopyFileToNewDest(file, destPath, 'TEST')
                allFiles.append((Configurations.FileTypeTest, file, dest))

    return allFiles

def CopyFileToNewDest(file, destPath, type):
    filePath = join(basename(dirname(file)), basename(file))
    dest = join(destPath, type)
    if not exists(dirname(dest)):
        makedirs(dirname(dest))
    dest = join(dest, filePath)
    if not exists(dirname(dest)):
        makedirs(dirname(dest))
    copyfile(file, dest)
    return dest


def CopyFilesToNewDataset(files, destPath):
    if not exists(destPath):
        makedirs(destPath)
    for i, file in enumerate(files):
        dest = join(destPath, file[1])
        if not exists(dirname(dest)):
            makedirs(dirname(dest))
        copyfile(file[0], dest)



def GetFilesFromDatasetToNewLocation():
    print(GetFoldersInDatasetPath(Configurations.DatasetPath))
    folders = GetFoldersInDatasetPath(Configurations.DatasetPath)
    allFiles = []
    for i, folder in enumerate(folders):
        files = GetFilesInFolder(folder)
        allFiles.extend(files)

    allFilesWithPaths = GetDiffsByType(allFiles, Configurations.DestPath)

    resultFiles = join(Configurations.DestPath, 'files.txt')
    with open(resultFiles,"w+") as fobj:
        for file in allFilesWithPaths:
            fobj.write(file[0] + ' ' + file[1] + ' ' + '\n')


def GetOneLinersFromOneFileChanges():
    srcFolders = [Configurations.PomDestPath, Configurations.JavaTestDestPath]

    for fldr in srcFolders:
        dest = join(fldr, 'OneLine')
        allOneLiners = []
        if not exists(dirname(dest)):
            makedirs(dest)
        subFolders = GetFoldersInDatasetPath(fldr)
        for subFolder in subFolders:
            files = GetFilesInFolder(subFolder)
            for file in files:
                if isOneLineChange(file):
                    filePath = join(basename(dirname(file)), basename(file))
                    allOneLiners.append(file)
                    fileDest = join(dest, filePath)
                    if not exists(dirname(fileDest)):
                        makedirs(dirname(fileDest))
                    copyfile(file, fileDest)

        resultFiles = join(fldr, 'files.txt')
        with open(resultFiles, "w+") as fobj:
            for file in allOneLiners:
                fobj.write(file + ' ' + '\n')



GetOneLinersFromOneFileChanges()

