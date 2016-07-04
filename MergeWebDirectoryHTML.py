# -*- coding: utf-8 -*-
"""
Merge Web Directory to HTML
merges the HTML from subdirectories on a root website and places them into a txt document
Created on Wed Oct 23 15:50:55 2013
@author: Will Rhodes
"""
import urllib2
def start():
    root = "http://www.website.com/website/"
    subdirs = ["page1.html","page2.html","page3.html"]
    subdirs = sorted(subdirs)
    
    contents = []
    for each in subdirs:
        subdir = root+each
        thishtml = readPage(subdir)
        contents.append(thishtml)
    #writeMerged(contents)   
    writeMergedText(contents) 
    
    
def readPage(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
    except:
        print "ERROR downloading ",url
        exit()
    #print "HERE IT COMES"
    #print html
    return html
    
def writeMergedText(contents,outputFilePath = "mergedhtml.html"):
    
    merged = "<html><body>"
    for each in contents:
        merged +=each
        merged +="<br><hl><br>"
    merged += "</body></html>"
    
    output = open(outputFilePath,"wb")
    output.write(merged)       
    
    
def writeMerged(contents,outputFilePath = "mergedhtml.html"):
    merged = ""
    header = contents[0]
    header = header[0:header.index("<BODY")]
    merged = merged+header
    for i in range(len(contents)):
        fullPage = contents[i]
        try:
            parsedPage = fullPage[fullPage.index("<BODY"):fullPage.rindex("</BODY>")]
            parsedPage = parsedPage[parsedPage.index(">")+1:len(parsedPage)]            
            merged += parsedPage
        except:
            print "ERROR"
            print i
            
         
    merged +="</BODY></HTML>"    
    
    output = open(outputFilePath,"wb")
    output.write(merged)
    
        
    
    
if  __name__ =='__main__':start()