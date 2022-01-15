# -*- coding: utf-8 -*-
from tkinter import *
from random import randint, shuffle
from datetime import *
import os

def minus_hracovy_body(hrac):
    # pro razeni. Radime sestupne podle bodu.
    # V pripade rovnosti vzestupne podle jmena.
    return (-hrac.body, hrac.jmeno) 

class ap:
  def __init__(self, vel, vyska, sirka, prodleva):
    self.vel = vel
    self.sirka = sirka
    self.vyska = vyska
    self.prodleva = prodleva
    self.okno = Tk()
    self.okno.title("snake")
    self.platno=Canvas(self.okno,
                       width=(self.sirka+1)*self.vel,
                       height=(self.vyska+1)*self.vel,
                       bg="black")
    self.platno.pack()
    self.klavesy = []
    self.okno.bind("<KeyPress>", self.stisk)
    self.okno.bind("<KeyRelease>",self.pusteni)
    
    self.konec = False
    self.hadi = []
    self.mrtvi = []
    self.jidlo = []
    self.vyrob_jidlo()
    self.kolo = 0

  def pridej_hada(self,had):
    self.hadi.append(had)

  def vyrob_jidlo(self):
    x = randint(0,self.sirka)
    y = randint(0,self.vyska)
    if (self.obsazeno(x,y)):
      self.vyrob_jidlo()
      return
    self.jidlo.append([x,y])
    
  def stisk(self,udalost):
    if not udalost.keysym in self.klavesy:
      self.klavesy.append(udalost.keysym)
    for had in self.hadi:
      had.zmena_smeru(self.klavesy)        

  def pusteni(self,udalost):
    self.klavesy.remove(udalost.keysym)

  def vyhodnot_stav(self):
    self.konec = False
    for had in self.hadi:
      if (had.body < -30):
        print("vyrazen hrac: " + str(had.jmeno))
        self.hadi.remove(had)
        had.smrt()
        self.mrtvi.append(had)
      if (had.body > 30):
        self.konec = True
    if (len(self.hadi) <= 1):
      self.konec = True
    if (self.konec):
      if not os.path.exists('vysledky'):
        os.makedirs('vysledky')
      jmeno_souboru = "vysledky/vysledek" + str(datetime.now().strftime("%Y-%m-%d_%H_%M_%S")) + ".txt"
      with open(jmeno_souboru,"w") as file:
        file.write(jmeno_souboru + "\n")
        for had in self.mrtvi:
          file.write(str(had.jmeno) + ": " + str(had.body) + "\n")
        for had in self.hadi:
          file.write(str(had.jmeno) + ": " + str(had.body) + "\n")
          print(str(had.jmeno) + ": " + str(had.body))
        print("Konec hry. Vysledek zapsan do " + jmeno_souboru)

  def akce(self):
    self.kolo = self.kolo + 1
    shuffle(self.hadi) # pohyb hadu se vyhodnoti v nahodnem poradi
    for had in self.hadi:
      had.akce()
    self.vyhodnot_stav()
    self.platno.delete(ALL) 
    for had in self.hadi:
      had.vykresli()
    self.vykresli_jidlo()
    self.vykresli_stav()
    for had in self.hadi:
      if(isinstance(had,hrac_AI)):
        had.update(self.hadi)

    if (not self.konec):
      self.okno.after(self.prodleva, self.akce)
  
  def vykresli_jidlo(self):
    for souradnice in self.jidlo:
      x = souradnice[0]
      y = souradnice[1]
      vel = self.vel
      self.platno.create_rectangle(x * vel, y * vel,
                                   (x+1) * vel, (y + 1) * vel,
                                   fill="#eeee88")

  def vykresli_stav(self):
    self.hadi.sort(key = minus_hracovy_body)
    for i in range(len(self.hadi)):
      had = self.hadi[i]
      self.platno.create_text(20, (i + 1) * self.vel, text= str(had.jmeno) + " " + str(had.body), fill=had.barva)

  def obsazeno(self, x, y):
    if x >= self.sirka:
      return True
    if x < 0:
      return True
    if y >= self.vyska:
      return True
    if y < 0:
      return True
    for had in self.hadi:
      for clanek in had.ocas:
        if (clanek == [x,y]):
          return True
    return False

class hrac(object):
  def __init__(self,aplikace, delka, barva, jmeno, klavesy_pohyb):
    self.a = aplikace
    self.delka = delka
    self.barva=barva
    self.jmeno=jmeno
    self.klavesy_pohyb = klavesy_pohyb
    self.body = 0
    self.cas_smrti = -1
    self.ozivit()

  def kolize(self):
    self.body = self.body - 10
    self.ozivit()

  def pohyb(self,smer):
    if smer == 0 and self.x < self.a.sirka:        # doprava
      self.x = self.x + 1
    elif smer == 1 and self.y > 0:                 # nahoru
      self.y = self.y - 1
    elif smer == 2 and self.x > 0:                 # doleva
      self.x = self.x - 1
    elif smer == 3 and self.y < self.a.vyska:      # dolu
      self.y = self.y + 1
    else:
      self.kolize()
      return
    if (self.a.obsazeno(self.x,self.y)):
      self.kolize()
    self.ocas.append([self.x,self.y])
    for i in range(len(self.a.jidlo)):
      clanek = self.a.jidlo[i]
      if (clanek == [self.x,self.y]):
        self.snedeno_jidlo(i)
        return
    while(len(self.ocas) > self.delka):
      self.ocas.pop(0) 

  def snedeno_jidlo(self,i):
    self.delka = self.delka + 3
    self.body = self.body + 1
    self.a.jidlo.pop(i)
    self.a.vyrob_jidlo()
  
  def ozivit(self):
    self.x=randint(0, self.a.sirka)
    self.y=randint(0, self.a.vyska)
    self.smer=randint(0, 3)
    self.ocas = [[self.x, self.y]]
    self.delka = 5

  def zmena_smeru(self, klavesy):
    for i in range(4):
        if (self.klavesy_pohyb[i] in klavesy):
          self.smer = i
    print (self.smer)

  def akce(self):
    self.pohyb(self.smer)
  
  def smrt(self):
    self.cas_smrti = self.a.kolo

  def vykresli(self):
    for souradnice in self.ocas:
      x = souradnice[0]
      y = souradnice[1]
      vel = self.a.vel
      self.a.platno.create_rectangle(x * vel, y * vel,
                                     (x + 1) * vel,(y + 1) * vel,
                                     fill = self.barva)

class hrac_AI(hrac):
  def __init__(self,aplikace, delka, barva, jmeno, klavesy, ai):
    hrac.__init__(self,aplikace, delka, barva, jmeno, klavesy)
    self.ai = ai

  def zmena_smeru(self, klavesy):
    for i in range(4):
        if (self.klavesy_pohyb[i] in klavesy):
          self.smer = i

  def update(self, hadi):
      self.smer = self.ai.novy_smer(self,hadi)
