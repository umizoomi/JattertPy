from lxml.html import soupparser
import os
import requests
import urllib
from google import search
from django.utils.http import urlquote

def get_foldername(url):
    split = url.split('/')[:-1]
    return '/'.join(split)

def baseurl(url):
    """
    Get the base URL from an arbitrary URL
    http://www.example.com/page/2390 -> http://www.example.com
    Does not work without protocol (http://).
    """
    split = url.split('/')[:3]
    return '/'.join(split) 


#url = "http://www.suara-jawa.sr/Myjukebox_Jones_S-02/myjukebox.xml"

henk = 0
for url in search('site:suara-jawa.sr disableclicktoactiveprompt="false"', stop=200):
    henk = henk + 1
    print "--- (%d) %s ---" % (henk, url)
    domain = baseurl(url)
    r = requests.get(url)
    root = soupparser.fromstring(r.content)
    nodes = root.xpath('//node[@file]')
    filenames = map(lambda x: x.get('file'), nodes)

    foldername = get_foldername(url)

    mp3_urls_quoted = map(lambda x: "%s/%s" % (foldername, urlquote(x)), filenames)
    mp3_urls = map(lambda x: "%s/%s" % (foldername, x), filenames)
	
    for i in xrange(len(mp3_urls)): # NOTE: same as len(filenames)
        relpath = mp3_urls[i][len(domain) + 1:]
        relpath = relpath.replace('Myjukebox_', '')
        relpath = relpath.replace('/myjukebox_files', '')
        parent_folders = '/'.join(relpath.split('/')[:-1])
        
        if os.path.exists(relpath):
            continue
        if not os.path.exists(parent_folders):
            os.makedirs(parent_folders)

        print 'GET', mp3_urls[i]
		
        urllib.urlretrieve(mp3_urls_quoted[i], relpath)