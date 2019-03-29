#!/usr/bin/python

import json

def generate_sram( name, width, depth, mux, mask, typ ):
  # TODO: Implement SRAM generation
  print( '# ERROR -- Need to implement macro generation!' )

def main():

  # Load IDF into a dict object
  fid = open('floorplan.idf.json', 'r')
  idf = json.load(fid)
  fid.close()

  # For each SRAM, call the generate_sram(...) function
  for sram in idf['harden']['srams']:
    generate_sram( sram['name'], sram['width'], sram['depth'], sram['mux'], sram['mask'], sram['type'] )

if __name__ == '__main__':
  main()

