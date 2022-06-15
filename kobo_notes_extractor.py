import sqlite3,json
import ebooklib
from ebooklib import epub



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
	SQLLITE_PATH = "C:\\\\Users\\astro\\Documents\\KoboReader.sqlite"
	TitleLike = 'Bodies of Water'
	BookPath= "C:\\\\Users\\astro\\Calibre Library\\Alex Pendragon (draft)\\Bodies of Water (123)\Bodies of Water - Alex Pendragon (draft).epub"

	con = sqlite3.connect(SQLLITE_PATH)
	cur = con.cursor()
	
	contentId = get_content_id(cur,TitleLike)
	print(f"Found content Id {contentId}")

	bookmarks = get_content_bookmarks(cur,contentId)
	print(f"Found {len(bookmarks)} bookmarks")
	print(bookmarks[0].toJSON())

	book = parse_epub(BookPath)
	#print(book)



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
	rows = cur.execute("select * from Bookmark WHERE VolumeID=:ContentID ORDER BY DateCreated DESC",{"ContentID":ContentID}).fetchall()
	return [Bookmark(x) for x in rows]


def parse_epub(BookPath):
	book = epub.read_epub(BookPath)
	chapters = []   
	for item in book.get_items():        
		if item.get_type() == ebooklib.ITEM_DOCUMENT:
			chapters.append(item.get_content())
	return chapters


if __name__ == '__main__': main()