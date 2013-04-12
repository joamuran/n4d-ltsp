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


def load_class_from_file(path,class_name):
  class_inst = None
  expected_class = 'LtspChroot'
  mod_name,file_ext = os.path.splitext(os.path.split(path)[-1])
  '''
  if file_ext.lower() == '.py':
    py_mod = imp.load_source(mod_name, path)

  if hasattr (py_mod, expected_class):
    class_inst = py_mod.LtspChroot()
  '''

  module=imp.load_source(class_name,path)
  return module

def writeMarkdownAPI(module,class_name):

  # getattr(module,class_name) == LtspChroot.LtspChroot
  
  # ltsp=LtspChroot.LtspChroot()
  # ltsp.apt()
  # getattr(ltsp,"apt") == ltsp.apt
  # getattr(ltsp,"apt")()
  
  toDocument = [getattr(module,class_name)]
  for thing in toDocument:
    fn = "%s.md" % thing.__name__
    print("Writing %s..." % fn)
    f = open(fn, 'w')
    md = pydoc.render_doc(thing)
    f.write(md)
    f.close()


def usage():
  print("\nUSAGE:")
  print("\tmakeAPIdoc CLASS_FILE CLASS_NAME\n")

if __name__ == "__main__":
  try:
    if len(sys.argv)==3:
      module=load_class_from_file(sys.argv[1],sys.argv[2]) 
      writeMarkdownAPI(module,sys.argv[2])
    else:
      usage()
  except Exception as e:
    print("* Execution failed:\n")
    print(e)

