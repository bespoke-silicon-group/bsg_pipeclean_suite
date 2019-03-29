'''
usage: idf_to_def.py [-h] -idf file -tf file -o file [-swap_metal]
                     [-max_metal_layer num]

This script takes an IDF json floorplanning file and converts it to a DEF
file. IDF files are "dimensionaless" therefore the user must provide the
technology file (.tf) for the target process.

optional arguments:
  -h, --help            show this help message and exit
  -idf file             Input IDF .json file
  -tf file              Input technology file (.tf)
  -o file               Output .def file
  -swap_metal           Changes the starting orientation of the metal stack.
                        By default, the first metal layer is assumed to be
                        horizontal. Use this flag to set the first metal layer
                        to be vertical.
  -max_metal_layer num  Used to specify the max metal layer number
'''

import sys
import argparse
import json
import re

from tf_parser import techfile_to_dict

# Import converter functions for various IDF versions. To add a new version
# converter, use the proper function naming convetion and simply import the
# function here. The script will call the new converter based on the version
# found in the IDF file.

from idf_converter_v0_3 import convert_idf_to_def_v0_3

### Setup the argument parsing

app_desc = '''
  This script takes an IDF json floorplanning file and converts it to a DEF
  file. IDF files are "dimensionaless" therefore the user must provide the
  technology file (.tf) for the target process.
'''

swap_metal_desc = '''
  Changes the starting orientation of the metal stack. By default, the first
  metal layer is assumed to be vertical. Use this flag to set the first metal
  layer to be horizontal.
'''

parser = argparse.ArgumentParser(description=app_desc)
parser.add_argument('-idf', metavar='file', dest='idf', required=True, type=argparse.FileType('r'), help='Input IDF .json file')
parser.add_argument('-tf', metavar='file', dest='tf', required=True, type=argparse.FileType('r'), help='Input technology file (.tf)')
#parser.add_argument('-o', metavar='file', dest='outfile', required=True, type=argparse.FileType('w'), help='Output .def file')
parser.add_argument('-swap_metal', dest='first_metal_h', action='store_true', help=swap_metal_desc)
parser.add_argument('-max_metal_layer', metavar='num', default=-1, dest='max_metal_layer', type=int, help='Used to specify the max metal layer number')
args = args = parser.parse_args()

### Read the IDF file and TF file into a dicts

idf = json.load(args.idf)
args.idf.close()

tf  = techfile_to_dict(args.tf)
args.tf.close()

### Call the convert function based on the IDF version

idf_version = idf['version'].replace('.', '_')
if hasattr(sys.modules[__name__], 'convert_idf_to_def_v'+idf_version):
  convert_func = getattr(sys.modules[__name__], 'convert_idf_to_def_v'+idf_version)
  def_files = convert_func(idf, tf, args.first_metal_h, args.max_metal_layer)
  if not def_files:
    print('Error: failed to generate DEF file, exiting!')
    sys.exit(1)
else:
  print('Error: No valid conversion function for IDF version %s, exiting!' % idf['version'])
  sys.exit(1)

### Write out the def file

for def_file in def_files:
  with open('%s.def' % def_file[0], 'w') as fid:
    fid.write('\n'.join(def_file[1]))

### Close and exit

sys.exit(0)

