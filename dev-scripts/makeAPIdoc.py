#!/usr/bin/python3
#
# Simple script to generate documentation
# for a Python Library
# 

import markdowndoc
import pydoc
import imp
import sys
import os
# Is possible that you want change this object
# import potools

pydoc.text = markdowndoc.MarkdownDoc()


def load_clas_from_file(path):
  class_inst = None
  expected_class = 'LtspChroot'
  mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
  
  if file_ext.lower() == '.py':
    py_mod = imp.load_source(mod_name, filepath)

  if hasattr (py_mod, expected_class):
    class_inst = py_mod.LtspChroot()

  return class_inst

def writeMarkdownAPI():
  toDocument = [LtspChroot]
  for thing in toDocument:
    fn = "%s.md" % thing.__name__
    print("Writing %s..." % fn)
    f = open(fn, 'w')
    md = pydoc.render_doc(thing)
    f.write(md)
    f.close()

if __name__ == "__main__":
  load_clas_from_file(sys.argv[1]) 
  writeMarkdownAPI()
