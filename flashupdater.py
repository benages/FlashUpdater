#!/usr/bin/python3

import requests
import shutil
import tarfile
import re

Directory = "/usr/lib/flashplugin-nonfree/"
Archive = "install_flash_player_11_linux.x86_64.tar.gz"

def DownloadFlash(Version):
    URL = "https://fpdownload.adobe.com/get/flashplayer/pdc/%s/flash_player_npapi_linux.x86_64.tar.gz" % Version
    r = requests.get(URL, stream = True)
    if r.status_code == 404:
        exit("No se encuenta el flash")
    with open(Directory + Archive, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

def ExtractFile():
    Filename = "libflashplayer.so"
    with tarfile.open(Directory+Archive,'r') as f:
        a = f.extractfile("libflashplayer.so")
        with open(Directory + Filename, 'wb') as g:
            shutil.copyfileobj(a,g)
        a = f.extractfile("readme.txt")
        with open(Directory+"readme.txt", 'wb') as g:
            shutil.copyfileobj(a, g)


def CheckInstalledVersion():
    try:
        with open(Directory + "readme.txt", 'r') as f:
            a = f.read()
            p = re.compile('2\d.0.\d.\d\d\d')
            return p.findall(a)[0]
    except FileNotFoundError:
        return '11.2.000.001'

def CheckUpstreamVersion():
    URL = "https://get.adobe.com/flashplayer/"
    UserAgent = {'User-agent': 'Mozilla/5.0 (X11; Linux $arch; rv:45.0) Gecko/20100101 Firefox/45.0'}
    r = requests.get(URL, headers = UserAgent)
    p = re.compile('2\d.0.\d.\d\d\d')
    return p.findall(r.text)[0]

def main():
    UpstreamVersion = CheckUpstreamVersion()
    if UpstreamVersion > CheckInstalledVersion():
        print('Downloading flash...')
        DownloadFlash(UpstreamVersion)
        ExtractFile()
    elif CheckUpstreamVersion() == CheckInstalledVersion():
        print('Your flash version is the latest')
    else:
        print('There is a big problem. Your flash version is newer than the latest from Adobe')

if __name__ == '__main__':
        raise SystemExit(main())