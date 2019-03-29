'''
tf_parser.py

This file is a very simple pyparsing grammar for parsing a Technology File
(.tr). The technology file is then returned as a dict. You can test the parser
by executing this script and passing the .tf file as the first command line
argument and the resulting dict will be printed to standard out, or you may
import this script and use the techfile_to_dict(...) function inside your own
script.
'''

import sys
import json

from pyparsing import *

### Setup the grammar for the tf_parser object

tf_num_group = Literal('"').suppress()                           \
                 + Group(                                        \
                   Word(nums+'e.-')                              \
                   + ZeroOrMore(                                 \
                     Literal(',').suppress() + Word(nums+'e.-')  \
                   )                                             \
                 )                                               \
               + Literal('"').suppress()

tf_tbl_entry = Word(nums+'e.-')      \
               ^ Word(alphanums+'_') \
               ^ tf_num_group

tf_table = Literal('(').suppress()                                             \
           + tf_tbl_entry + ZeroOrMore(Literal(',').suppress() + tf_tbl_entry) \
           + Literal(')').suppress()

tf_key = Word(alphanums+'_')('key')

tf_value = Literal('"').suppress() + Optional(Word(alphanums+'_ '))('value') + Literal('"').suppress() \
           ^ Word( nums + 'e.-' )('value')                                                             \
           ^ Group(tf_table)('value')

tf_section = Group(                                                                                                                                \
               Word(alphanums+'_')('name')                                                                                                         \
               + Optional(Literal('"').suppress() + Word(alphanums+'_ ')('value') + Literal('"').suppress())                                       \
               + Literal('{').suppress() + Group(OneOrMore(Group(tf_key + Literal('=').suppress() + tf_value)))('items') + Literal('}').suppress() \
             )

tf_parser = Group(OneOrMore(tf_section))('sections')
tf_parser.ignore(cppStyleComment)
tf_parser.ignore(Literal(';') + SkipTo(lineEnd))

# techfile_to_dict ( fid_or_filename )
#
# Read the file specified (can be an opened file pointer object or the path to
# a file) and convert it to a dict object.
#
def techfile_to_dict ( fid_or_filename ):
  return tf_parser.parseFile(fid_or_filename).asDict()

# main()
#
# This is the entry point for testing the tf parser. This will parse the given
# tf file (the first command line argument) and print out the resulting dict
# using the json package to print it out nicely.
#
def main():
  print (json.dumps(techfile_to_dict(sys.argv[1]), indent=2))

if __name__ == '__main__':
  main()

