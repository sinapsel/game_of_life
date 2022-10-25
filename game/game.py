import numpy as np
from scipy.signal import convolve2d as cv
from typing import Literal, NamedTuple, Optional, Tuple


class Rules (NamedTuple):
    '''Default rules for Game of Live with wrapping boundary conditions'''
    bottom_alive_density: int = 2
    upper_alive_density: int = 3
    borning_density: int = 3
    boundaries: Literal['fill', 'wrap', 'symm'] = 'wrap'


class Game (object):
    '''Iterable Game of Life. iterating on game object yields new state'''

    def __init__(self, init_state: Optional[np.ndarray] = None,
                 size: Optional[Tuple[int, int]] = (100, 100),
                 p: Optional[float] = 0.5, rules: Optional[Rules] = Rules()) -> None:
        self._rules: Rules = rules
        if init_state is None:
            self.size: Tuple[int, int] = size
            self._state: np.ndarray = self._generate_random(p)
        else:
            self._state: np.ndarray = init_state
            self.size = self._state.shape
        self._neighbourhood: np.ndarray = self._get_nb()

    @classmethod
    def _get_nb(cls) -> np.ndarray:
        '''convolution kernel of all ones around a cell'''
        m: np.ndarray = np.ones((3, 3))
        m[1, 1] = 0
        return m

    def _generate_random(self, probability: float) -> np.ndarray:
        '''generate True/False matrix with probability for True value'''
        return (np.random.random(self.size) <= probability)

    def _count_neighbours(self) -> np.ndarray:
        '''count all non-empty cells around each cell'''
        return cv(self._state, self._neighbourhood, mode='same',
                  boundary=self._rules.boundaries)

    def _follow_rules(self) -> None:
        '''aplying rules to game state'''
        nbh: np.ndarray = self._count_neighbours()
        alive: np.ndarray = ((nbh >= self._rules.bottom_alive_density) *
                             (nbh <= self._rules.upper_alive_density))
        birth: np.ndarray = nbh == self._rules.borning_density
        alived: np.ndarray = self._state * alive

        self._state = np.where(birth, True, alived)

    def iterate(self):
        '''do step of simulation'''
        self._follow_rules()
        return self._state

    def __next__(self):
        return next(self.__iter__())

    def __iter__(self):
        while True:
            yield self._state
            self._follow_rules()


class StateCollection:
    LINE = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    CORNER = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    RICKY = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
