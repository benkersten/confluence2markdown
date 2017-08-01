# confluence2markdown
Python 2.7.x tool converting Confluence html to Markdown. Primarily, it uses Github flavored Markdown, but also adds some stuff that is used on stackoverflow. Focusses on code-blocks, tables, lists, images. Might miss some other advanced html tags.

# Zero dependencies
This project aims to have zero dependencies except for python 2.7.x itself, which is available on most systems. No extra packages, pip, or similar. To reach this goal, code is not as efficient/performant as it could be. E.g. bs4/BeatifulSoup is NOT used, though it would have been useful for html parsing. 

# WARN
This project is a 0.x version NOT working yet, but under development

# Usage
- Open Confluence, go to space tools (need to be space admin), export, select html format, download the html zip-file, extract it somewhere
- c2m.py is the only file you need. Either clone the repo or download the single file. No installation required. chmod +x c2m.py
- Run ./c2m.py [sourcefolder] [destinationfolder]

Sample:
```
python c2m.py /path/to/extracted/confluence/html/ /tmp/my-markdown
```

# Python version
Python 2.7.x is used by intention to be able to run on most platforms (e.g. MacOS still has no python3 by default when this project was started in 2017). Fork the project and use [2to3](https://docs.python.org/2/library/2to3.html) to use python3.


