#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge Web Directory to HTML
merges the HTML from subdirectories on a root website and places them into a txt document
Created on Wed Oct 23 15:50:55 2013
@author: Will Rhodes
"""
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup

def start():
    root = "https://www.springfieldspringfield.co.uk/view_episode_scripts.php?tv-show=battlestar-galactica&"
    subdirs = ['episode=s01e01','episode=s01e02','episode=s01e03','episode=s01e04','episode=s01e05','episode=s01e06','episode=s01e07','episode=s01e08','episode=s01e09','episode=s01e10','episode=s01e11','episode=s01e12','episode=s01e13','episode=s02e01','episode=s02e02','episode=s02e03','episode=s02e04','episode=s02e05','episode=s02e06','episode=s02e07','episode=s02e08','episode=s02e09','episode=s02e10','episode=s02e11','episode=s02e12','episode=s02e13','episode=s02e14','episode=s02e15','episode=s02e16','episode=s02e17','episode=s02e18','episode=s02e19','episode=s02e20','episode=s03e01','episode=s03e02','episode=s03e03','episode=s03e04','episode=s03e05','episode=s03e06','episode=s03e07','episode=s03e08','episode=s03e09','episode=s03e10','episode=s03e11','episode=s03e12','episode=s03e13','episode=s03e14','episode=s03e15','episode=s03e16','episode=s03e17','episode=s03e18','episode=s03e19','episode=s03e20','episode=s04e01','episode=s04e02','episode=s04e03','episode=s04e04','episode=s04e05','episode=s04e06','episode=s04e07','episode=s04e08','episode=s04e09','episode=s04e10','episode=s04e11','episode=s04e12','episode=s04e13','episode=s04e14','episode=s04e15','episode=s04e16','episode=s04e17','episode=s04e18','episode=s04e19']
    seperator = "<br><br>"
    filterSelector = ".scrolling-script-container"
    contents = []
    outputFilePath = "battlestar_scripts.html"

    #subdirs = sorted(subdirs)
    #subdirs.reverse()

    for i,each in enumerate(subdirs):
        print('{0:.2f}%'.format(i/len(subdirs)*100))
        subdir = root+each
        content = readPage(subdir)
        content = filterContent(content,filterSelector,seperator)
        content = str(content)
        contents.append(content)
    writeMergedText(contents,outputFilePath,seperator) 

'''
def startFollow():
    url = "https://www.wattpad.com/569784435-a-forbidden-magic-chapter-1"
    followViaSelector = "a.next-part-link"
    seperator = "<br><hl><br>"
    filterSelector = ".panel-reading"
    contents = []
    outputFilePath = "mergedhtml.html"
    maxPages = 100
    page = 1
    while page <= maxPages and url is not None:
        thishtml = readPage(url)
        content = filterContent(thishtml,filterSelector,seperator)
        contents.append(content)
        url = findHref(thishtml,followViaSelector)
        page = page + 1

    writeMergedText(contents,outputFilePath,seperator) 

'''

def readPage(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
        con = urllib.request.urlopen( req )
        html = con.read()
    except Exception as e:
        print("ERROR downloading ",url, str(e))
        exit()
    return html
    
def findHref(html,selector):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.select(selector)
    print("link",link)
    if len(link) == 0:
        return None
    return link[0]["href"]

def filterContent(html, selector, seperator):
    soup = BeautifulSoup(html, 'html.parser')
    filtered = soup.select(selector)
    filtered = [x.prettify() for x in filtered]
    return seperator.join(filtered)
    
def writeMergedText(contents, outputFilePath, seperator):
    merged = "<html><body>"
    for each in contents:
        merged +=each
        merged += seperator
    merged += "</body></html>"
    
    output = open(outputFilePath,"w")
    output.write(merged)       
    

if  __name__ =='__main__':start()
