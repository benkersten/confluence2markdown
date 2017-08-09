
# imports
import argparse
import shutil
import os
# formerly used python's HTML parser, changed to bs4:
# from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag

# flags
rendering_html = False
indent = -1
li_break = False
li_for_ul_only = False # see convert_li

# linebreaks
md_br = "\n"
md_dbr = "\n\n"
html_br = "<br/>"
html_dbr = "<br/><br/>"
def linebreak():
    if rendering_html:
        return html_br
    else:
        return md_br

# convert the passed html-tag. Delegates to convert-* functions depending on tag
def convert_html_tag(tag):
    if tag is None:
        return ""

    # info about this tag:
    tag_info = ("convert_html_tag: type="+(str(type(tag))) + ", classname="+tag.__class__.__name__)
    if tag.name is not None:
        tag_info += (", name="+tag.name)
    # print(tag_info) 
    
    # check type:
    # if isinstance( type(tag), type(NavigableString) ): # would return true for <p> too, checks subtypes
    #if tag.__class__.__name__ == "NavigableString" :
    #    print("string==true")
    #if tag.__class__ == NavigableString :
    #    print("string==true")

    if tag.name == "div":
        return convert_div(tag)
    if tag.name == "p":
        return convert_p(tag)
    if tag.name == "table":
        return convert_table(tag)
    if tag.name == "img":
        return convert_img(tag)
    if tag.name == "a":
        return convert_a(tag)
    if tag.name == "ul":
        return convert_ul(tag)
    if tag.name == "pre":
        return convert_pre(tag)
    return ""

def convert_div(tag):
    md = ""
    for child in tag.children:
        if child.__class__ == NavigableString:
            md += child.string
        else:
            md += convert_html_tag(child)
    return md

def convert_p(tag):
    md = ""
    # How to add text in <p>text</p>?
    # - tag.text does not work: returns text of ALL children
    # - tag.string does not work: fails if there are other tags, e.g. as in <p>text<br/>more text</p>
    # So, instead traverse children and check for string or tag.
    for child in tag.children:
        # print("convert_p:child:"+(str(type(child))))
        if child.__class__ == NavigableString:
            md += child.string
            # print("NavigableString: "+child.string)
        elif child.__class__ == Tag:
            if child.name == "br":
                # print("tag-br")
                md += linebreak()
            else:
                md += str(tag)
        else:
            md += str(tag)
    
    # linebreak at end of tag
    md += linebreak()
    
    return md

def convert_table(tag):
    # in markdown, tables can be represented with pipes:
    # Col1 | Col2 ...
    # or by just rendering html. As complex tables (e.g. with multi-line-code) does not work
    # with pipe-rendering, just keep the html-table as-is:

    # set rendering_html, so that other tag-processing works fine. E.g. <br/> will be kept as
    # <br/> instead of being converted to \n
    global rendering_html
    rendering_html = True
    md = ""
    md += linebreak()
    # just keep the <html>-table as-is:
    md = str(tag)
    # remove confluence-CSS
    md = md.replace(' class="confluenceTd"', '')
    md = md.replace(' class="confluenceTr"', '')
    md = md.replace(' class="confluenceTh"', '')
    md = md.replace(' class="confluenceTable"', '')
    rendering_html = False

    # linebreak at end of tag
    md += linebreak()
    md += linebreak()
    
    return md

def convert_img(tag):
    return ""
    
def convert_a(tag):
    return ""

def convert_pre(tag):
    # pre-tag -> source code
    md = ""
    md += linebreak()

    # Confluence uses "brush" for a specified language, e.g. <pre class="brush: bash; gutter: ...
    # Note: in bs4, tag-attributes which are expected to be multi-valued (such as 'class'),
    # will return a list of values EVEN if there are colon-/semicolon values: i.e. 'brush: bash' will
    # be returned as two values
    lang = ""
    class_value_list = tag['class']
    if class_value_list is not None:
        for idx, val in enumerate(class_value_list):
            if val == "brush:":
                # next value after brush is language. Remove last char via :-1
                lang = (class_value_list[idx+1])[:-1]
                break

    # add language-notification via HTML-comment as used on stackoverflow. This is ignored on 
    # github anyway (just a comment):
    if lang != "":
        md += "<!-- language: lang-" + lang + " -->"
        md += linebreak()
 
    # use github-flavored markdown (three backticks): 
    md += "```" + lang
    md += linebreak()
    
    for child in tag.children:
        if child.__class__ == NavigableString:
            md += child.string
    
    md += linebreak()
    md += "```"
    md += linebreak()
    return md

def convert_ul(tag):
    md = ""
    # insert linebreaks around <ul>, but NOT for nested <ul>. Therefore, linebreak
    # only if indent-level is -1:
    global indent
    global li_for_ul_only
    #if indent == -1:
    if not li_for_ul_only:
        md += linebreak()
    # increase indention for each list level
    indent += 1
    for child in tag.children:
        if child.__class__ == Tag:
            if child.name == "li":
                md += convert_li(child)
    # reset indention
    indent -= 1
    if indent == -1:
        md += linebreak()
    return md

def convert_li(tag):
    # each <li> is prefixed with a dash
    md = ""
    global indent
    global li_break
    # reset li_break, see end of function
    li_break = False
    # true if current <li> exist for purpose of single <ul> only, as in "<li><ul><li>content</li></ul></li>
    global li_for_ul_only
    # reset li_for_ul_only, might be True from previous nested list-element
    li_for_ul_only = False
    
    # check if current <li> exist for purpose of single <ul> only, as in "<li><ul><li>content</li></ul></li>
    if len(tag.contents)==1 and tag.contents[0].__class__ == Tag and tag.contents[0].name == "ul":
        li_for_ul_only = True

    # indent markup depending on level
    if not li_for_ul_only:
        for i in range(0,indent*2):
            md += " "
        md += "- "

    # traverse children: append strings, delegate tag processing
    for child in tag.children:
        if child.__class__ == NavigableString:
            # a string, just append it
            md += child.string
        elif child.__class__ == Tag:
            md += convert_html_tag(child)
    
    # Linebreak after <li>. Skip if last chars in "md" already were li-break, as in </li></ul></li>.
    if not li_break and not li_for_ul_only:
        md += linebreak()
        li_break = True

    return md

# convert the whole page / html_content. Taverses children and delegates logic per tag.
def convert_html_page(html_content):
    # let bs4 parse the html:
    soup = BeautifulSoup(html_content, "html.parser")
    # the markdown string returned as result:
    md = ""
    
    # html-page title: Confluence uses "spacename : pagename". Remove the spacename here
    title = soup.title.string 
    position_colon = title.find(" : ")
    if position_colon >= 0 :
        title = title[(position_colon+3):]
    md += "# " + title + md_dbr
    
    # goto <body><div id="main-content"> and ignore all that other Confluence-added-garbage
    div_main = soup.find("div", {"id": "main-content"})
    if div_main is None :
        return md
    # traverse all children of div_main and try to convert to markdown
    for child in div_main.children:
        md += convert_html_tag(child)

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
        markdown_content = convert_html_page(html_content)

        # write markdown to .md file
        markdown_filename = "%s.md" % filename
        markdown_file_path = os.path.join(root, markdown_filename)
        with open(markdown_file_path, 'w') as fout:
            fout.write(markdown_content)

        # remove copied .html file
        os.remove(html_file_path)



