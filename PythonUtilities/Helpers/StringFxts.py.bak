"""
String Functions
@author: Will Rhodes
"""

# returns a list of text found in between "beg" and "end" of large text "string." 
def getTextInBetween(string,beg,end):
    results = []
    
    while beg in string:
        begIndex = string.find(beg)
        string = string[begIndex+len(beg):len(string)]
        
        if string.find(beg)<string.find(end) and string.find(beg)>0:
            cutAt = beg
        else:
            if string.find(end) >0:
                cutAt = end
            else:
                print "Done early"
                break
        extraction,string = (string[0:string.find(cutAt)],string[string.find(cutAt):len(string)])
        results.append(extraction)        
        #print extraction,string
	return results
	
