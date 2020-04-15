from anonBrowser import *
from bs4 import BeautifulSoup
import os, optparse, re

def printLinks(url):
    ab = anonBrowser()
    ab.anonymize()
    page = ab.open(url)
    html = page.read()
    try:
        print('[+] Printing Links From Regex')
        link_finder = re.compile('href="(.*?)"')
        links = link_finder.findall(html)
        for link in links:
            print(link)
    except Exception:
        pass
    try:
        print('\n[+] Printing Links From BeautifulSoup.')
        soup = BeautifulSoup(html)
        links = soup.findAll(name='a')
        for link in links:
            if link.has_key('href'):
                print(link['href'])
    except Exception:
        pass

def mirrorImages(url, dir):
    ab = anonBrowser()
    ab.anonymize()
    html = ab.open(url)
    soup = BeautifulSoup(html)
    image_tags = soup.findall('img')
    for image in image_tags:
        filename = image['src'].lstrip('https://')
        filename = os.path.join(dir, filename.replace('/', '_'))
        print('[+] Saving ' + str(filename))
        data = ab.open(image['src']).read()
        ab.back()
        save = open(filename, 'wb')
        save.write(data)
        save.close()

def main():
    parser = optparse.OptionParser('usage %prog -u <target url> -d <destination directory>')
    parser.add_option('-u', dest='tgtURL', type='string', help='specify target URL')
    parser.add_option('-d', dest='dir', type='string', help='specify destination directory')
    (options, args) = parser.parse_args()
    url = options.tgtURL
    dir = options.dir
    if url == None or dir == None:
        print(parser.usage)
        exit(0)
    else:
        try:
            printLinks(url)
            mirrorImages(url, dir)
        except Exception as e:
            print('[-] Error while scraping:')
            print('[-] ' + str(e))

if __name__ == '__main__':
    main()