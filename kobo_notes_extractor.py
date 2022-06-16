import sqlite3,json,re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup,Tag


class Bookmark:
	def __init__(self,item):
		self.BookmarkID = item[0]
		self.VolumeID = item[1]
		self.ContentID= item[2]
		self.StartContainerPath= item[3]
		self.StartContainerChildIndex = item[4]
		self.StartOffset = item[5]
		self.EndContainerPath = item[6]
		self.EndContainerChildIndex = item[7]
		self.EndOffset = item[8]
		self.Text = item[9]
		self.Annotation = item[10]
		self.ExtraAnnotationData = item[11]
		self.DateCreated= item[12]
		self.ChapterProgress= item[13]
		self.Hidden= item[14]
		self.Version= item[15]
		self.DateModified= item[16]
		self.Creator= item[17]
		self.UUID= item[18]
		self.UserID= item[19]
		self.SyncTime= item[20]
		self.Published = item[21]
		self.ContextString= item[22]
		self.Type= item[23]
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def main():
	PATH_IN_SQLITE = "C:\\\\Users\\astro\\Documents\\KoboReader.sqlite"
	PATH_OUT_HTML = './out/bodies_of_water_comments_wer.html'
	TITLE_LIKE = 'Bodies of Water'
	PATH_IN_EPUB= "C:\\\\Users\\astro\\Calibre Library\\Alex Pendragon (draft)\\Bodies of Water (123)\Bodies of Water - Alex Pendragon (draft).epub"

	#connection to db
	con = sqlite3.connect(PATH_IN_SQLITE)
	cur = con.cursor()
	
	contentId = get_content_id(cur,TITLE_LIKE)
	print(f"Found content Id {contentId}")

	bookmarks = get_content_bookmarks(cur,contentId)
	print(f"Found {len(bookmarks)} bookmarks")
	#print(bookmarks[0].toJSON())

	soup = epub_to_soup(PATH_IN_EPUB,True)
	
	#add marks in reverse order so location-finding works
	for bookmark in bookmarks:
		soup = insert_bookmark(soup,bookmark)
		pass


	#add bootstrap
	soup = add_bootstrap(soup)

	#write
	write_html(soup.prettify(),PATH_OUT_HTML)



def get_content_id(cur,titleLike):
	'''
	lookup for contentID
	'''
	content = cur.execute("select ContentID from content WHERE Title=:titleLike",{"titleLike":titleLike}).fetchone()
	return content[0]

def get_content_bookmarks(cur,ContentID):
	'''
	Finds and ORMs all bookmarks for supplied content ID with the weirdness that the volumeID is the contentID
	'''
	rows = cur.execute("select * from Bookmark WHERE VolumeID=:ContentID ORDER BY DateCreated desc",{"ContentID":ContentID}).fetchall()
	return [Bookmark(x) for x in rows]


def epub_to_html(path):
	'''
	epub to html
	'''
	book = epub.read_epub(path)
	chapters = []   
	for item in book.get_items():        
		if item.get_type() in [ebooklib.ITEM_DOCUMENT]:
			clean = item.get_content().decode("utf-8")
			chapters.append(clean)
	return ''.join(chapters)


def epub_to_soup(path,removeCover=False):
	'''
	epub to soup
	'''	
	html = epub_to_html(path)
	soup = BeautifulSoup(html, 'html.parser')
	if removeCover:
		soup.find('html').extract()
	return soup


def add_bootstrap(soup):
	bootstrap = '''
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
	<style>body{margin:0 10%;}</style>
	'''
	bootstrap = BeautifulSoup(bootstrap, 'html.parser')
	
	soup.head.append(bootstrap)

	popoverEnable = '''<script>
	var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
	var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
	return new bootstrap.Popover(popoverTriggerEl)
	})</script>
	'''
	popoverEnable = BeautifulSoup(popoverEnable, 'html.parser')
	soup.find_all('body')[-1].append(popoverEnable)
	return soup


def insert_bookmark(soup,bookmark):
	'''
	insert bookmark
	'''
	#print(bookmark.Text)
	coordinatesStart = get_point_coordinates(bookmark.StartContainerPath)
	coordinatesEnd = get_point_coordinates(bookmark.EndContainerPath)
	tag = get_bookmark_tag(soup,bookmark)
	if(coordinatesStart[1] == coordinatesEnd[1]):
		soup = inject_tag(soup,coordinatesStart,coordinatesEnd,tag)
	else:
		soup = wrap_tag(soup,coordinatesStart,coordinatesEnd,tag)
	
	print('\n\n')
	return soup

def locate_tag(soup,documentIndex,index):
	'''
	locates the tag
	'''
	document = soup.find_all('body')[documentIndex]
	
	documentElements = list(document.children)
	tag = documentElements[index]
	
	if(not isinstance(tag,Tag)):
		print('not instance')
		#tag = tag.parent

	if tag.string is None:
		tag.string = ""
	return tag

def wrap_tag(soup,coordinatesStart,coordinatesEnd,tag):
	'''
	wraps multiple elements
	'''
	documentIndex, indexStart, charStart = coordinatesStart
	_,indexEnd,charEnd = coordinatesEnd
	for i in range(indexStart-1,indexEnd):
		line = locate_tag(soup,documentIndex,i)
		tag['class'] = 'd-block bg-warning'
		line.wrap(tag)
	return soup

def inject_tag(soup,coordinatesStart,coordinatesEnd,tag):
	'''
	wraps text within element
	'''
	documentIndex, index, charStart = coordinatesStart
	_,_,charEnd = coordinatesEnd
	
	line = locate_tag(soup,documentIndex,index)

	print(type(line))

	start = line.string[:charStart] or ""
	middle = line.string[charStart:charEnd] or ""
	end = line.string[charEnd:] or ""

	tag.string = middle

	line.string = start
	line.append(tag)
	line.append(end)
	return soup


def get_point_coordinates(containerPath):
	'''
	parses the vital coordinates based on the containerPath
	'''
	pattern = r"^(.+)#.*\((.*)\)$"
	matches = re.search(pattern,containerPath)
	#nodes = [int(x) for x in matches.group(2).split('/')]
	document = matches.group(1)
	components = matches.group(2).split('/')
	index = components[-2]
	chars = components[-1].split(':')
	index = int(index if len(components) == 5 else chars[0]) #sometimes the index is in the last section
	index += -2 #not zero indexed?

	#BUSINESS LOGIC HERE
	documentIndexes = {
		"index_split_000.html":0,
		"index_split_001.html":1
	}
	documentIndex = documentIndexes[document]

	#aparently this is just the last one?
	chars = int(chars[-1])

	return [documentIndex,index,chars]


def get_bookmark_tag(soup, bookmark):
	annotation = bookmark.Text.replace("\"","\\\'")
	tag = soup.new_tag('a')
	tag["class"] ="bg-warning"
	tag["data-bs-toggle"] ="popover"
	tag["title"] = bookmark.BookmarkID
	tag["data-bs-content"] = annotation
	return tag



def write_html(html,out):
	f = open(out,'w')
	f.write(html)
	f.close()



if __name__ == '__main__': main()