#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# -------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------
#
# This file is a Python plug-in for GIMP which imports text from a file
# into layers.

import sys
import codecs
from gimpfu import *

justification_list = ["Gauche justifié", "Right justified", "Centered", "Filled"]
justification_values = [
    TEXT_JUSTIFY_LEFT, 
    TEXT_JUSTIFY_RIGHT, 
    TEXT_JUSTIFY_CENTER, 
    TEXT_JUSTIFY_FILL]
alignment_list = ["top", "bottom", "middle"]
hintstyle_list = ["None", "Slight", "Meium", "Full"]
hintstyle_values = [
    TEXT_HINT_STYLE_NONE,
    TEXT_HINT_STYLE_SLIGHT,
    TEXT_HINT_STYLE_MEDIUM,
    TEXT_HINT_STYLE_FULL]

boxmode_list = [
    "fixed",
    "dynamic",
    "shrink font size to fit",
    "grow font size to fit",
    "best font size fit",
    "shrink width to fit",
    "grow width to fit",
    "best width",
    "shrink height to fit",
    "grow height to fit",
    "best height" ]
# arguments:
#   image, active_layer, 
#   source_path, source_seperator, font, font_size, antialias, hintstyle, 
#   font_color, justification, vertical_align, indent, letter_spacing, 
#   line_spacing, box_mode, language, padding_horz, padding_vert, offset_horz, 
#   offset_vert, use_markdown
def plugin_import_text_layers_dctrad(image, active_layer, 
    source_path, 
    source_seperator, 
    source_escaped, 
    font, 
    font_size, 
    antialias, 
    hintstyle_index, 
    #font_color, 
    justification_index, 
    #vertical_align_index, 
    #indent, 
    letter_spacing, 
    line_spacing, 
    box_mode_index, 
    #language, 
    padding, 
    offsets):
    #use_markdown):
  (padding_horz,padding_vert) = padding.split(',')
  (offset_horz, offset_vert) = offsets.split(',')
  indent = 0
  font_color = '#000000'
  language = 'en'
  use_markdown = False
  return import_text_layers(image, active_layer, source_path, source_seperator, source_escaped, font, font_size, antialias, hintstyle_values[hintstyle_index], font_color, justification_values[justification_index], indent, letter_spacing, line_spacing, boxmode_list[box_mode_index], language, int(padding_horz), int(padding_vert), int(offset_horz), int(offset_vert), use_markdown)

