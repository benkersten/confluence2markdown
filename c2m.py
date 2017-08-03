
# imports
import argparse
import shutil
import os
# formerly used python's HTML parser, changed to bs4:
# from HTMLParser import HTMLParser
from bs4 import BeautifulSoup

# the actual conf-html-to-markdown logic:
def convert_html_to_markdown(html_content):
    # let bs4 parse the html:
    soup = BeautifulSoup(html_content, "html.parser")
    # the markdown string returned as result:
    md = ""
    
    # html-page title: Confluence uses "spacename : pagename". Remove the spacename here
    title = soup.title.string 
    print(title)
    position_colon = title.find(" : ")
    if position_colon >= 0 :
        title = title[(position_colon+3):]
    print(title)
    md += "# " + title
    print(md) 
    return md

# setup program arguments:
parser = argparse.ArgumentParser()
parser.add_argument("source", help="source folder, i.e. path to Confluence html files to be converted to .md")
parser.add_argument("dest", help="destination folder, i.e. path to folder where to write converted .md-files, e.g. /tmp/conf-md")
args = parser.parse_args()

# print info
print( "------------------------------" )
print( "Converting Confluence (.html to .md) from" )
print( args.source )
print( "to" )
print( args.dest )
print( "------------------------------" )

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



