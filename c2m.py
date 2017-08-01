
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

def convert_html_to_markdown(html_content):
    parser = ConfluenceHtmlToMarkdownConverter()
    parser.feed(html_content)
    return "not implemented yet"

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

# copy whole source tree to destination, i.e. the .html files.
# This makes it easier to handle path+folder and new .md files.
# Plus, if conversion fails for some files, one can inspect remaining html files.
shutil.copytree(args.source, args.dest)

# iterate all files. Read in html, write out md
for root, dirs, files in os.walk(args.dest):
    for file in files:
        filename, extension = os.path.splitext(file)
        # print file, filename, extension
        # skip non-html files:
        if not extension == '.html':
            continue

        # read html
        html_file_path = os.path.join(root, file)
        with open(html_file_path, 'r') as fin:
            html_content = fin.read()

        # convert html to markdown
        markdown_content = convert_html_to_markdown(html_content)

        # write markdown to .md file
        markdown_filename = "%s.md" % filename
        markdown_file_path = os.path.join(root, markdown_filename)
        with open(markdown_file_path, 'w') as fout:
            fout.write(markdown_content)

        # remove copied .html file
        os.remove(html_file_path)