def import_text_layers(image, active_layer, source_path, source_seperator, source_escaped, font, font_size, antialias, hintstyle, font_color, justification, indent, letter_spacing, line_spacing, box_mode, language, padding_horz, padding_vert, offset_horz, offset_vert, use_markdown):
  
  #source_file = file(source_path, 'r')
  source_file = codecs.open(source_path, "r", encoding="utf_8", buffering=0)
  raw_source = source_file.read()
  source_file.close()
  if (raw_source):
    source = raw_source
  else:
    pdb.gimp_message("failure: invalid source file(\""+source_path+"\")")
    return
  
  #text_list = source.split("\n"+source_seperator)
  text_list = source.splitlines()
  
  pdb.gimp_image_undo_group_start(image)
  
  layer_position = 0
  layer_offsetx = 0
  layer_offsety = 0
  layer_width = pdb.gimp_image_width(image)
  layer_height = pdb.gimp_image_height(image)
  if (active_layer):
    layer_position = pdb.gimp_image_get_layer_position(image, active_layer)
    layer_offsetx = active_layer.offsets[0]
    layer_offsety = active_layer.offsets[1]
    tlayer_x = layer_offsetx
    tlayer_y = layer_offsety
    layer_width = active_layer.width
    layer_height = active_layer.height
  
  for rawtext in text_list:
    if (source_escaped):
      text = rawtext.decode('unicode_escape')
    else:
      text = rawtext
    tlayer_x = tlayer_x + padding_horz
    tlayer_y = tlayer_y + padding_vert
    #tlayer_width = layer_width - padding_horz * 2
    #tlayer_height = layer_height - padding_vert * 2
    tlayer_width = 450
    tlayer_height = 100
    
    tlayer = pdb.gimp_text_layer_new(image, text, font, font_size, 0)
    pdb.gimp_image_add_layer(image, tlayer, layer_position)
    
    pdb.gimp_text_layer_set_antialias(tlayer, antialias)
    pdb.gimp_text_layer_set_color(tlayer, font_color)
    pdb.gimp_text_layer_set_indent(tlayer, indent)
    pdb.gimp_text_layer_set_justification(tlayer, justification)
    #pdb.gimp_text_layer_set_kerning(tlayer, kerning)
    pdb.gimp_text_layer_set_hint_style(tlayer, hintstyle)
    #pdb.gimp_text_layer_set_hinting(tlayer, hinting)
    pdb.gimp_text_layer_set_language(tlayer, language)
    pdb.gimp_text_layer_set_letter_spacing(tlayer, letter_spacing)
    pdb.gimp_text_layer_set_line_spacing(tlayer, line_spacing)
    
    if (box_mode == 'fixed'):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == "dynamic"):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == "shrink font size to fit"):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == "grow font size to fit"):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == "best font size fit"):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == "shrink width to fit"):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == "grow width to fit"):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == "best width"):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == "shrink height to fit"):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == "grow height to fit"):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == "best height"):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == 'grow_font_to_fit'):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == 'adjust_font_to_fit'):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == 'shrink_width_to_fit'):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == 'grow_width_to_fit'):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == 'adjust_width_to_fit'):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == 'shrink_height_to_fit'):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == 'grow_height_to_fit'):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    elif (box_mode == 'adjust_height_to_fit'):
      pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)
    else:
      pdb.gimp_message("failure: invalid box_mode(\""+box_mode+"\")")
      return
    
    #if (vertical_align == 'top'):
    #  
    #elif (vertical_align == 'bottom'):
    #  
    #elif (vertical_align == 'middle'):
    #  
    #else:
    #  pdb.gimp_message("failure: invalid vertical alignment(\""+vertical_align+"\")")
    #  return
    
    pdb.gimp_layer_set_offsets(tlayer, tlayer_x+offset_horz, tlayer_y+offset_vert)
    pdb.gimp_item_set_visible(tlayer, True)
  
  pdb.gimp_image_undo_group_end(image)
  
  return



register(
    "plugin_import_text_layers_dctrad",
    "import text",
    "Import text from file to layers",
    "ELH",
    "Open source (BSD 3-clause license)",
    "2017",
    "<Image>/DC-trad/Import Text DCtrad",
    "*",
    # (type, name, description, default [, extra])
    [ (PF_FILE,     "source_path",      "text file",        ''),
      (PF_STRING,   "source_seperator", "text seperator",   ''),
      (PF_BOOL,     "source_escaped",   "text is escaped",  False),
      (PF_FONT,     "font",             "font",             'Sans'),
      (PF_INT,      "font_size",        "font size",        27),
      (PF_BOOL,     "antialias",        "antialias",        True),
      (PF_OPTION,   "hintstyle_index",    "hint style",     0, hintstyle_list) ,
      #(PF_COLOR,    "font_color",       "font color",       '#000000'),
      (PF_OPTION,   "justification_index","justification",  2, justification_list),
      #(PF_OPTION,   "vertical_align_index","alignment",     0, alignment_list),
      #(PF_FLOAT,    "indent",           "indent",           0),
      (PF_FLOAT,    "line_spacing",     "line spacing",     0),
      (PF_FLOAT,    "letter_spacing",   "letter spacing",   0),
      (PF_OPTION,   "box_mode_index",   "box mode",         0, boxmode_list),
      #(PF_STRING,   "language",         "language",         'English'),
      (PF_STRING,   "padding",          "padding",          '0,150'),
      (PF_STRING,   "offsets",          "offsets",          '600,200') ],
      #(PF_BOOL,     "use_markdown",     "use markdown",     True) ],
    [],
    plugin_import_text_layers_dctrad)

main()