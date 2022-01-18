# Soutěž umělé inteligence ve hře Snake

## Zadání

Vytvořte co nejlepší umělou inteligenci, co bude hrát hada.

Soutěžit budou každý týden umělé inteligence všech hráčů proti sobě.

## Jak spustit hru

Naklonujte si tento repozitář přes velké zelené tlačítko vpravo nahoře.

Buď si můžete repozitář naklonovat přes git (pro pokročilé) nebo stáhnout
jako zip a rozbalit.

Mělo by stačit spustit soubor startsnake.py a uvidíte dva ukázkové hady,
co proti sobě soutěží.

Hadi se snaží co nejdéle přežít a získat co nejvíce bodů. Výsledné pořadí
se totiž určuje primárně podle toho, v jakém pořadí hadi zemřeli a sekundárně
podle toho, kolik dostali bodů, pokud jich přežilo více.

Hra končí tím, že nějaký had dosáhne 30 bodů nebo tím, že jsou všichni hadi vyřazeni.

Za snědení jídla dostane had 1 bod a prodlouží se. Pokud narazí do zdi, do sebe nebo
do jiného hada, dostane postih -5 bodů a oživí se.

## Jak vytvořit vlastní umělou inteligenci

Ve složce participants vytvořte kopii souboru martin.py a kopii pojmenujte svým jménem

Upravte soubor startsnake.py, aby se váš nový bot připojil do hry.

Pokud se jmenujete Zbyněk, upravte soubor, aby vypadal takto:

```
from game import SnakeGame

from participants import martin, zbynek

game = SnakeGame(20, 20, 30, 1)
#game.add_human_player('Human 1', '#bbff00', ['d','w','a','s'])
game.add_ai_player('Martin', '#ff0000', martin.AI())
game.add_ai_player('Zbynek', '#ffffff', zbynek.AI())
game.start()
```

Jakmile vám to bude fungovat, můžete začít svůj soubor libovolně rozvíjet a upravovat.

Pokud zrušíte zakomentování řádku, kde se volá funkce add_human_player,
můžete proti hadům hrát sami pomocí klávesnice. Můžete samozřejmě přidat také více botů a
zkoušet různé verze proti sobě.

Své finální hady odevzdávejte buď do publicu do složky public/SIVT2021/snake/participants
nebo e-mailem. Soutěžit se bude každé úterý v 16:55.
