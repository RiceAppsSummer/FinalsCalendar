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
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        print layout
        print list(layout)
