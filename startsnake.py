import snake
from random import randint
from Spanel import *
from tkinter import mainloop

a = snake.ap(20,20,30,100)
h1 = snake.hrac_AI(a, 5, "#0000ff","h1",["Right","Up","Left","Down"],ai_Spanel_random2(a))
#h1 = snake.hrac(a, 5, "#bbff00","h2",["d","w","a","s"])
h2 = snake.hrac_AI(a, 5, "#ff0000","h2",["d","w","a","s"],ai_Spanel_random2(a))
a.pridej_hada(h1)
a.pridej_hada(h2)
print("zacatek hry")
a.akce()
mainloop()

