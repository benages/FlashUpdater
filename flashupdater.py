import requests
import shutil
import tarfile
import re


Directory = "/usr/lib/flashplugin-nonfree/"
Archive = "install_flash_player_11_linux.x86_64.tar.gz"


def DownloadFlash():
    URL = "https://fpdownload.macromedia.com/get/flashplayer/current/licensing/linux/install_flash_player_11_linux.x86_64.tar.gz"
    r = requests.get(URL, stream = True)
    with open(Directory + Archive, 'wb') as f:
        shutil.copyfileobj(r.raw, f)


def ExtractFile():
    Filename = "libflashplayer.so"
    with tarfile.open(Archive,'r') as f:
        a = f.extractfile("libflashplayer.so")
        with open(Directory + Filename, 'wb') as g:
            shutil.copyfileobj(a,g)
        a = f.extractfile("readme.txt")
        with open(Directory+"readme.txt", 'wb') as g:
            shutil.copyfileobj(a, g)

def CheckInstalledVersion():
    with open(Directory + "readme.txt", 'r') as f:
        a = f.read()
        p = re.compile('11.2.\d\d\d.\d\d\d')
        return p.findall(a)[0]

def CheckUpstreamVersion():
    URL = "https://get.adobe.com/flashplayer/"
    UserAgent = {'User-agent': 'Mozilla/5.0 (X11; Linux $arch; rv:45.0) Gecko/20100101 Firefox/45.0'}
    r = requests.get(URL, headers = UserAgent)
    p = re.compile('11.2.\d\d\d.\d\d\d')
    return p.findall(r.text)[0]

def main():
    if CheckUpstreamVersion() > CheckInstalledVersion():
        print('Downloading flash...')
        DownloadFlash()
        ExtractFile()
    elif CheckUpstreamVersion() == CheckInstalledVersion():
        print('Your flash version is the latest')
    else:
        print('There is a big problem. Your flash version is newer than the latest from Adobe')


if __name__ == '__main__':
        raise SystemExit(main())



