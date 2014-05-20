import StringIO
import urllib2
from collections import defaultdict, namedtuple
import re
import datetime
import calendar

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox

from contextlib import closing


BoundingBox = namedtuple('BoundingBox',['x','y','width','height'])

def in_bounding_box(box,x,y):
    return (box.x <= x <= box.x+box.width) and (box.y <= y <= box.y + box.height)


column_x_and_widths =  {
	"course": (48,66),
	"crn": (114,35),
	"type": (150,70),
	"date": (220,90),
	"time": (310,94),
	"instructor": (402,108),
	"room": (512,52)
}

column_height = 660
column_y = 73


def make_bounding_boxes():
	return {
		name: BoundingBox(x =info[0],width=info[1],y=column_y,height=column_height) for name,info in column_x_and_widths.items()
	}


bounding_boxes = make_bounding_boxes()


def download_schedule():
    """ 
    Downloads a servery pdf and returns a StringIO file descriptor of the data.
    Note that the StringIO does not need to be closed like a regular file.
    """
    complete_url = "http://registrar.rice.edu/WorkArea/DownloadAsset.aspx?id=2147483951"
    with closing(urllib2.urlopen(complete_url)) as servery_file:
        data = servery_file.read()
    
    return StringIO.StringIO(data)


def process_pdf(file_handle):
    """
    Processes a PDF in a file_handle and returns a generator of ((x,y),text) tuples for each page.
    The final result is somewhat equivalent to [ [(x,y,text) for text in page] for page in PDF].
    """
    parser = PDFParser(file_handle)
    document = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr,laparams=LAParams(char_margin=1.0))
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in list(PDFPage.create_pages(document))[:2]:
        interpreter.process_page(page)
        layout = device.get_result()
        text_positions = get_text_positions(layout)

        processed = process_text_positions(text_positions)
        result = coalesces_rows(processed)
        for item in result:
        	yield item

def coalesces_rows(processed):
	result = defaultdict(dict)

	for name,row,text in processed:
		result[row][name] = text

	return result.values()

def get_type(x,y):
	for name,bounding_box in bounding_boxes.items():
		if in_bounding_box(bounding_box,x,y):
			return name

	return None

def get_row(y):
	return int((y - column_y) * 34.0/(660.0))

def process_text_positions(text_positions):
	for a in text_positions:
		name = get_type(a[0][0],a[0][1])
		row = get_row(a[0][1])
		if name is not None:
			yield (name,row,a[1])





def get_text_positions(layout):
    """Processes a single page in a PDF and returns a generator of ((x,y),text) tuples."""
    for child in layout:
        if isinstance(child,LTTextBox):
            for line in child:
                coords = (line.x0+line.x1)/2, layout.height - (line.y0 + line.y1)/2
                yield (coords,line.get_text().strip())

def strip_schedule():
	schedule = download_schedule()
	return process_pdf(schedule)


if __name__ == "__main__":
	print list(strip_schedule())