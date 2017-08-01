
# imports
import argparse
import shutil
import os
from HTMLParser import HTMLParser

# confluencehtml2markdown-converter extending pyhton's HTMLParser
# TODO convert. For now, just prints html tags
class ConfluenceHtmlToMarkdownConverter(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag

    def handle_data(self, data):
        print "Encountered some data  :", data


# setup program arguments:
parser = argparse.ArgumentParser()
parser.add_argument("source", help="source folder, i.e. path to Confluence html files to be converted to .md")
parser.add_argument("dest", help="destination folder, i.e. path to folder where to write converted .md-files, e.g. /tmp/conf-md")
args = parser.parse_args()

# print info
print "------------------------------"
print "Converting Confluence (.html to .md) from"
print args.source
print "to"
print args.dest
print "------------------------------"

# iterate all files. Read in html, write out md
for root, dirs, files in os.walk(args.source):
    for file in files:
        filename, extension = os.path.splitext(file)
        # skip non-html files:
        if not extension == '.html':
            continue

        # read html
        html_file_path = os.path.join(root, file)
        with open(html_file_path, 'r') as fin:
            html_content = fin.read()

        parser = ConfluenceHtmlToMarkdownConverter()
        parser.feed(html_content)

