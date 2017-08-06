# confluence2markdown
Python 3.x tool converting Confluence html to Markdown. Primarily, it uses Github flavored Markdown, but also adds some stuff that is used on stackoverflow. Focusses on code-blocks, tables, lists, images. Might miss some other advanced html tags. See details below. Designed for Confluence 5.8.2.

# Requirements
You need 
1. python3
2. bs4 - [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Python3 should be available on most Linux distros. If on Mac, install via brew or download.

bs4 is a HtmlParser. Can be installed via package manager on several Linux distros (e.g. `apt-get install python3-bs4`). Otherwise install via pip (e.g. `pip3 install beautifulsoup4`)

# WARN
This project is a 0.x version NOT working yet, but under development

# Usage
- Open Confluence, go to space tools (need to be space admin), export, select html format, download the html zip-file, extract it somewhere
- c2m.py is the only file you need. Either clone the repo or download the single file. No installation required. chmod +x c2m.py
- Run `python3 c2m.py [sourcefolder] [destinationfolder]`

Sample:
```
python3 c2m.py /path/to/extracted/confluence/html/ /tmp/my-markdown
```

# Markdown

`Code blocks` are rendered Gibhub-flavored, using three backticks. stackoverflow uses 4-space-indention instead, but code on SO can be easily indented (CTRL-K). SO also uses optional HTML-comments to specify language. Github allows to specify language appended to backticks. \
\```python\
some code\
\```

Tables are rendered as-is, i.e. html is kept. Even though tables are often written with pipes in markup, pipe-tables have limitations. E.g. there is no way (i am aware of) to render multi-line-code within tables (in a single cell).


