from .game import Game, StateCollection
from .IOItering import *
from .plotting import AnimationPlotter

games: list[Game] = [
    None,
    Game(init_state=StateCollection.RICKY),
    Game(init_state=StateCollection.CORNER),
    Game(init_state=StateCollection.LINE),
    Game(p=0.37, size=(200, 200)),
    Game(p=0.22, size=(100, 100)),
    Game(p=0.27, size=(50, 50)),
]


def play( output: Optional[str] = 'out.gif', frames: Optional[int] = 150, configuration: Optional[int] = 0, 
         width: Optional[int] = 100, p: Optional[float] = 0.27, data_fname: Optional[str] = 'data.hdf5'):
    if configuration == 0:
        games[0] = Game(p=p, size=(width, width))

    g: Game = games[configuration]
    wr: IOIter = IOIterHDF(data_fname)
    wr.write(frames=frames, iterobj=g)
    p = AnimationPlotter(wr.read(), frames, marker='s', dpi=144)
    p.ani.save(output, writer='pillow', fps=30, dpi=144)
