import numpy as np

from pyroad.util import format_zeros


class Angulo:
    DEC_PLACES = 3

    def __init__(self, deg: float, mnt: float, sec: float):
        self.deg = deg
        self.mnt = mnt
        self.sec = sec

    def is_nan(self):
        return np.isnan(self.deg) or \
               np.isnan(self.mnt) or \
               np.isnan(self.sec)

    def __str__(self):
        deg = round(format_zeros(self.deg), self.DEC_PLACES)
        mnt = round(format_zeros(self.mnt), self.DEC_PLACES)
        sec = round(format_zeros(self.sec), self.DEC_PLACES)
        return f'{deg}° {mnt}\' {sec}\"' if not self.is_nan() else '-'

    def __repr__(self):
        return self.__str__()
