##############
#broken
################


import pygame as pg

CTYPE={
1:
(               #sized 24x24
      "XX                      ",
      "XXX                     ",
      "XXXX                    ",
      "XX.XX                   ",
      "XX..XX                  ",
      "XX...XX                 ",
      "XX....XX                ",
      "XX.....XX               ",
      "XX......XX              ",
      "XX.......XX             ",
      "XX........XX            ",
      "XX........XXX           ",
      "XX......XXXXX           ",
      "XX.XXX..XX              ",
      "XXXX XX..XX             ",
      "XX   XX..XX             ",
      "     XX..XX             ",
      "      XX..XX            ",
      "      XX..XX            ",
      "       XXXX             ",
      "       XX               ",
      "                        ",
      "                        ",
      "                        ")

}

class Cursor:
    def __init__(self):#, ctype):
      self.visible = True
      self.flipVisible()

      # self.ctype = ctype
      # self.changeType(self.ctype)
        
    def flipVisible(self):
        self.visible = not self.visible
        pg.mouse.set_visible(self.visible)

    def setVisible(self):
      self.visible = True
    
    def changeType(self, ctyp):
      pass
      # self.ctype = ctyp
      # c = pg.cursors.compile(CTYPE[self.ctype], black="X", white=".", xor="o")
      # print c, CTYPE[self.ctype]
      # pg.mouse.set_cursor(*c)
        