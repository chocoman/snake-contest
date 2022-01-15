from random import randint, shuffle

class ai_Spanel_random1:
  def __init__(self,a):
    self.a = a
  def novy_smer(self, had, hadi):
    return randint(0,3)

class ai_Spanel_random2:
  def __init__(self,a):
    self.a = a
    self.vyska = a.height
    self.sirka = a.width
  def novy_smer(self, had, hadi):
    volne_smery = []
    x = had.x
    y = had.y
    if (not self.a.occupied(x+1,y)):
      volne_smery.append(0)
    if (not self.a.occupied(x,y-1)):
      volne_smery.append(1)
    if (not self.a.occupied(x-1,y)):
      volne_smery.append(2)
    if (not self.a.occupied(x,y+1)):
      volne_smery.append(3)
    shuffle(volne_smery)
    if (len(volne_smery) == 0):
      return 0
    return volne_smery[0]
