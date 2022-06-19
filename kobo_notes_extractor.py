import sqlite3,json,re,traceback
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup,Tag,NavigableString


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
	soup = add_navigation(soup)
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
	[x.extract() for x in soup.find_all('a')]
	if removeCover:
		soup.find('html').extract()
	return soup


def add_bootstrap(soup):
	bootstrap = '''
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
	<style>body{width:900px; margin:5rem auto;}</style>
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


def add_navigation(soup):
	'''
	adds navigation pane
	'''
	navigation = '''
	<div class="bg-light fixed-top w-100 p-2 text-end">
	<span id="annotation-current"></span>
	<button type="button" id="btn-prev" class="btn btn-sm btn-outline-dark">Previous</button>
	<button type="button" id="btn-next" class="btn btn-sm  btn-outline-primary">Next</button>
	</div>
	<script>
		var annotationIndex = -1;
		const annotations = Array.from(document.querySelectorAll('.kne-annotation'));

		annotations.map((el,i)=>{
			
			el.onclick = (e)=>{
				navigate(i);
			}
		});

		const navigate = (newIndex) =>{
			annotationIndex = newIndex;
			annotationIndex = annotationIndex < 0 ? annotations.length-1 : annotationIndex;
			annotationIndex = annotationIndex >= annotations.length ? 0 : annotationIndex;
			
			const el = annotations[annotationIndex];
			console.log('annotationIndex',annotationIndex,el);

			document.getElementById('annotation-current').innerText = el.dataset.title; //bs is hiding title
			
			const y = el.getBoundingClientRect().top + window.scrollY - 50;
			window.scroll({
				top: y,
				behavior: 'smooth'
			});
		};

		document.getElementById('btn-prev').onclick = _=>{
			navigate(annotationIndex-1)
		};

		document.getElementById('btn-next').onclick = _=>{
			navigate(annotationIndex+1)
		};
	</script>
	'''
	navigation = BeautifulSoup(navigation, 'html.parser')
	soup.find_all('body')[-1].append(navigation)
	return soup


def insert_bookmark(soup,bookmark):
	'''
	insert bookmark
	'''
	#print(bookmark.BookmarkID)
	try:
		coordinatesStart = get_point_coordinates(bookmark.StartContainerPath)
		coordinatesEnd = get_point_coordinates(bookmark.EndContainerPath)
		
		if(coordinatesStart is None or coordinatesEnd is None):
			return soup

		popover = get_bookmark_tag(soup,bookmark)
		
		if(coordinatesStart[1] == coordinatesEnd[1]):
			soup = inject_popover(soup,coordinatesStart,coordinatesEnd,popover)
		else:
			soup = wrap_popover(soup,coordinatesStart,coordinatesEnd,popover)
	except Exception as e:
		print(f"\n ERROR INSERTING BOOKMARK {bookmark.BookmarkID}")
		print(bookmark.toJSON())
		print(traceback.format_exc())
		
	return soup


def locate_content(soup,documentIndex,index):
	'''
	locates the tag
	'''
	document = soup.find_all('body')[documentIndex]
	
	documentElements = list(document.children)
	content = documentElements[index]


	if(len(str(content).strip()) == 0):
		#we are in a liminal space, take heed, move back one
		#content = content.next_sibling
		raise "fix this"
		print('No content. Using next sibling.')
		pass

	if content.string is None:
		content.string = ""
	return content


def wrap_popover(soup,coordinatesStart,coordinatesEnd,popover):
	'''
	wraps multiple elements
	'''
	#print('\twrap')
	documentIndex, indexStart, charStart = coordinatesStart
	_,indexEnd,charEnd = coordinatesEnd
	'''
	#creates multiple wrappers and just doesn't work well enough
	for i in range(0,indexEnd-indexStart+1):
		content = locate_content(soup,documentIndex,indexEnd-i)
		content.wrap(popover)
	'''
	content = locate_content(soup,documentIndex,indexStart)
	content.wrap(popover)
	return soup


def inject_popover(soup,coordinatesStart,coordinatesEnd,popover):
	'''
	wraps text within element
	'''
	#print('\tinject')
	documentIndex, index, charStart = coordinatesStart
	_,_,charEnd = coordinatesEnd
	content = locate_content(soup,documentIndex,index)

	if(isinstance(content,NavigableString)):
		return wrap_popover(soup,coordinatesStart,coordinatesEnd,popover)

	if(popover['title'] == 'c0b813bf-5f6f-4a4e-ae8a-111d85f46eff'):
		print(len(list(content.children)))

	start = content.string[:charStart] or ""
	middle = content.string[charStart:charEnd] or ""
	end = content.string[charEnd:] or ""

	

	popover.string = middle

	content.string = start
	content.append(popover)
	content.append(end)
	return soup


def get_point_coordinates(containerPath):
	'''
	parses the vital coordinates based on the containerPath
	'''
	pattern = r"^(.+)#.*\((.*)\)$"
	matches = re.search(pattern,containerPath)

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
	annotation = '<div class=\"text-small mb-3\">\"'+ bookmark.Text.replace("\"","\\\'") + '\"</div><div class=\"fw-bold\">'+  (bookmark.Annotation or '(No comment given.)').replace("\"","\\\'")+'</div>'
	tag = soup.new_tag('a')
	tag["href"] = "javascript:void(0)"
	tag["class"] = "kne-annotation bg-warning d-inline-block"
	tag["data-bs-toggle"] ="popover"
	tag["data-bs-placement"] ="bottom"
	tag["data-bs-trigger"] = "focus"
	tag["title"] = bookmark.BookmarkID
	tag["data-title"] = bookmark.BookmarkID
	tag["data-bs-html"] = "true"
	tag["data-bs-content"] = annotation
	return tag



def write_html(html,out):
	f = open(out,'w')
	f.write(html)
	f.close()



if __name__ == '__main__': main()