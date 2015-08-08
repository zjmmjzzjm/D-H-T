# coding: utf-8
import urllib
from datetime import *
import datetime
import os
import getopt
import sys
import threading
import signal
import time
import re

def ctrlCSignalHandler(signal, frame):
    global conf
    print("=============>Get Ctrl C interrupt===============")
    conf.bExit = True

downloadDir = "download"
downloadTxtDir = downloadDir + "/txt/"
downloadTorrentDir = downloadDir + "/torrent/"

max_threads = 5


startday = date(2015, 8, 1)
#startday = date(2014,6,1)


def makeUrl(i, start=startday):
    delta = datetime.timedelta(days=i)
    date1 = start + delta
    str1 = date1.strftime("%Y%m%d") + ".txt"
    return str1


def reporthook(blocks_read, block_size, total_size):
    if not blocks_read:
        print("Connection opened")
        return
    if total_size < 0:
        print("Read %d blocks (%d bytes)" % (blocks_read, blocks_read * block_size))
    else:
        amount_read = blocks_read * block_size
        print("Read %d blocks,  %d/%d, %.0f%%" % (blocks_read, amount_read, total_size, amount_read*100.0/(total_size)))
    return


def download(filename):
    savefile = downloadTxtDir + filename
    if os.path.exists(savefile):
        return
    _url = "http://torrage.com/sync/" + filename
    urllib.urlretrieve(_url, savefile, reporthook)


#download()
#def initProxy():
#    proxy = {"http": "127.0.0.1:10000"}
#    proxyhandle = urllib.request.ProxyHandler(proxy)
#    opener = urllib.request.build_opener(proxyhandle)
#    urllib.request.install_opener(opener)


def downloadTorrent(txtFileName):
    global conf
    global stats
    f = open(downloadTxtDir + txtFileName, 'r').readlines()
    torrentDir = downloadTorrentDir + txtFileName.split('.')[0] + "/"
    if not os.path.isdir(torrentDir):
        os.mkdir(torrentDir)

    for item in f:
        if conf.bExit:
            return

        item = item.strip("\r\n")
        _saveTorrentName = torrentDir + item + ".zip"
        if os.path.exists(_saveTorrentName):
            continue
        url = "http://torrage.com/torrent/" + item.upper() + ".torrent"
        print("downloading torrent url:" + url + " Save: " + _saveTorrentName)
        try:
            _content = urllib.request.urlopen(url).read()
            stats.totalBytes = stats.totalBytes + len(_content)
            open(_saveTorrentName, "wb").write(_content)
        except KeyboardInterrupt as e:
            print("Keyboard interupted" + str(e))
            conf.bExit = True
        except:
            print("download torrent failed")
            continue


def prepareDirs():
    if not os.path.isdir(downloadDir):
        os.mkdir(downloadDir)
    if not os.path.isdir(downloadTxtDir):
        os.mkdir(downloadTxtDir)
    if not os.path.isdir(downloadTorrentDir):
        os.mkdir(downloadTorrentDir)


def threadFunc(thread_index):

    datenow = date.today()
    delta = datenow - startday
    global downloadingSet
    global lock
    global conf

    for i in range(0, delta.days, 1):
        try:
            if conf.bExit:
                return
            if i%max_threads == thread_index:
                continue
            fn = makeUrl(i)
            if conf.downUrl:
                download(fn)
                print("=====>downloading  torrent list" + fn)
            if conf.downTorrent:
                downloadTorrent(fn)
        except KeyboardInterrupt as e:
            print("Keyboard interupted" + str(e))
            conf.bExit = True
        except:
            print("downLoad failed... continue next")
            continue

def getdirsize(dir):
   size = 0
   for root, dirs, files in os.walk(dir):
      size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
   return size

def get_last_uncompressed_date():
    lines = open("download/torrent/pack.log", "rt").readlines()
    timestr = None
    for l in lines[::-1]:
        m =re.match(r"(\d*).*(compress)", l)
        if m :
            timestr = m.group(1)
            break

    if timestr is None:
        timestr = "20190101"
    b = time.strptime(timestr,"%Y%m%d")
    #time.struct_time(tm_year=2013, tm_mon=12, tm_mday=18, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=352, tm_isdst=-1)
    return b
