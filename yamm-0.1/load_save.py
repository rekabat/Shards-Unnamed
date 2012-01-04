# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#
# load_save.py
#
# File created by herve couvelard - herve@viva-vous.net
# 05 2010
# license : gplv3
#
#

import sys, os, pygame
import xml.dom.minidom as xml
import tkFileDialog
from Tkinter import *
import re

class load_save():


  def load(self,config,mapping,map_file ):
    """ load a saved map"""
    mf=open(map_file, 'r')
    data=xml.parse(mf)
    the_map=data.getElementsByTagName('map')

    for atr in the_map[0].attributes.keys():
      if atr in ('size_map_x','size_map_y','size_tile_x','size_tile_y'):
	config.config[atr]=int(the_map[0].attributes[atr].value)
      elif atr == "tiles_file":
	config.config['tiles_file']=os.path.join(os.path.dirname(map_file),os.path.basename(the_map[0].attributes[atr].value))

    mapping_string=the_map[0].childNodes[0].nodeValue
    pat='([0-9\-]+)\:([\,0-9]+)'
    coco=re.findall(pat,mapping_string)
    for i in coco:
      mapping[i[0]]=i[1]
    mf.close ()
    return True

  def save(self,config,mapping):
    """save a map"""
    tk_root = Tk()
    tk_root.withdraw()
    self.fichier=tkFileDialog.asksaveasfile(filetypes=[('map files', '*.hmp')])
    if not self.fichier:
      return
    doc = xml.Document()
    root=doc.createElementNS("herve_map", "config")
    root.setAttributeNS("herve_map","map_version","0.1")
    doc.appendChild(root)
    fichier_carte = doc.createElementNS("herve_map", "map")
    fichier_carte.setAttributeNS("herve_map","tiles_file",os.path.basename(config.config['tiles_file']))
    fichier_carte.setAttributeNS("herve_map","size_map_x",str(config.config['size_map_x']))
    fichier_carte.setAttributeNS("herve_map","size_map_y",str(config.config['size_map_y']))
    fichier_carte.setAttributeNS("herve_map","size_tile_x",str(config.config['size_tile_x']))
    fichier_carte.setAttributeNS("herve_map","size_tile_y",str(config.config['size_tile_y'])) 
    root.appendChild(fichier_carte)
    #
    # we could use pickle for serialize the dict but the xml file is uggly, a easy to read xml file is
    # what we want to have in this project
    #
    ma_str='|'.join([str(item)+":"+str(mapping[item]) for item in mapping])
    contenu_carte = doc.createTextNode(ma_str)
    fichier_carte.appendChild(contenu_carte)
    doc.writexml(self.fichier)
    self.fichier.close()



