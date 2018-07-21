#!/usr/bin/env python
# -*- coding: utf8 -*-
# -------------------------------------------------------------------------------------
#
# This file is a Python plug-in for GIMP which imports text from a file
# into layers, on a path.



import sys
import re
import codecs
from gimpfu import *

#def debugMessage(Message):
#    dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, Message)
#    dialog.run()
#    dialog.hide()

justification_list = ["Aligné à gauche", "Aligné à droite", "Centré", "Justifié"]
justification_values = [
    TEXT_JUSTIFY_LEFT, 
    TEXT_JUSTIFY_RIGHT, 
    TEXT_JUSTIFY_CENTER, 
    TEXT_JUSTIFY_FILL]
alignment_list = ["top", "bottom", "middle"]
hintstyle_list = ["Aucun", "Léger", "Moyen", "Full/Justifié"]
hintstyle_values = [
    TEXT_HINT_STYLE_NONE,
    TEXT_HINT_STYLE_SLIGHT,
    TEXT_HINT_STYLE_MEDIUM,
    TEXT_HINT_STYLE_FULL]

boxmode_list = ["fixed", "dynamic"]


def plugin_import_text_layers_path_dctrad(image, active_layer, 
    source_path, 
    page_index,
    font, 
    font_size, 
    antialias, 
    hintstyle_index, 
    #font_color, 
    justification_index, 
    #vertical_align_index, 
    line_spacing,
    letter_spacing, 
    box_mode_index):
    #use_markdown):
  indent = 0
  font_color = '#000000'
  language = 'fr'
  font_size_int = int(font_size)
  use_markdown = False
  source_escaped = False
  return import_text_layers(image, active_layer, source_path, page_index, source_escaped, font, font_size_int, antialias, hintstyle_values[hintstyle_index], font_color, justification_values[justification_index], indent, letter_spacing, line_spacing, boxmode_list[box_mode_index], language, use_markdown)

def import_text_layers(image, active_layer, source_path, page_index, source_escaped, font, font_size, antialias, hintstyle, font_color, justification, indent, letter_spacing, line_spacing, box_mode, language, use_markdown):
  special = u"\u2003"
  #source_file = file(source_path, 'r')
  source_file = codecs.open(source_path, "r", encoding="utf_8", buffering=0)
  raw_source = source_file.read()
  source_file.close()
  if (raw_source):
    source = raw_source
  else:
    pdb.gimp_message("failure: invalid source file(\""+source_path+"\")")
    return
  
  #splits on "Page " + a sequence of numbers + a newline
  pages = re.split(u"page [0-9]+(\r\n)", source.replace(special,''), flags=re.IGNORECASE)
  filtered = filter(lambda x: not re.match(r'^\s*$', x), pages)
  #pdb.gimp_message(filtered[int(page_index)-1])
  text_list = filtered[int(page_index)-1].splitlines()
  
  pdb.gimp_image_undo_group_start(image)
  
  layer_position = 0
  flag = False
  if (active_layer):
    layer_height = pdb.gimp_image_height(image)
    layer_position = pdb.gimp_image_get_layer_position(image, active_layer)
    tlayer_x = active_layer.offsets[0]
    tlayer_y = active_layer.offsets[1]
    #get active vector, path and points
    vectors = pdb.gimp_image_get_active_vectors(image)
    if(vectors == None):
      pdb.gimp_message("Vous devriez tracer un chemin avec l'outil chemin")
      n_points = 0
    else:
      nstrokes, strokes = pdb.gimp_vectors_get_strokes(vectors)
      stroke_type, n_points, cpoints, closed = pdb.gimp_vectors_stroke_get_points(vectors, strokes[0])
    #indexes in cpoints array
    x_index = 0
    y_index = 1
    #(x,y) positions for text
    x_pos = 0.0
    y_pos = 0.0
    tlayer_width = 450
    tlayer_height = 150
  
  for rawtext in text_list:
    if (source_escaped):
      text = rawtext.decode('unicode_escape')
    else:
      text = rawtext
    
    if (text != '//' and text != ''):
        if (len(text) < 20):
          tlayer_width = 150
          tlayer_height = 100
        else:
          tlayer_width = 450
          tlayer_height = 150
        
        
        if (x_index < n_points):
          #Text position from path
          x_pos = cpoints[x_index]
          y_pos = cpoints[y_index]
        else:
          if (flag == False):
            pdb.gimp_message('Attention !!!\nLe nombre de points que vous avez selectionné ne correspond pas au nombre de lignes de texte du fichier.\nLe script va continuer en placant les lignes de texte restantes en bas de la page.\nVous devriez vérifier vos bulles, ou annuler pour recommencer, en pointant toutes les bulles et encarts de texte.')
            flag = True
          x_pos = 500
          y_pos = layer_height - 200
        
        x_index += 6
        y_index += 6
        
        tlayer = pdb.gimp_text_layer_new(image, text, font, font_size, 0)
        pdb.gimp_image_add_layer(image, tlayer, layer_position)
        
        pdb.gimp_text_layer_set_antialias(tlayer, antialias)
        pdb.gimp_text_layer_set_color(tlayer, font_color)
        pdb.gimp_text_layer_set_indent(tlayer, indent)
        pdb.gimp_text_layer_set_justification(tlayer, justification)
        #pdb.gimp_text_layer_set_kerning(tlayer, kerning)
        pdb.gimp_text_layer_set_hint_style(tlayer, hintstyle)
        pdb.gimp_text_layer_set_language(tlayer, language)
        pdb.gimp_text_layer_set_letter_spacing(tlayer, letter_spacing)
        pdb.gimp_text_layer_set_line_spacing(tlayer, line_spacing)
        
        pdb.gimp_text_layer_resize(tlayer, tlayer_width, tlayer_height)    
        pdb.gimp_layer_set_offsets(tlayer, x_pos , y_pos)
        pdb.gimp_item_set_visible(tlayer, True)
  
  pdb.gimp_image_undo_group_end(image)
  
  return



register(
    "plugin_import_text_layers_path_dctrad",
    "Importer le texte le long du chemin trace",
    "Import text from file to layers on path",
    "Sergeileduc",
    "",
    "2018",
    "<Image>/DC-trad/Importer un texte sur un chemin",
    "*",
    # (type, name, description, default [, extra])
    [(PF_FILE,     "source_path",      "Fichier texte",        ''),
    (PF_SPINNER, "page_index", "Numero de page (la première page est tout le temps 1)", 1, (1, 50, 1)),
    #(PF_BOOL,     "source_escaped",   "text is escaped",  False),
    (PF_FONT,     "font",             "Police",             'Sans'),
    (PF_SPINNER,      "font_size",        "Taille de police",        27, (1, 200, 1)),
    (PF_BOOL,     "antialias",        "Lissage (antialiasing)",        True),
    (PF_OPTION,   "hintstyle_index",    "Ajustement",     0, hintstyle_list) ,
    #(PF_COLOR,    "font_color",       "font color",       '#000000'),
    (PF_OPTION,   "justification_index","Justification",  2, justification_list),
    (PF_SPINNER,    "line_spacing",     "Espacement de ligne",     0.0, (0.0, 200.0, 0.1)),
    (PF_SPINNER,    "letter_spacing",   "Espacement de lettre",   0.0, (0.0, 200.0, 0.1)),
    (PF_OPTION,   "box_mode_index",   "Boite",         0, boxmode_list)],
    [],
    plugin_import_text_layers_path_dctrad)

main()