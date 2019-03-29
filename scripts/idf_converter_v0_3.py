'''
idf_converter_v0_3.py

This file contains the main idf to def file convert for IDF v0.3. The output of
the convert is a list of tuples in the form (design_name, def_file_lines). The
design_name is a string of the design's name and the def_file_lines is a list
of strings where each string is a new line in the def file.
'''

import re

# Just make sure that this number is >= the max number of metal layers in your
# technology. It is for initial list allocation so a large number should have
# very minimal impact on performance therefore I set it arbitrarily large.

MAX_NUMBER_OF_METAL_LAYERS = 100

# convert_idf_to_def_v0_3( idf, tf, first_metal_h=False, max_metal_layer=-1 )
#
# IDF to DEF conversion function for IDF v0.3.
#
def convert_idf_to_def_v0_3( idf, tf, first_metal_h=False, max_metal_layer=-1 ):

  # Get some easier to use dicts with the .tf file data
  unit_tile, layer_stack = __extract_data_from_tf_dict( tf, max_metal_layer )

  # Get the x dimensional scalar
  if idf['units']['x'] == 'cpp':
    x_unit = unit_tile['width']
  elif idf['units']['x'] == 'track_width':
    bot_v = 1 if first_metal_h else 0
    x_unit = layer_stack[bot_v]['minSpacing'] + layer_stack[bot_v]['minWidth']
  else:
    print('Error: Unknown unit:x - %s' % idf['units']['x'])
    return

  # Get the y dimensional scalar
  if idf['units']['y'] == 'track_height':
    bot_h = 0 if first_metal_h else 1
    y_unit = layer_stack[bot_h]['minSpacing'] + layer_stack[bot_h]['minWidth']
  else:
    print('Error: Unknown unit:y - %s' % idf['units']['y'])
    return

  # Return value list of tuples in the form (design_name, def_file_lines)
  result = []

  # Iterate through each design
  for design in idf['designs']:

    # List of lines that form the def file
    lines = []

    #########################
    # BEGIN DEF FILE
    #########################

    lines.append( 'VERSION 5.7 ;' )
    lines.append( 'DIVIDERCHAR "/" ;' )
    lines.append( 'BUSBITCHARS "[]" ;' )
    lines.append( 'DESIGN %s ;' % design['name'] )
    lines.append( 'UNITS DISTANCE MICRONS 1000 ;' )
    #lines.append( 'PROPERTYDEFINITIONS' )
    #lines.append( 'COMPONENTPIN ACCESS_DIRECTION STRING ;' )
    #lines.append( 'END PROPERTYDEFINITIONS' )

    #########################
    # DIE AREA
    #########################

    die_llx = int(idf['area']['die']['llx']) * x_unit
    die_lly = int(idf['area']['die']['lly']) * y_unit
    die_urx = int(idf['area']['die']['urx']) * x_unit
    die_ury = int(idf['area']['die']['ury']) * y_unit
    die_width  = die_urx-die_llx
    die_height = die_ury-die_lly

    lines.append( 'DIEAREA ( {0} {1} ) ( {0} {3}  ) ( {2} {3} ) ( {2} {1} ) ;'.format(
      die_llx,
      die_lly,
      die_urx,
      die_ury
    ))

    #########################
    # STD CELL ROWS
    #########################

    core_llx = int(idf['area']['core']['llx'])*x_unit
    core_lly = int(idf['area']['core']['lly'])*y_unit
    core_urx = int(idf['area']['core']['urx'])*x_unit
    core_ury = int(idf['area']['core']['ury'])*y_unit
    core_width  = core_urx-core_llx
    core_height = core_ury-core_lly
    
    ver_site_count = int( core_height / unit_tile['height'] )
    hor_site_count = int( core_width  / unit_tile['width'] )

    for i in range(ver_site_count):
      lines.append( 'ROW STD_ROW_{0} unit {1} {2} {3} DO {4} BY 1 STEP {5} 0 ;'.format(
        i,
        core_llx,
        core_lly + (unit_tile['height'] * i),
        "N" if i%2==0 else "FS",
        hor_site_count,
        unit_tile['width']
      ))

    #########################
    # TRACKS
    #########################

    for layer in layer_stack:
      track_pitch = layer['minWidth'] + layer['minSpacing']
      track_count_x = int( die_width  / track_pitch )
      track_offset_x = int( core_width  - int(core_width  / track_pitch) * track_pitch) + die_llx
      lines.append( 'TRACKS X {0} DO {1} STEP {2} LAYER {3} ;'.format(
        track_offset_x,
        track_count_x,
        track_pitch,
        layer['name']
      ))

      track_count_y = int( die_height / track_pitch )
      track_offset_y = int( core_height - int(core_height / track_pitch) * track_pitch) + die_lly
      lines.append( 'TRACKS Y {0} DO {1} STEP {2} LAYER {3} ;'.format(
        track_offset_y,
        track_count_y,
        track_pitch,
        layer['name']
      ))

    #########################
    # COMPONENTS
    #########################

    lines.append( 'COMPONENTS %d ;' % len(design['place']) )

    for comp in design['place']:
      lines.append( ' - {0} {1} + SOURCE DIST + PLACED ( {2} {3} ) {4} ;'.format(
        comp['name'],
        comp['type'],
        int(comp['x']) * x_unit,
        int(comp['y']) * y_unit,
        comp['orientation']
      ))

    lines.append( 'END COMPONENTS' )

    #########################
    # PINS
    #########################

    lines.append( 'PINS %d ;' % len(design['io_ports']) )

    for pin in design['io_ports']:

      pin_layer = __get_relative_layer(pin['layer'], layer_stack, first_metal_h)

      if   pin['side'] == 'top':    pin_orientation = 'S'
      elif pin['side'] == 'bottom': pin_orientation = 'N'
      elif pin['side'] == 'left':   pin_orientation = 'E'
      elif pin['side'] == 'right':  pin_orientation = 'W'

      lines.append( ' - {0} + NET {0} + USE SIGNAL + LAYER {1} ( 0 0 ) ( {2} {2} ) + PLACED ( {3} {4} ) {5} ;'.format(
        pin['name'],
        pin_layer['name'],
        pin_layer['minWidth'],
        int(pin['x']) * x_unit,
        int(pin['y']) * y_unit,
        pin_orientation
      ))

    lines.append( 'END PINS' )

    #########################
    # PLACEMENT BOUNDS
    #########################

    lines.append( 'REGIONS %d ;' % len(design['placement_bounds']) )

    for i, bound in enumerate(design['placement_bounds']):
      lines.append( ' - bound_{0} ( {1} {2} ) ( {3} {4} ) {5};'.format(
        i,
        int(bound['llx']) * x_unit,
        int(bound['lly']) * y_unit,
        int(bound['urx']) * x_unit,
        int(bound['ury']) * y_unit,
        '+ TYPE GUIDE ' if bound['type']=='soft' else ''
      ))

    lines.append( 'END REGIONS' )

    lines.append( 'GROUPS %d ;' % len(design['placement_bounds']) )

    for i, bound in enumerate(design['placement_bounds']):
      lines.append( ' - group_{0} {1} + REGION bound_{0} ;'.format(
        i,
        bound['inst']
      ))

    lines.append( 'END GROUPS' )

    #########################
    # END DEF FILE
    #########################

    lines.append( 'END DESIGN' )
    lines.append( '' )

    result.append( (design['name'], lines) )

  return result

