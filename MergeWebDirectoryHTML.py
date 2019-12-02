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
    root = "https://www.nifty.org/nifty/gay/sf-fantasy/aquata-cove/"
    subdirs = ["epilogue-2","epilogue-1","aquata-cove-101","aquata-cove-100","aquata-cove-99","aquata-cove-98","aquata-cove-97","aquata-cove-96","aquata-cove-95","aquata-cove-94","aquata-cove-93","aquata-cove-92","aquata-cove-91","aquata-cove-90","aquata-cove-89","aquata-cove-88","aquata-cove-87","aquata-cove-86","aquata-cove-85","aquata-cove-84","aquata-cove-83","aquata-cove-82","aquata-cove-81","aquata-cove-80","aquata-cove-79","aquata-cove-78","aquata-cove-77","aquata-cove-76","aquata-cove-75","aquata-cove-74","aquata-cove-73","aquata-cove-72","aquata-cove-71","aquata-cove-70","aquata-cove-69","aquata-cove-68","aquata-cove-67","aquata-cove-66","aquata-cove-65","aquata-cove-64","aquata-cove-63","aquata-cove-62","aquata-cove-61","aquata-cove-60","aquata-cove-59","aquata-cove-58","aquata-cove-57","aquata-cove-56","aquata-cove-55","aquata-cove-54","aquata-cove-53","aquata-cove-52","aquata-cove-51","aquata-cove-50","aquata-cove-49","aquata-cove-48","aquata-cove-47","aquata-cove-46","aquata-cove-45","aquata-cove-44","aquata-cove-43","aquata-cove-42","aquata-cove-41","aquata-cove-40","aquata-cove-39","aquata-cove-38","aquata-cove-37","aquata-cove-36","aquata-cove-35","aquata-cove-34","aquata-cove-33","aquata-cove-32","aquata-cove-31","aquata-cove-30","aquata-cove-29","aquata-cove-28","aquata-cove-27","aquata-cove-26","aquata-cove-25","aquata-cove-24","aquata-cove-23","aquata-cove-22","aquata-cove-21","aquata-cove-20","aquata-cove-19","aquata-cove-18","aquata-cove-17","aquata-cove-16","aquata-cove-15","aquata-cove-14","aquata-cove-13","aquata-cove-12","aquata-cove-11","aquata-cove-10","aquata-cove-9","aquata-cove-8","aquata-cove-7","aquata-cove-6","aquata-cove-5","aquata-cove-4","aquata-cove-3","aquata-cove-2","aquata-cove-1"]
    seperator = "<br><hl><br>"
    filterSelector = "body"
    contents = []
    outputFilePath = "mergedhtml.html"

    #subdirs = sorted(subdirs)
    subdirs.reverse()
    for each in subdirs:
        subdir = root+each
        content = readPage(subdir)
        #content = filterContent(content,filterSelector,seperator)
        content = str(content)
        contents.append(content)
    writeMergedText(contents,outputFilePath,seperator) 

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

def readPage(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
        con = urllib.request.urlopen( req )
        html = con.read()
    except Exception as e:
        print("ERROR downloading ",url, str(e))
        exit()
    #print "HERE IT COMES"
    #print html
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
    filtered = [x.get_text() for x in filtered]
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