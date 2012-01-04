# -*- coding: utf-8 -*-
#
# interaction.py
#
# File created by herve couvelard - herve@viva-vous.net
# 05 2010
# license : gplv3
#
#
import sys, os 
from Tkinter import *



class interaction():

  def modif(self,config):

    config.config['size_tile_x']=int(self.tx.get())
    config.config['size_tile_y']=int(self.ty.get())
    config.config['size_map_x']=int(self.mx.get())
    config.config['size_map_y']=int(self.my.get())
    self.racine.destroy()

  def screen_size(self,item):
    size=item.split("x")
    self.mx.delete(0, END)
    self.mx.insert(0,int(size[0])/int(self.tx.get()))
    self.my.delete(0, END)
    self.my.insert(0,int(size[1])/int(self.ty.get()))


  def taille(self,config):
    retour=""
    self.racine=Tk()
    self.racine.geometry("300x300")
    self.racine.title("Yamm config")
    cadre_tuile= LabelFrame(self.racine,text="Tiles size (x,y)",width="180")
    self.tx=Entry(cadre_tuile,width=5)
    self.tx.pack(side=LEFT)
    self.tx.insert(0, config.config['size_tile_x'])
    self.ty=Entry(cadre_tuile,width=5)
    self.ty.pack(side=LEFT)
    self.ty.insert(0, config.config['size_tile_y'])
    cadre_tuile.pack(fill=X, expand=True)

    cadre_map= LabelFrame(self.racine,text="Map size (x,y)",width="180")
    self.mx=Entry(cadre_map,width=5)
    self.mx.pack(side=LEFT)
    self.mx.insert(0, config.config['size_map_x'])
    self.my=Entry(cadre_map,width=5)
    self.my.pack(side=LEFT)
    self.my.insert(0, config.config['size_map_y'])
    cadre_map.pack(fill=X, expand=True)

    cadre_standard=LabelFrame(self.racine,text="Standard size",width="180")
    bt1=Radiobutton(cadre_standard,text="Nokia N810", variable=retour, value=1, command=lambda: self.screen_size("800x480")).pack()
    bt2=Radiobutton(cadre_standard,text="gp2x", variable=retour, value=2,command=lambda: self.screen_size("320x240")).pack()
    bt3=Radiobutton(cadre_standard,text="640x480", variable=retour, value=3,command=lambda: self.screen_size("640x480")).pack()
    bt3=Radiobutton(cadre_standard,text="800x600", variable=retour, value=4,command=lambda: self.screen_size("800x600")).pack()
    bt3=Radiobutton(cadre_standard,text="1024x768", variable=retour, value=5,command=lambda: self.screen_size("1024x768")).pack()

    cadre_standard.pack(fill=X, expand=True)

    b = Button(self.racine, text="OK", command=lambda: self.modif(config)).pack(side=LEFT)

    self.racine.mainloop()
class aide():
  def general(self):
    print "coucou"
    win=Tk()
    scrollbar=Scrollbar(win)
    scrollbar.pack(side=RIGHT, fill=Y)

    f = open ("help.txt",'r')
    contenu=f.read()
    texte=Text(win,yscrollcommand=scrollbar.set)
    texte.pack()
    scrollbar.config(command=texte.yview)
    texte.insert(END,contenu)
    f.close()
    win.mainloop()