# __extract_data_from_tf_dict( tf, max_metal_layers=-1 )
#
# This function takes the raw techfile dict from the techfile parser and
# creates new dicts that are easier to use for this particular application.
#
def __extract_data_from_tf_dict( tf, max_metal_layers=-1 ):
  unit = {}
  layers = [None for i in range(MAX_NUMBER_OF_METAL_LAYERS)]
  for s in tf['sections']:
    ### Unit tile section
    if s['name'] == 'Tile' and s['value'] == "unit":
      for i in s['items']:
        if i['key'] == 'width':
          unit['width']  = int(float(i['value'])*1000)
        elif i['key'] == 'height':
          unit['height'] = int(float(i['value'])*1000)
    ### Layer sections
    elif s['name'] == 'Layer':
      maskName = list(filter(lambda d: d['key'] == 'maskName', s['items']))
      if len(maskName) > 0 and 'value' in maskName[0]:
          match = re.match('metal([0-9]+)', maskName[0]['value'])
          if match:
            l = {}
            l['name']       = s['value']
            l['minWidth']   = int(float(list(filter(lambda d: d['key'] == 'minWidth',   s['items']))[0]['value'])*1000)
            l['maxWidth']   = int(float(list(filter(lambda d: d['key'] == 'maxWidth',   s['items']))[0]['value'])*1000)
            l['minSpacing'] = int(float(list(filter(lambda d: d['key'] == 'minSpacing', s['items']))[0]['value'])*1000)
            layers[int(match.group(1))] = l
  layers = [l for l in layers if l]
  if max_metal_layers >= 0:
    layers = layers[0:max_metal_layers]
  return (unit, layers)

# get_relative_layer( layer_string, layer_stack, first_metal_h=False )
#
# In the IDF format, metal layers are specified in a relative format where the
# metal layer can be relative to the top or bottom of the metal stack. It can
# also be specified relative to only the horizontal and vertical layers. This
# function will take the relative layer string from the IDF file and return the
# layer object form the layer stack dict. Note: The assumption is that every
# metal layer changes their preferred routing direction. By default the first
# metal layer is considered horiztonal but can be changed via the first_metal_h
# argument.
#
def __get_relative_layer( layer_string, layer_stack, first_metal_h=False ):
  match = re.match('metal-(B|BH|BV|T|TH|TV)([0-9]+)', layer_string)
  if match:
    rel = match.group(1)
    num = int(match.group(2))
    if rel == 'B':
      bot = 0
      offset = num - 1
      abs_num = bot + offset
    elif rel == 'BH':
      bot_h = (0 if first_metal_h else 1)
      offset = 2*(num-1)
      abs_num = bot_h + offset
    elif rel == 'BV':
      bot_v = (1 if first_metal_h else 0)
      offset = 2*(num-1)
      abs_num = bot_v + offset
    elif rel == 'T':
      top = len(layer_stack) - 1
      offset = num - 1
      abs_num = top - offset
    elif rel == 'TH':
      even = (len(layer_stack) % 2) == 0
      top_is_h = (even and not first_metal_h) or (not even and first_metal_h)
      top_h = (len(layer_stack)-1 if top_is_h else len(layer_stack)-2)
      offset = 2*(num-1)
      abs_num = top_h - offset
    elif rel == 'TV':
      even = (len(layer_stack) % 2) == 0
      top_is_h = (even and not first_metal_h) or (not even and first_metal_h)
      top_v = (len(layer_stack)-2 if top_is_h else len(layer_stack)-1)
      offset = 2*(num-1)
      abs_num = top_v - offset
    return layer_stack[abs_num]
  return None

