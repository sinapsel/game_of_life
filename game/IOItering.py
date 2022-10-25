import numpy as np
from typing import Optional
from collections.abc import Iterable
import h5py
import json


class IOIter (object):
    '''Writes states from iterable object that returns np.ndarrays and reads as iterable'''

    def __init__(self, filename: Optional[str] = 'data', dtype: Optional[type] = bool) -> None:
        self.filename: str = filename
        self.dtype = dtype

    @staticmethod
    def enumit(frames, iterobj):
        '''enumerates iterable object states'''
        return zip(np.arange(0, frames+1), iterobj)

    def write(self, frames: int, iterobj: Iterable):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def read_all(self):
        raise NotImplementedError

    def __next__(self):
        return self.read()


class IOIterTXT (IOIter):
    pass


class IOIterJSON (IOIter):
    '''implements IOIter with JSON files'''
    def write(self, frames: int, iterobj: Iterable):
        _dict = {}
        with open(self.filename, 'w') as f:
            for i, arr in IOIter.enumit(frames, iterobj):
                _dict[f'dframe_{i}'] = arr.astype(self.dtype).tolist()
            j = json.dumps(_dict)
            f.write(j)

    def read(self):
        with open(self.filename, 'r') as f:
            _dict = json.load(f)
        for i in range(len(_dict.keys())):
            yield np.array(_dict[f'dframe_{i}'])


class IOIterHDF (IOIter):
    '''implements IOIter with HDF5 files'''
    def write(self, frames: int, iterobj: Iterable):
        with h5py.File(self.filename, 'w') as f:
            for i, arr in IOIter.enumit(frames, iterobj):
                f.create_dataset(f'dframe_{i}', data=arr.astype(self.dtype))

    def read(self):
        with h5py.File(self.filename, 'r') as f:
            for i in range(len(f.keys())):
                yield f[f'dframe_{i}'][:]