def doPack():
    global conf

    sevenZ = "\"C:\\Program Files\\7-Zip\\7z.exe\" "

    archiveSizeLimite = 3.8 * 1024 * 1024 * 1024
    archive = sevenZ + " a -t7z -mx0 -pz55j75m315 "
    if conf.bPack is False:
        return
    #datenow = date.today()
    #最后四个还没下完，不打包
    #startday = date(2013, 11, 28)
    timestruct = get_last_uncompressed_date()
    startday = date(timestruct.tm_year, timestruct.tm_mon, timestruct.tm_mday)
    endday = date.today()
    print(endday)
    delta = endday - startday

    global downloadTorrentDir
    curDir = os.getcwd()
    print("old dir is ", curDir)
    os.chdir(downloadTorrentDir)
    log = open("pack.log", "a")
    packSize = 0
    dirNameList = []
    for i in range(0, delta.days - 4, 1):
        dirName = makeUrl(i, startday)[0: -4]
        if not os.path.isdir(dirName):
            print(dirName + "is not dir")
            continue
        print("getting dir size... " + dirName)
        dirSize = getdirsize(dirName)
        print("dirname is %s dirsize is %d" % (dirName, dirSize))
        if packSize + dirSize > archiveSizeLimite:
            totalArchiveCmd = archive
            if packSize > archiveSizeLimite:
                totalArchiveCmd += " -v3g "
            targetArchiveName = "torrent" + dirNameList[0] + "_" + dirNameList[-1]
            totalArchiveCmd += targetArchiveName + " "
            for tempDir in dirNameList:
                totalArchiveCmd += tempDir + " "
            log.write("%s, compress: %s\n" % (dirName, totalArchiveCmd))
            log.flush()
            print("Finally Archive cmd is " + totalArchiveCmd)
            print("begin archive" + totalArchiveCmd)
            os.system(totalArchiveCmd)
            print("finish archive")
            packSize = dirSize
            dirNameList = [dirName]
        else:
            packSize += dirSize
            dirNameList.append(dirName)
            log.write("%s, size: %s, total: %s\n" % (dirName, dirSize, packSize))
            log.flush()
    log.close()
    os.chdir(curDir)


def InitSignal():
    signal.signal(signal.SIGINT, ctrlCSignalHandler)
    signal.signal(signal.SIGTERM, ctrlCSignalHandler)


def doWork():
    global conf
   # if conf.downTorrent:
   #     initProxy()
    prepareDirs()
    InitSignal()
    threads = []
    for i in range(max_threads):
        threads.append(threading.Thread(target=threadFunc, args=(i,)))
    print("begin threads num " + str(len(threads)))
    for t in threads:
        t.start()

    while conf.bExit is False:
        try:
            print("total bytes " + str(stats.totalBytes) +  " total time" + str(stats.totalTime) + " average speed is " + str(stats.totalBytes/stats.totalTime))
            time.sleep(2)
        except:
            continue
    while True:
        isAlive = False
        try:
            time.sleep(2)
        except:
            continue
        finally:
            for t in threads:
                #t.join()
                isAlive = isAlive or t.is_alive()
            if not isAlive:
                break
    print("exit!!!!1")


class Conf:
    def __init__(self):
        self.downUrl = True
        self.downTorrent = False
        self.bExit = False
        self.bPack = False


class Stats:
    def __init__(self):
        self.totalBytes = 0
        self.totalTime = 0


if __name__ == "__main__":
    opts,args = getopt.getopt(sys.argv[1:], "utap", ["url","torrent", "all","pack"]);
    conf = Conf()
    stats = Stats()

    for o, a in opts:
        if o in ("-u", "--url"):
            conf.downUrl = True
        elif o in ("-t", "--torrent"):
            conf.downTorrent = True
        elif o in ("-a", "--all"):
            conf.downUrl = True
            conf.downTorrent = True
        elif o in ("-p", "--pack"):
            conf.bPack = True
        else:
            conf.downUrl = True
            conf.downTorrent = False
            print("downloadUrl{0:s} downloadTorrent {1:s} ".format(conf.downUrl, conf.downTorrent))

    downloadingSet = {1}
    lock = threading.Lock()

    startSeconds = time.time()
    if conf.bPack:
        doPack()
    else:
        doWork()

    stats.totalTime = time.time() - startSeconds
    print("total bytes {} total time {} average speed is {}".format(stats.totalBytes, stats.totalTime, stats.totalBytes/stats.totalTime))



