import pyxel

pyxel.init(
    width=160,
    height=120,
    caption='typo',
)

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)

pyxel.run(update, draw)
