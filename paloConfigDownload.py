#!/usr/bin/python3

import os
import datetime
import urllib.request
import ssl
from slackclient import SlackClient

sc = SlackClient("slack_api_token_change_me")
slackchannel = "Change_me"
retentionTime = 2629743  # 1 Month




def main():
    '''
    Disable SSL check
    '''
    if (not os.environ.get('PYTHONHTTPSVERIFY', '')
        and getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context


    configFile, currentDir = findPath()
    paloDict = findPaloAPI(configFile)

    for paloName, paloApi in paloDict.items():
        downloadXMLConfig(paloName, paloApi, currentDir)

    if currentDir:
        filesRemove = cleanUpXMLFiles(currentDir)
        for file in filesRemove:
            print("File removed: {}".format(file))


def findPath():
    currentDir = os.path.dirname(os.path.realpath(__file__))
    configPath = currentDir + "/paloConfigDownload.conf"

    try:
        configFile = open(configPath, "r")
    except IOError:
        print("Error: File paloConfigDownload.conf does not appear to exist.")
        os._exit(0)
    else:
        return(configFile, currentDir)


def findPaloAPI(configFile):
    paloDict = {}
    if configFile.mode == 'r':
        context = configFile.readlines()
        for line in context:
            line = line.rstrip('\n')
            if not line.startswith('#'):
                paloName, paloAPI = line.split(",")
                paloDict[paloName] = paloAPI
                # downloadXMLConfig(line)
                # print(line)
        # cleanUpXMLFiles(currentDir)
        return(paloDict)


def downloadXMLConfig(paloName, paloApi, currentDir):
    dateToday = (datetime.datetime.now().strftime('%d-%m-%Y'))
    datetime.datetime
    # urlPaloXML ="https://www.google.nl"
    for port in (443, 4443):
        urlPaloXML = "https://{}:{}/api/?type=export&category=configuration&key={}".format(
            paloName, port, paloApi)
        try:
            urllib.request.urlretrieve(
                urlPaloXML,
                currentDir + "/backup/{}_{}.xml".format(paloName, dateToday))
            slacknotification(paloName)
            break
        except:
            print("Failed to download configuration file")


def slacknotification(paloName):
    if sc != "slack_api_token_change_me":
        sc.api_call(
            "chat.postMessage",
            channel=slackchannel,
            text="Download config file from: {}".format(paloName),
            user="PythonScript")


def cleanUpXMLFiles(currentDir):
    currentTimestamp = datetime.datetime.now().timestamp()
    backupFileList = os.listdir(currentDir + "/backup")
    filesRemove = []

    if not os.path.exists(currentDir + "/backup"):
        os.mkdir(currentDir + "/backup")

    for files in backupFileList:
        backupFullFilePath = str(os.path.join(currentDir + "/backup", files))
        timestampFileCreated = os.stat(backupFullFilePath).st_mtime
        if retentionTime <= (currentTimestamp - timestampFileCreated):
            print(currentTimestamp - timestampFileCreated)
            os.remove(backupFullFilePath)
            filesRemove.append(files)
    return(filesRemove)


if __name__ == '__main__':
    main()
