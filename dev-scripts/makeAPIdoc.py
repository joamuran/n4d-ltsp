#!/usr/bin/python3
#
# Simple script to generate documentation
# for a Python Library
# 

import markdowndoc
import pydoc

# Is possible that you want change this object
import potools

pydoc.text = markdowndoc.MarkdownDoc()

def writeMarkdownAPI():
    toDocument = [potools]
    for thing in toDocument:
        fn = "%s.md" % thing.__name__
        print("Writing %s..." % fn)
        f = open(fn, 'w')
        md = pydoc.render_doc(thing)
        f.write(md)
        f.close()

if __name__ == "__main__":
    writeMarkdownAPI()
