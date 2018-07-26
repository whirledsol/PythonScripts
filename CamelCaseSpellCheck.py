import sys, re, collections, enchant

# Camel Case Spell Check
# Will Rhodes  07/01/2016
# Works with CamelCase and bumpyCase variables in a file. Also allows for accronyms in the variables like FOOBar. Untested but works with normal words too.
# How to use:
#	>cd to/directory/with/this/file
#	>python CamelCaseSpellCheck.py "Path/To/TextFile.txt"
def CamelCaseSpellCheck(filepath = None, wordRegex="[A-Za-z0-9]+"):
    
	if filepath is None:
		print("Please supply a file name.")
		return

	#we have a filename now
	contents = ReadFile(filepath)
    #print contents #DEBUG
    
    #get the words from the file
	words = re.findall(wordRegex,contents)
    
    #use enchant library to create a US based dictionary spell checker
	spellcheck = enchant.Dict("en_US")
    
    #go through words and print out errors
	print("\n\n##################  SPELLING ERRORS FOUND  #######################")
	for word in words:
    	#split up the word based on casing
		segments = SplitOnCaseChange(word)
    	#go through segments in each word
		for segment in segments:
    		#if it is not whitespace and is not spelled right, display it in a nicely formatted output
			if len(segment) > 0 and not spellcheck.check(segment):
				print("{0:<20s} {1:<10s} {2:<40s}".format(segment," in ", word))
	print("##################################################################\n\n")

#reads a file and returns all text as string
def ReadFile(filepath):
	with open(filepath) as f:
		content = f.read()
	return content

#this is where the magic happens, yo
def SplitOnCaseChange(word):
	#init
	segments = [] #the array housing the segments in the word
	currentlyUpper = False #the last i's case
	counter = 0 #counts the number of letters in each segment
	
	#clean up dat word
	word = word.strip() #oh myyyy
	#print word #DEBUG
	
	#go through each letter in the word
	for i in range(0,len(word)):
		#not the first character
		if i != 0:
			if (not currentlyUpper and word[i].isupper()):
				#lower/number  to upper case change
				segment = word[i-counter:i]
				segments.append(segment)
				counter = 0
			if (currentlyUpper and not word[i].isupper()):
				#upper to lower case change but only if we have accronyms
				if counter > 1:
					segment = word[i-counter:i-1]
					segments.append(segment)
					counter = 1 #important, we are splitting one character back
		#do the below every time
		counter += 1
		currentlyUpper = word[i].isupper()
	#when done, dump the remainder of the word in the segments
	segments.append(word[len(word)-counter:])

	#bye, bye
	return segments




#Always needed to call a function from >python filename.py. Passes the one argument supplied
if __name__ == "__main__":
    CamelCaseSpellCheck(sys.argv[1])