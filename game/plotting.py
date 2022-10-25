from typing import Generator, Tuple, Union, Any
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class AnimationPlotter (object):
    __default_kwargs: dict[str, Union[str, int, bool]] = {
        'dpi': 144,
        'marker': 'o',
        'color': 'green',
        'repeat': True
    }

    def __init__(self, stream: Generator, frames: int, **kwargs):
        self.stream = stream
        self.frames = frames
        self.picsize = None
        self.kwargs = self.__default_kwargs | kwargs
        self.fig, self.ax = plt.subplots(figsize=(10, 10), dpi=self.kwargs['dpi'])
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.set_title('Game of life simulation')
        self.ani = animation.FuncAnimation(self.fig, func=self.onUpdate, init_func=self.onStart, blit=True,
                                           frames=self.frames, repeat=self.kwargs['repeat'])

    def onStart(self):
        """Initial drawing of the scatter plot."""
        s = (self.ax.get_window_extent().width / 50. * 72./self.fig.dpi)**2
        self.scat = self.ax.scatter([], [], s=s, c=self.kwargs['color'], marker=self.kwargs['marker'])
        return self.scat,

    def onUpdate(self, i):
        """Update the scatter plot."""
        data = next(self.stream)
        x, y = np.where(data)
        if self.picsize == None:
            self.picsize = data.shape
            self.ax.axis([-1, data.shape[0] + 1, -1, data.shape[1] + 1])
            s = (self.ax.get_window_extent().width / data.shape[0] * 72./self.fig.dpi)**2
            self.scat.set_sizes((s,)*len(x))
        self.scat.set_offsets(np.column_stack((x, y)))
        # s = (self.ax.get_window_extent().width / data.shape[0] * 72./self.fig.dpi)**2
        # self.scat.set_sizes((s,)*len(x))
        return self.scat,
