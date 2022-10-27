from typing import Generator, Tuple, Union, Any, Dict
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class AnimationPlotter (object):
    __default_kwargs: Dict[str, Union[str, int, bool]] = {
        'dpi': 144,
        'marker': 'o',
        'color': 'green',
        'repeat': True
    }

    def __init__(self, stream: Generator, frames: int, **kwargs):
        self._stream = stream
        self._frames = frames
        self._picsize = None
        self._kwargs = {**self.__default_kwargs, **kwargs}
        self._fig, self._ax = plt.subplots(figsize=(10, 10), dpi=self._kwargs['dpi'])
        self._ax.get_xaxis().set_visible(False); self._ax.get_yaxis().set_visible(False)
        self._ax.set_title('Game of life simulation')

        self.ani = animation.FuncAnimation(self._fig, func=self.onUpdate, init_func=self.onStart, blit=True,
                                           frames=self._frames, repeat=self._kwargs['repeat'])

    def onStart(self):
        """Initial drawing of the scatter plot."""
        s = (self._ax.get_window_extent().width / 50. * 72./self._fig.dpi)**2
        self._scatter = self._ax.scatter([], [], s=s, c=self._kwargs['color'], marker=self._kwargs['marker'])
        return self._scatter,

    def onUpdate(self, i):
        """Update the scatter plot."""
        data: np.ndarray = next(self._stream)
        x, y = np.where(data)
        if self._picsize == None:
            self.__first_update(data, x)
        self._scatter.set_offsets(np.column_stack((x, y)))
        return self._scatter,
    
    def __first_update(self, data: np.ndarray, x: np.ndarray) -> None:
        self._picsize = data.shape
        self._ax.axis([-1, data.shape[0] + 1, -1, data.shape[1] + 1])
        s = (self._ax.get_window_extent().width / data.shape[0] * 72./self._fig.dpi)**2
        self._scatter.set_sizes((s,)*len(x))
